import serial
import time
import random

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Update 'COM3' with your Arduino's port

try:
    while True:
        
        v1 = random.random()
        v2 = random.random()
        v3 = random.random()
        
        # Send data to Arduino
        data_to_send = f"{v1},{v2},{v3}\n"  # Example data
        ser.write(data_to_send.encode())

        # Wait for a short time to allow Arduino to process the data
        time.sleep(1)

        received_data = ser.readline().decode().strip()
        values = received_data.split(",")  # Split the CSV into individual values
        if len(values) >= 3:
            sum_val = float(values[0])
            sum_squared = float(values[1])
            sqrt_sum = float(values[2])
            print("Received Sum:", sum_val)
            print("Received Sum Squared:", sum_squared)
            print("Received Square Root of Sum:", sqrt_sum)
        else:
            print("Received data in unexpected format:", received_data)

except KeyboardInterrupt:
    print("Exiting program due to KeyboardInterrupt.")

# Close serial port
ser.close()
