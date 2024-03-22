import serial
import time
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Replace 'COMX' with the correct port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)

# Initialize lists to store data for plotting
x_data = []
y_data_1 = []
y_data_2 = []
y_data_3 = []

# Initialize the plot (assuming you want to plot the received data)
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Random Data 1')
line2, = ax.plot([], [], label='Random Data 2')
line3, = ax.plot([], [], label='Random Data 3')
ax.set_xlabel('Time')
ax.set_ylabel('Random Data')
ax.set_title('Real-Time Data Plot')
ax.legend()

# Function to initialize the plot
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3

# Function to update the plot with new data
def update_plot(frame):
    # Generate three random input values
    input_data_1 = str(random.randint(-1, 1)) + '\n'
    input_data_2 = str(random.randint(-3, 3)) + '\n'
    input_data_3 = str(random.randint(-2, 2)) + '\n'

    # Send the random input values to ESP32
    ser.write(input_data_1.encode())
    ser.write(input_data_2.encode())
    ser.write(input_data_3.encode())

    # Read and append the updated random values from ESP32
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()

        # Check if data is not empty and contains a comma
        if data and ',' in data:
            random_values = list(map(int, data.split(',')))

            print(random_values)

            # Check if random_values has at least 3 elements
            if len(random_values) >= 3:
                x_data.append(time.time())  # Use current time as x-axis value
                y_data_1.append(random_values[0] + 3)  # Append the first random value
                y_data_2.append(random_values[1] - 1)  # Append the second random value
                y_data_3.append(random_values[2] - 3)  # Append the third random value

                # Update the plot with new data
                line1.set_data(x_data, y_data_1)
                line2.set_data(x_data, y_data_2)
                line3.set_data(x_data, y_data_3)

    return line1, line2, line3

# Create the animation
ani = animation.FuncAnimation(fig, update_plot, frames=None, init_func=init, blit=True, interval=100, cache_frame_data=False)


# Real-time communication with ESP32
while True:
    # Read data from ESP32 if available
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        print("Received from ESP32:", data)  # Print received data for debugging or logging purposes
        # Process the received data as needed

plt.show()
