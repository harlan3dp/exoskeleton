import serial
import csv

with open('logger.csv', 'w', newline='') as csvfile:
    logwriter = csv.writer(csvfile, delimiter=',')

    with serial.Serial('/dev/ttyACM0', 115200, timeout=10) as ser:
        logwriter.writerow(['timestamp', 'raw', 'angle', 'velocity', 'acceleration'])
        while True:
            line = ser.readline().decode().strip()
            data = line.split(",")
            print(data)
            logwriter.writerow(data)





