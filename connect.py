import rpyc

# Create a RPyC connection to the remote ev3dev device.
# Use the hostname or IP address of the ev3dev device.
# If this fails, verify your IP connectivty via ``ping X.X.X.X``
conn = rpyc.classic.connect('192.168.0.100')

# import ev3dev2 on the remote ev3dev device
ev3dev2_motor = conn.modules['ev3dev2.motor']

# Use the LargeMotor and TouchSensor on the remote ev3dev device
motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_A)

# If the TouchSensor is pressed, run the motor
while True:
    motor.run_forever(speed_sp=200)

    ts.wait_for_released()
    motor.stop()
