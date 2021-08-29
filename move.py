import ev3_dc as ev3
from time import sleep
from thread_task import Sleep

# CONSTANTS
turntableGR = 56 / 8
mac = '00:16:53:49:67:10'

turnKp = 0.015
turnKi = 0
turnKd = 0
turnIActiveZone = 10

tiltKp = 0.025
tiltKi = 0
tiltKd = 0

# GLOBAL VARS
lastTurnError = 0
lastTiltError = 0
turnErrorSum = 0
tiltErrorSum = 0
l = 0 # min tilter angle
r = 25 # max tilter angle
ranLastTime = 0

# INITITIALIZE MOTORS
turntableMotor = ev3.Motor(ev3.PORT_A, protocol=ev3.WIFI, host=mac)
tilterMotor = ev3.Motor(ev3.PORT_C, ev3_obj=turntableMotor)
shooterMotor = ev3.Motor(ev3.PORT_D, ev3_obj=turntableMotor)

def moveTurntable(moveToDeg, vel):
    mvmt_plan=(
        turntableMotor.move_to(int(moveToDeg * turntableGR), speed=vel, ramp_up=vel+10, ramp_down=vel+10, brake=True) +
        turntableMotor.stop_as_task(brake=False)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved turntable to deg:", turntableMotor.position)

def moveTurntableByVel(vel):
    if vel == 0:
        turntableMotor.stop()
        return
    turntableMotor.speed = abs(vel)
    d = 1
    if vel < 0:
        d = -1
    turntableMotor.start_move(direction=d)

def moveTilter(moveToDeg, vel):
    mvmt_plan=(
    tilterMotor.move_to(moveToDeg, speed=vel, ramp_up=50, ramp_down=50, brake=True) +
    tilterMotor.stop_as_task(brake=True)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved tilter to deg:", tilterMotor.position)

def moveTilterByVel(vel):
    if vel == 0:
        tilterMotor.stop(brake=True)
        return
    tilterMotor.speed = abs(vel)
    d = 1
    if vel < 0:
        d = -1
    tilterMotor.start_move(direction=d)

def moveShooter(numShots):
    mvmt_plan=(
    shooterMotor.move_to(shooterMotor.position + 362 * numShots, speed=100, ramp_up=0, ramp_down=0, brake=True) +
    Sleep(0.1) +
    shooterMotor.stop_as_task(brake=False)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved shooter to deg:", shooterMotor.position)

def turnAndTilt(turnError, tiltError):
    global lastTurnError, lastTiltError, turnErrorSum, tiltErrorSum, l, r, ranLastTime

    # Turntable PID calculations
    turnErrorDiff = turnError - lastTurnError
    lastTurnError = turnError
    turnErrorSum += lastTurnError
    turnSpeed = turnKp * turnError + turnKi * turnErrorSum + turnKd * turnErrorDiff
    if abs(turnError) > turnIActiveZone:
        turnSpeed -= turnKi * turnErrorSum
    if abs(turnSpeed) > 100:
        if turnSpeed > 0:
            turnSpeed = 100
        else:
            turnSpeed = -100
    if abs(turnSpeed) < 1 and abs(turnSpeed) > 0.1:
        if turnSpeed > 0:
            turnSpeed = 3
        else:
            turnSpeed = -3
    turnVel = int(turnSpeed)

    d1 = 1

    if turnVel != 0:
        if turnVel < 0:
            d1 = -1
            turnVel *= -1
        t1 = turntableMotor.move_for(
            0.2,
            speed = turnVel,
            direction = d1,
            ramp_up_time = 0,
            ramp_down_time = 0
        )
        t1.start()
    else:
        t1 = (
            turntableMotor.move_to(turntableMotor.position, speed=100, ramp_up=0, ramp_down=0, brake=True) +
            Sleep(0.1) + 
            turntableMotor.stop_as_task(brake=False)
        )
        t1.start()

    # Tilter calculations
    # Binary searching for the meaning of life (correct tilter angle)
    if l > r:
        # reset bsearch
        print("RESET BSEARCH")
        l = 0
        r = 25
    
    mid = (l + r) // 2

    if abs(tiltError) <= 18: # an accuracy threshold
        pass # the current mid value is correct, hold the tilter there
    else:
        if ranLastTime % 4 == 0:
            if tiltError > 0:
                l = mid + 1
            elif tiltError < 0:
                r = mid - 1

        ranLastTime += 1
    
        print("BSEARCH DEBUG:", mid, l, r)

        d2 = 1

        t2 = (
            tilterMotor.move_to(mid, speed=60, ramp_up=100, ramp_down=100, brake=True)
        )

        t2.start()
        t2.join()

    t1.join()
    

    print("Moved turntable to deg:", turntableMotor.position, "and tilter to deg:", tilterMotor.position)
    t1.stop()
    #t2.stop()

def cleanup_motors():
    # Make sure no motor is left on brake when program ends 
    t1 = (
        turntableMotor.move_to(turntableMotor.position, speed=100, ramp_up=0, ramp_down=0, brake=True) +
        Sleep(0.1) + 
        turntableMotor.stop_as_task(brake=False)
    )
    t2 = (
        tilterMotor.move_to(tilterMotor.position, speed=100, ramp_up=0, ramp_down=0, brake=True) +
        Sleep(0.1) +
        tilterMotor.stop_as_task(brake=False)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t1.stop()
    t2.stop()

    #moveShooter(0)

    if (turntableMotor.busy or tilterMotor.busy or shooterMotor.busy):
        print("Error: motors are not relaxed")