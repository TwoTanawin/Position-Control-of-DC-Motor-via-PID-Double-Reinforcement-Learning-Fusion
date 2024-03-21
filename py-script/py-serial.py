import serial
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backend_bases import KeyEvent

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Replace 'COMX' with the correct port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)

# Initialize lists to store data for plotting
x_data = []
y_data_1 = []
y_data_2 = []
y_data_3 = []

# Initialize the plot (assuming you want to plot the received data)
plt.ion()  # Turn on interactive mode for real-time plotting
fig, ax = plt.subplots()
line1, = ax.plot(x_data, y_data_1, label='Random Data 1')
line2, = ax.plot(x_data, y_data_2, label='Random Data 2')
line3, = ax.plot(x_data, y_data_3, label='Random Data 3')
ax.set_xlabel('Time')
ax.set_ylabel('Random Data')
ax.set_title('Real-Time Data Plot')
ax.legend()

# Function to handle keyboard events
def on_key(event):
    if isinstance(event, KeyEvent):
        if event.key == 'q':
            plt.close()
            exit()  # Terminate the program

# Connect the keyboard event handler
plt.gcf().canvas.mpl_connect('key_press_event', on_key)

# Loop to continuously send and receive data in real time
while True:
    time.sleep(0.01)
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

                # Inside the while loop where you update the plot
                # Update the plot with new data
                line1.set_xdata(x_data)
                line1.set_ydata(y_data_1)
                line2.set_xdata(x_data)
                line2.set_ydata(y_data_2)
                line3.set_xdata(x_data)
                line3.set_ydata(y_data_3)

                # Calculate the lower and upper bounds for the x-axis
                lower_bound = max(0, len(x_data) - 20)
                upper_bound = len(x_data)

                # Check if lower_bound is less than upper_bound before setting the x-axis limit
                if lower_bound < upper_bound:
                    ax.set_xlim(x_data[lower_bound], x_data[upper_bound - 1])

                ax.relim()
                ax.autoscale_view()
                plt.draw()
                plt.pause(0.01)  # Pause to allow time for plot update

        else:
            print("Invalid data received:", data)  # Print a message for debugging or logging purposes
