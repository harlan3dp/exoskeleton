import numpy as np
import csv

sample_rate = 100
duration = 10
frequency  = 1

time = np.arange(0, duration, 1 / sample_rate)
print(time)

angle = 65 + 40 * np.sin(2 * np.pi * frequency * time)
print(angle)

angles = angle.tolist()


with open('logger.csv', 'w', newline='') as csvfile:
    logwriter = csv.writer(csvfile, delimiter=',')
    logwriter.writerow(['timestamp','angle'])
    for time, angle in zip(time, angle):
        logwriter.writerow([time, angle])   
                



