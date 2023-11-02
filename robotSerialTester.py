# import serial

# ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

# while True: 
#     if ser.is_open:
#         try:
#             # Create a string of four comma-separated integers
#             data_to_send = "42, 12, 8, 56\n"  # Make sure to include the newline character

#             # Send the string to the serial port
#             ser.write(data_to_send.encode())

#             print("Data sent:", data_to_send.strip())

#             # Wait for a response (optional)
#             response = ser.readline().decode().strip()
#             responseList = response.strip().split(',')
#             integer_list = [int(element) for element in responseList]
#             print(integer_list)

#         except:
#             pass

#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)