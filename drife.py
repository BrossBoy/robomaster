import cv2
from robomaster import robot
import time

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis
    # 依次播放两个本地文件

    ep_robot.play_audio(filename="Tokyo_Drift.wav")
    time.sleep(2)
    ep_chassis.drive_wheels(w1=130, w2=130, w3=130, w4=130)
    time.sleep(2.7)
    ep_chassis.drive_wheels(w1=0, w2=100, w3=-100, w4=200)
    time.sleep(2.7)
    # ep_chassis.drive_wheels(w1=0, w2=50, w3=0, w4=200)
    # time.sleep(2.3)
    # ep_chassis.drive_wheels(w1=-150, w2=150, w3=-150, w4=150)
    # time.sleep(0.3)
    ep_chassis.drive_wheels(w1=0, w2=250, w3=0, w4=250)
    time.sleep(1.3)
    # ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    # time.sleep(0.1)

    ep_chassis.drive_wheels(w1=100, w2=0, w3=-100, w4=250)
    time.sleep(20)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(0.1)
    ep_robot.close()