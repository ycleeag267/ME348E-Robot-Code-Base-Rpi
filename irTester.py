from irSensor import irSensor

tester_sensor = irSensor(14)

while True:
    print(f'Average IR sensor value is: {tester_sensor.averageRead()}')