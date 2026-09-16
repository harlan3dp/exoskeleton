import serial
import csv
try:
    with open('logger.csv', 'w', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=',')

        print("Connecting to exoskeleton...")

        try:
            with serial.Serial('/dev/ttyACM0', 115200, timeout=10) as ser:
                logwriter.writerow(['timestamp', 'raw', 'angle', 'velocity', 'acceleration'])
                while True:
                    line = ser.readline().decode().strip()
                    data = line.split(",")
                    print(data)
                    logwriter.writerow(data)

        except serial.SerialException as E:
            print(f"Unexpected error: {E}")

        except PermissionError:
            print("Permission denied. Another application may be using this device. Try adding your user to uucp and/or dialout groups.")
        

except KeyboardInterrupt:
    print("Exiting...")

except Exception as E:
    print(f"Unknown error: {E}")



