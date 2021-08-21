from move import *
from time import sleep

"""
turnAndTilt(45, 20, 100, 60)
sleep(3)
turnAndTilt(0, 0, 50, 30)
cleanup_motors()
"""

moveTurntable(45, 100)
moveTurntable(-45, 100)
moveTurntable(0, 50)

for i in range(30):
    print("Trying to move to angle:", i)
    moveTilter(i, 60)
    sleep(1)
    
moveShooter(1)
cleanup_motors()

