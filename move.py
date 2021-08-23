import ev3_dc as ev3
from time import sleep
from thread_task import Sleep

# CONSTANTS
turntableGR = 60 / 8
mac = '00:16:53:49:67:10'

# INITITIALIZE MOTORS
turntableMotor = ev3.Motor(ev3.PORT_A, protocol=ev3.USB, host=mac)
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
    shooterMotor.stop_as_task(brake=True)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved tilter to deg:", tilterMotor.position)

def moveTilterByVel(vel):
    if vel == 0:
        tilterMotor.stop()
        return
    tilterMotor.speed = abs(vel)
    d = 1
    if vel < 0:
        d = -1
    tilterMotor.start_move(direction=d)

def moveShooter(numShots):
    mvmt_plan=(
    shooterMotor.move_to(shooterMotor.position + 360 * numShots, speed=100, ramp_up=40, ramp_down=40, brake=True) +
    Sleep(0.1) +
    shooterMotor.stop_as_task(brake=False)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved shooter to deg:", shooterMotor.position)

def turnAndTilt(turnVel, tiltVel):
    d1 = 1
    d2 = 1
    if turnVel < 0:
        d1 = -1
        turnVel *= -1
    if tiltVel < 0:
        d2 = -1
        tiltVel *= -1
    t1 = turntableMotor.move_for(
        1,
        speed = turnVel,
        direction = d1,
        ramp_up_time = 0,
        ramp_down_time = 0
    )
    t2 = tilterMotor.move_for(
        1,
        speed = tiltVel,
        direction = d2,
        ramp_up_time = 0,
        ramp_down_time=0
    )
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    print("Moved turntable to deg:", turntableMotor.position, "and tilter to deg:", tilterMotor.position)
    t1.stop()
    t2.stop()

def cleanup_motors():
    # Make sure no motor is left on brake when program ends
    sleep(1)
    
    turntableMotor.move_by(0).start()
    tilterMotor.move_by(0).start()
    #shooterMotor.move_by(0).start()

    sleep(1)

    if (turntableMotor.busy or tilterMotor.busy or shooterMotor.busy):
        print("Error motors are not relaxed")
