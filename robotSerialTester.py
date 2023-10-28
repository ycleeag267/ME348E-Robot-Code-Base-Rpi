import serial

ser = serial.Serial('COM4', 115200, timeout = 1)

while True: 
    if ser.is_open:
        try:
            # Create a string of four comma-separated integers
            data_to_send = "42, 12, 8, 56\n"  # Make sure to include the newline character

            # Send the string to the serial port
            ser.write(data_to_send.encode())

            print("Data sent:", data_to_send.strip())

            # Wait for a response (optional)
            response = ser.readline().decode().strip()
            responseList = response.strip().split(',')
            integer_list = [int(element) for element in responseList]
            print(integer_list)

        except:
            pass