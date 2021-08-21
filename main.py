from move import *
from time import sleep

# Motor threading Tests
turnAndTilt(10, 3)
sleep(2)
turnAndTilt(-10, 3)

# Velocity Control Tests
moveTilterByVel(10)
sleep(0.5)
moveTilterByVel(-5)
sleep(1)
moveTilterByVel(0)

moveTurntableByVel(30)
sleep(1)
moveTurntableByVel(-30)
sleep(1)
moveTurntableByVel(0)

# Absolute Position Control Tests
moveTurntable(45, 100)
moveTurntable(-45, 100)
moveTurntable(0, 50)

for i in range(30):
    print("Trying to move to angle:", i)
    moveTilter(i, 60)
    sleep(1)
    
moveShooter(1)
cleanup_motors()

