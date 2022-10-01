import cv2
from robomaster import robot
import keyboard
import time

def read_sensor():
    time.sleep(0.25)
    f_r = ep_sensor_adaptor.get_io(id=1, port=1)
    f_l = ep_sensor_adaptor.get_io(id=1, port=2)
    r = ep_sensor_adaptor.get_io(id=2, port=1)
    l = ep_sensor_adaptor.get_io(id=2, port=2)
    # print(f_r, f_l)
    return f_r, f_l, r, l

def move_chassis(state):
    if state == 0:
        ep_chassis.drive_wheels(w1=40, w2=40, w3=40, w4=40)
    elif state == 1:
        ep_chassis.drive_wheels(w1=20, w2=-20, w3=20, w4=-20)
    else:
        ep_chassis.drive_wheels(w1=-20, w2=20, w3=-20, w4=20)
    time.sleep(0.25)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    return read_sensor()

def check_wr(r):
    state = 2
    if r == 0:
        state = 1
        f_r, f_l, r, l = move_chassis(state)
        while f_r == 0 or f_l == 0:
            print(state)
            f_r, f_l, r, l = move_chassis(state)
    return state

def check_wl(l):
    state = 1
    if l == 0:
        state = 2
        f_r, f_l, r, l = move_chassis(state)
        while f_r == 0 or f_l == 0:
            print(state)
            f_r, f_l, r, l = move_chassis(state)
    return state

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type='rndis')

    ep_sensor_adaptor = ep_robot.sensor_adaptor
    ep_chassis = ep_robot.chassis
    print("compleat")
    time.sleep(5)
    f_r, f_l, r, l = read_sensor()
    state = 0
    while True:
        if f_r == 1 and f_l == 1:
            state = 0
        elif f_r == 0:
            state = 1
            while f_r == 0 or f_l == 0:
                state = check_wl(l)
                f_r, f_l, r, l = move_chassis(state)
        else:
            state = 2
            while f_r == 0 or f_l == 0:
                state = check_wr(r)
                f_r, f_l, r, l = move_chassis(state)
        f_r, f_l, r, l = move_chassis(state)
        if r == 0 and l == 0:
            break
    
    ep_robot.close()