import ev3_dc as ev3

with ev3.EV3(protocol=ev3.WIFI, host='00:16:53:49:67:10') as my_robot:
    print(my_robot)