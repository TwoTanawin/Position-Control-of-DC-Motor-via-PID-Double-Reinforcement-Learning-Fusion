import serial
import time
import random

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Update 'COM3' with your Arduino's port
counter = 0
try:
    while True:
        
        # v1 = random.random()
        # v2 = random.random()
        # v3 = random.random()
        counter += 1
        print(f"counter : {counter}")
        
        # // PID constants
        v1 = 0.1
        v2 = 0.006
        v3 = 0.0
        
        # Send data to Arduino
        data_to_send = f"{v1},{v2},{v3}\n"  # Example data
        ser.write(data_to_send.encode())

        # Wait for a short time to allow Arduino to process the data
        # time.sleep(1)

        try:
            received_data = ser.readline().decode('utf-8', errors='ignore').strip()
            print("Received data:", received_data)  # Print received data for debugging
            
            values = received_data.split(",")  # Split the CSV into individual values
            if len(values) >= 3:
                try:
                    sum_val = float(values[0])
                    sum_squared = float(values[1])
                    sqrt_sum = float(values[2])
                    print("target:", str(sum_val))
                    print("pos:", str(sum_squared))
                    print("e:", str(sqrt_sum))
                except ValueError as e:
                    print("Error converting data to float:", e)
                    # Handle the error as needed
            else:
                print("Received data in unexpected format:", received_data)
        except UnicodeDecodeError as e:
            print("Error decoding data:", e)
            # Handle the error as needed

except KeyboardInterrupt:
    print("Exiting program due to KeyboardInterrupt.")

# Close serial port
ser.close()
