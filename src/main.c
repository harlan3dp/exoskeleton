#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c_master.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "driver/gpio.h"

#define I2C_SDA 23
#define I2C_SCL 20
#define AS5600_ADDR 0x36

#define LED_GPIO 2

void app_main(void)
{   
    gpio_reset_pin(LED_GPIO);
    gpio_set_direction(LED_GPIO, GPIO_MODE_OUTPUT);

    float prevAngle = 0;
    float prevVol = 0;

    bool prevLedState = 0;

    int64_t prevTime = esp_timer_get_time();

    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = I2C_SDA,
        .scl_io_num = I2C_SCL,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };

    i2c_master_bus_handle_t bus_handle;

    ESP_ERROR_CHECK(
        i2c_new_master_bus(&bus_config, &bus_handle)
    );

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = AS5600_ADDR,
        .scl_speed_hz = 400000,
    };

    i2c_master_dev_handle_t as5600;

    ESP_ERROR_CHECK(
        i2c_master_bus_add_device(
            bus_handle,
            &dev_config,
            &as5600
        )
    );

    printf("AS5600 connected!\n");

    while (1)
    {
        uint8_t reg = 0x0C;
        uint8_t data[2];

        esp_err_t result = i2c_master_transmit_receive(
            as5600,
            &reg,
            1,
            data,
            2,
            100
        );

        if (result == ESP_OK)
        {
            uint16_t raw_angle =
                ((uint16_t)data[0] << 8) | data[1];

            raw_angle &= 0x0FFF;

            float angle = raw_angle * 360.0f / 4096.0f;

            int64_t currentTime = esp_timer_get_time();
            float elapsedSeconds = (currentTime - prevTime) / 1000000.0f;

            float angleDiff = angle - prevAngle;

            if (angleDiff > 180) {
                angleDiff -= 360;
            }

            else if (angleDiff < -180) {
                angleDiff +=360;
            }

            prevAngle = angle;
            prevTime = currentTime;

            float angular_velocity = angleDiff / elapsedSeconds;

            float angleVolDiff = angular_velocity - prevVol;
            
            float angularAccel = angleVolDiff / elapsedSeconds;

            printf("%lld,%u,%.2f,%.2f,%.2f\n", currentTime, raw_angle, angle, angular_velocity, angularAccel);

            prevVol = angular_velocity;

        }
        else
        {
            printf("I2C read failed: %s\n",
                   esp_err_to_name(result));

            if (prevLedState == 0) {
                gpio_set_level(LED_GPIO, 1);
                prevLedState = 1;
                }
                
            else {
                gpio_set_level(LED_GPIO, 0);
                prevLedState = 0;
            }

        }       

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}