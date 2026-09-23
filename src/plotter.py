import matplotlib.pyplot as plt
import csv
import statistics
from scipy.signal import savgol_filter
import json

success = 100
generalFailure = 300
generalFileError = 301
fatalFileNotFound = 302
generalPassableError = 200
passableFileNotFound = 201
unknownError = 401


contentStr = 0
contents = int(contentStr)


while True:
    try:
        with open("iteration.txt", "r", encoding="utf-8") as file:
            raw_data = file.read().strip()
            contents = int(raw_data) if raw_data else 0

    except FileNotFoundError as e:
        print(f"File not found (error {passableFileNotFound}), creating file.")
        contents = [1]

        with open("iteration.txt", "x", encoding="utf-8") as iterationFile:
            print("Created")

    except Exception as e:
        print(f"Unknown error (code {unknownError}): {e}")
        contents = 1

    if contents >= 1:
        contents += 1
        file.close()

    else:
        contents = 1
        file.close

    with open("iteration.txt", "w", encoding="utf-8") as file:
        print(contents, file=file)
        file.close()

    response = ""

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

    print("Plotter/analysis:")
    print("What do you want to do?")
    print("[1] Normal mode")
    print("[2] Stationary noise test (outputs to term and analysis.txt)")
    print("[3] Exit")   

    try:
        response = input("Awaiting input: ").strip()
    except Exception:
        print("Not allowed. ")


    print("Opening CSV 'logger.csv'...")

    try:
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
        filtered_angle = savgol_filter(angle, 5, 2)

        for i in range(1, len(filtered_angle)):
            filtered_angle[i] = round(filtered_angle[i], 3)

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


        #--Plotting--

        x = timestamp

        plt.plot(x, filtered_angle, color='red')
        plt.plot(x, angle, color='blue')

        plt.xlabel("Timestamp")
        plt.ylabel("Angle")
        plt.title("Angle vs. time")

        plt.grid(True)

        plt.savefig("angle_plot.png")

        plt.close()

        plt.plot(x, velocity)
        plt.plot(calculated_timestamp, calculated_velocity)

        plt.xlabel("Timestamp")
        plt.ylabel("Velocity:")
        plt.title("Velocity vs. time")

        plt.grid(True)

        plt.savefig("velocity_plot.png")
        plt.close()


        plt.plot(x, acceleration)
        plt.plot(calculated_timestamp[1:], calculated_accel)

        plt.xlabel("Timestamp")
        plt.ylabel("Acceleration")
        plt.title("Acceleration vs. time")

        plt.grid(True)

        plt.savefig("acceleration_plot.png")
        plt.close()


        time_difference = []

        for i in range(1, len(timestamp)):
            difference = timestamp[i] - timestamp[i-1]
            time_difference.append(difference)

        print("Mean time diff", statistics.mean(time_difference) * 1000)
        print("Std time diff", statistics.stdev(time_difference) * 1000)
        print("Min time diff", min(time_difference) * 1000)
        print("Max time diff", max(time_difference) * 1000)

        mean_angle = round(sum(angle) / len(angle), 3)
        min_angle = min(angle)
        max_angle = max(angle)
        std_angle = round(statistics.stdev(angle), 3)
        range_of_motion = max_angle - min_angle

        std_filter = round(statistics.stdev(angle), 3)

        max_velocity = max(calculated_velocity)

        min_accel = min(calculated_accel)
        max_accel = max(calculated_accel)

        print("Iteration number ", contents)

        print("Angle: Mean, min, max, std dev, ROM:")
        print(f"{mean_angle},{min_angle},{max_angle},{std_angle},{range_of_motion}")

        print("Velocity: Max:")
        print(max_velocity)

        print("Accel: Min, max:")
        print(f"{min_accel},{max_accel}")


    except FileNotFoundError:
        print(f"File 'logger.csv' was not found (code {fatalFileNotFound}). Exiting...")
        break

    except Exception as E:
        print(f"Unknown error (code {unknownError}): {E}")
        break

    if response == '1':
        try:
            with open("analysis.txt", "w", encoding="utf-8") as file:
                file.write("Analysis:\n")
                file.write(f"Run number {contents}")
                file.write("\nAngle:\n")
                file.write(f"Mean: {mean_angle}, min: {min_angle}, max: {max_angle}, std dev: {std_angle}, rom: {round(range_of_motion), 3}.\n")
                file.write("Velocity:\n")
                file.write(f"Max: {max_velocity}. \n")
                file.write("Accel: \n")
                file.write(f"Min: {min_accel}, max: {max_accel}\n")

                file.close()

                print(f"Exiting (code {success})")

                break


        except FileNotFoundError:
            print(f"File 'analysis.txt' was nout found (code {fatalFileNotFound}). Exiting...")
            break

        except Exception as E:
            print(f"Unknown error (code {unknownError}): {E}")
            break

    elif response == '2':
        try:
            with open("analysis.txt", "w", encoding="utf-8") as file:
                file.write("Stationary noise test: \n\n")
                file.write(f"Run number {contents}")
                file.write("\nRaw angle:\n")
                file.write(f"Range = {max_angle - min_angle}, std dev = {std_angle}\n\n")

                file.write("Filtered angle: \n")
                file.write(f"Range = {round(max(filtered_angle) - min(filtered_angle)), 3}, std dev = {std_filter}")

                print("Stationary noise test: \n\n")
                print(f"Run number {contents}")
                print("\nRaw angle:\n")
                print(f"Range = {max_angle - min_angle}, std dev = {std_angle}\n\n")

                print("Filtered angle: \n")
                print(f"Range = {round(max(filtered_angle) - min(filtered_angle), 3)}, std dev = {std_filter}")

                if abs(std_angle - std_filter) <= 0.1:
                    print("Raw angle is within tolerance compared to filtered angle.")

                elif abs(std_angle - std_filter) >= 0.1:
                    print("Raw angle is not within tolerance.")

                print(f"Exited (code {success}).")
                break

        except Exception as E:
            print(f"Unknown error: {E}")
            break

    elif response == '3':
        print(f"Exiting (code {success}).")
        break


