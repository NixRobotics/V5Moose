# ------------------------------------------
# 
# 	Project:      Moose
#	Author:       FX
#	Created:      10/2/2026
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

brain = Brain()

left_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

controller = Controller()

WHEEL_SIZE = 320 # mm

wait(100, MSEC)

def drive_for(direction, distance): # mm, direction can be FORWARD or REVERSE
    # move forward 600 mm
    number_of_turns = distance / WHEEL_SIZE
    left_motor.spin_for(direction, number_of_turns, TURNS, wait=False)
    right_motor.spin_for(direction, number_of_turns, TURNS)

def autonomoose():
    brain.screen.clear_screen(Color.BLUE)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("HELLO MOOSE")

    drive_for(FORWARD, 600)

def ipressedR2():
    arm_motor.set_velocity(100, PERCENT)
    arm_motor.spin_for(REVERSE, 360, DEGREES)

def ipressedR1():
    arm_motor.set_velocity(100, PERCENT)
    arm_motor.spin_for(FORWARD, 360, DEGREES)

claw_is_open = False
def ipressedA():
    global claw_is_open
    claw_motor.set_velocity(100, PERCENT)
    claw_motor.set_timeout(1, SECONDS)
    if claw_is_open:
        claw_motor.spin_for(FORWARD, 360, DEGREES)
        claw_motor.stop(COAST)
        claw_is_open = False
    else:
        claw_motor.spin_for(REVERSE, 360, DEGREES)
        claw_motor.stop(COAST)
        claw_is_open = True

def idriverobot():
    brain.screen.clear_screen(Color.GREEN)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("I DRIVE ROBOT")
    brain.screen.new_line()

    # R2 is lower_arm
    controller.buttonR2.pressed(ipressedR2)
    # R1 is raise_arm
    controller.buttonR1.pressed(ipressedR1)
    # A is open/close claw
    controller.buttonA.pressed(ipressedA)

    while True:
        gas = controller.axis3.position()
        turn = controller.axis1.position()

        left_speed = gas + turn
        right_speed = gas - turn

        left_motor.spin(FORWARD, left_speed, PERCENT)
        right_motor.spin(FORWARD, right_speed, PERCENT)

        wait(10, MSEC)

comp = Competition(idriverobot, autonomoose)
# Begin project code
