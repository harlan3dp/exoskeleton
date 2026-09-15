import matplotlib.pyplot as plt
import csv
import statistics
from scipy.signal import savgol_filter


timestamp = []
angle = []
velocity = []
acceleration = []
filtered_angle = []

new_velocity = []
calculated_velocity = []
calculated_timestamp = []

new_accel = []
calculated_accel = []

print("Opening CSV 'logger.csv'...")

with open ('logger.csv', newline='') as csvfile:
    logreader = csv.reader(csvfile, delimiter=',')

    next(logreader)

    print("Assigning lists...")

    for row in logreader:
        timestamp.append(float(row[0]) / 1000000)
        angle.append(float(row[2]))
        velocity.append(float(row[3]))
        acceleration.append(float(row[4]))

print("Calculating...")

filtered_velocity = savgol_filter(velocity, 11, 3)
filtered_angle = savgol_filter(angle, 11, 2)

for i in range(1, len(filtered_angle)):

    angle_diff = filtered_angle[i] - filtered_angle[i-1]
    time_diff = timestamp[i] - timestamp[i-1]

    calc_velocity = angle_diff / time_diff

    calculated_velocity.append(float(calc_velocity))
    calculated_timestamp.append(timestamp[i])



for i in range(1, len(calculated_velocity)):
    velocity_diff = calculated_velocity[i] - calculated_velocity[i-1]
    time_diff = calculated_timestamp[i] - calculated_timestamp[i-1]

    calc_accel = velocity_diff / time_diff

    calculated_accel.append(float(calc_accel))


x = timestamp

plt.plot(x, filtered_angle, color='red')

plt.xlabel("Timestamp")
plt.ylabel("Angle")
plt.title("Angle vs. time")

plt.grid(True)

plt.savefig("angle_plot.png")

plt.close()


plt.plot(x, acceleration)
plt.plot(calculated_timestamp[1:], calculated_accel)

plt.xlabel("Timestamp")
plt.ylabel("Acceleration")
plt.title("Acceleration vs. time")

plt.grid(True)

plt.savefig("acceleration_plot.png")
plt.close()


mean_angle = round(sum(angle) / len(angle), 3)
min_angle = min(angle)
max_angle = max(angle)
std_angle = round(statistics.stdev(angle), 3)

print("Mean, min, max, std dev:")
print(f"{mean_angle},{min_angle},{max_angle},{std_angle}")



