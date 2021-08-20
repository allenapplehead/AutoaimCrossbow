# CONSTANTS
turntableGR = 60 / 8

import ev3_dc as ev3

tgtAngle = int(45 * turntableGR)
with ev3.Motor(
    ev3.PORT_A,
    protocol=ev3.USB,
    host='00:16:53:49:67:10'
) as my_motor:
    (
        my_motor.move_by(tgtAngle, brake=True) +
        my_motor.move_by(-tgtAngle)
    ).start(thread=False)
