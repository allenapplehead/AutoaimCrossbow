#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Initialize EV3 Brick
ev3 = EV3Brick()

# Initialize motors
turntable = Motor(Port.A)
tilt = Motor(Port.C)
shoot = Motor(Port.D)
tilt.control.pid(1500, 0, 0, 1, 0.5, 1)

# Write your program here.
ev3.speaker.beep()
#shoot.run_angle(1000, 360 * 10)

"""
counter = 1

while(True):
    f = open(str(counter) + ".txt", "r")
    print("Turning to this degree:", f.read())
    #turntable.run_target(700, turn * (60/8))
    f.close()
    wait(10000)
    counter += 1
"""

for i in range(8, 35):
    print("Moving to angle", i)
    tilt.run_target(800, i)
    tilt.hold()
    print(tilt.angle())
    wait(2000)
    print(tilt.angle())

turntable.run_target(500, 45*(60/8))
print(turntable.angle())
wait(1000)
turntable.run_target(500, -45*(60/8))
print(turntable.angle())
wait(1000)
turntable.run_target(100, 0)
wait(2000)
