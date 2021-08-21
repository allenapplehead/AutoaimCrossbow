import ev3_dc as ev3
from time import sleep
from thread_task import Task, Repeated, Sleep

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

def moveTilter(moveToDeg, vel):
    mvmt_plan=(
    tilterMotor.move_to(moveToDeg, speed=vel, ramp_up=50, ramp_down=50, brake=True) +
    shooterMotor.stop_as_task(brake=True)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved tilter to deg:", tilterMotor.position)

def turnAndTilt(turntableDeg, tilterDeg, turntableVel, tilterVel):
    mvmt_plan_turn=(
        turntableMotor.move_to(int(turntableDeg * turntableGR), speed=turntableVel, ramp_up=turntableVel+10, ramp_down=turntableVel+10, brake=True) +
        turntableMotor.stop_as_task(brake=False)
    )
    mvmt_plan_tilt=(
        tilterMotor.move_to(tilterDeg, speed=tilterVel, ramp_up=50, ramp_down=50, brake=True) +
        tilterMotor.stop_as_task(brake=True)
    )
    t = Task(mvmt_plan_turn.start) + Task(mvmt_plan_tilt.start)
    t.start()
    t.stop()
    print("Moved turntable to deg:", turntableMotor.position, " and tilter to deg:", tilterMotor.position)

def moveShooter(numShots):
    mvmt_plan=(
    shooterMotor.move_to(360 * numShots, speed=100, ramp_up=100, ramp_down=100, brake=True) +
    shooterMotor.stop_as_task(brake=False)
    )
    mvmt_plan.start()
    mvmt_plan.join()
    print("Moved shooter to deg:", shooterMotor.position)

def cleanup_motors():
    # Make sure no motor is left on brake when program ends
    for _ in range(2):
        turntableMotor.move_by(0).start()
        tilterMotor.move_by(0).start()
        shooterMotor.move_by(0).start()

        sleep(1)

    if (turntableMotor.busy or tilterMotor.busy or shooterMotor.busy):
        print("Error motors are not relaxed")
