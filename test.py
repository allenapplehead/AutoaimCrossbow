import ev3_dc as ev3

with ev3.EV3(protocol=ev3.USB) as my_robot:
    print(my_robot)
