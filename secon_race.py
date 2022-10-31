import cv2
import robomaster
from robomaster import robot
import numpy
from chicken import check_alive_chicken
import time

distance = [0]

found_dead_chicken = 0

def sub_data_handler(sub_info):
    global distance
    distance = sub_info

def close_robot():
    cv2.destroyAllWindows()
    ep_sensor.unsub_distance()
    ep_camera.stop_video_stream()
    ep_robot.close()
    exit()

def move_left():
    ep_chassis.drive_wheels(w1=20, w2=-20, w3=20, w4=-20)
    time.sleep(0.2)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def turn_left():
    ep_chassis.drive_wheels(w1=20, w2=-20, w3=-20, w4=20)
    time.sleep(0.25)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def turn_right():
    ep_chassis.drive_wheels(w1=-20, w2=20, w3=20, w4=-20)
    time.sleep(0.25)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def move_right():
    ep_chassis.drive_wheels(w1=-20, w2=20, w3=-20, w4=20)
    time.sleep(0.2)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def move_forward():
    ep_chassis.drive_wheels(w1=160, w2=160, w3=160, w4=160)
    time.sleep(0.1)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def img_process():
    img = ep_camera.read_cv2_image(strategy="newest")

    crop = img[200:650, 300:980]
    low = numpy.array([10, 200, 100])
    high = numpy.array([40, 255, 255])
    hsvImg = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    new_img2 = cv2.inRange(hsvImg, low, high)
    new_img2 = cv2.medianBlur(new_img2, 3)
    # cv2.imshow("binary", new_img2)
    contours, hier = cv2.findContours(new_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    have_chicken = []
    center_chicken = []
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 900:
                x, y, w, h = cv2.boundingRect(contour)
                print(x+(w//2))
                cv2.rectangle(crop, (x,y), (x+w, y+h), (0,255,0), 2)
                live = check_alive_chicken(hsvImg[y:y+h, x:x+w], h)
                have_chicken.append(live)
                center_chicken.append(x + (w//2))
                if live == 1:
                    cv2.putText(crop, 'alive', (x,y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(crop, 'dead', (x,y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
    # cv2.imshow("img", crop)
    return have_chicken, center_chicken

def get_target():
    while distance[0] > 250: # เดินหน้า
        print(distance[0])
        ep_chassis.drive_wheels(w1=20, w2=20, w3=20, w4=20)
        time.sleep(0.2)
        ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    ep_servo.moveto(index=2, angle=45).wait_for_completed()
    ep_servo.moveto(index=2, angle=0).wait_for_completed()
    ep_servo.moveto(index=2, angle=-45).wait_for_completed()

    ep_servo.moveto(index=1, angle=10).wait_for_completed()
    ep_servo.moveto(index=1, angle=25).wait_for_completed()
    ep_servo.moveto(index=1, angle=45).wait_for_completed()
    
    # เดินหน้าซักทีนึง
    ep_chassis.drive_wheels(w1=20, w2=20, w3=20, w4=20)
    time.sleep(0.75)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    ep_gripper.close(power=50)
    time.sleep(2)
    ep_gripper.pause()

    ep_servo.moveto(index=1, angle=45).wait_for_completed()
    ep_servo.moveto(index=1, angle=25).wait_for_completed()
    ep_servo.moveto(index=1, angle=10).wait_for_completed()

    ep_servo.moveto(index=2, angle=-45).wait_for_completed()
    ep_servo.moveto(index=2, angle=0).wait_for_completed()
    ep_servo.moveto(index=2, angle=45).wait_for_completed()

    ep_gripper.open(power=50)
    time.sleep(2)
    ep_gripper.pause()

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    # ep_robot.initialize(conn_type="rndis")
    ep_camera = ep_robot.camera
    ep_servo = ep_robot.servo
    ep_gripper = ep_robot.gripper
    ep_chassis = ep_robot.chassis
    ep_camera.start_video_stream(display=False)
    ep_sensor = ep_robot.sensor
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)

    while True:
        have_chicken, center_chicken = img_process()
        
        dead_count = 0
        center = 1000
        real_cen = 0
        for i in range(len(have_chicken)):
            if have_chicken[i] == 0:
                dead_count += 1
                dead_center = abs(340 - center_chicken[i])
                if dead_center < center:
                    center = dead_center
                    real_cen = center_chicken[i]

        if dead_count == 0:
            move_forward()
        else:
            if real_cen < 330:
                move_left() # เดินซ้าย
            elif real_cen > 350:
                move_right() # เดินขวา
            else:
                print("Hu ray we can do !!!!!!")
                get_target()
                close_robot()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    ep_sensor.unsub_distance()
    ep_camera.stop_video_stream()
    ep_robot.close()
