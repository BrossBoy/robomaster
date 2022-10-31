import cv2
from robomaster import robot
import time
from chicken import check_alive_chicken
import numpy

def side_sen():
    time.sleep(0.2)
    return ep_sensor_adaptor.get_io(id=3, port=1), ep_sensor_adaptor.get_io(id=3, port=2)

def low_sen():
    time.sleep(0.2)
    return ep_sensor_adaptor.get_io(id=1, port=1)

def front_sen():
    time.sleep(0.2)
    return ep_sensor_adaptor.get_io(id=2, port=1), ep_sensor_adaptor.get_io(id=2, port=2)

def sub_data_handler(sub_info):
    global distance
    distance = sub_info

def move_left():
    ep_chassis.drive_wheels(w1=20, w2=-20, w3=20, w4=-20)
    time.sleep(0.2)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def move_right():
    ep_chassis.drive_wheels(w1=-20, w2=20, w3=-20, w4=20)
    time.sleep(0.2)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

def move_forward(t):
    ep_chassis.drive_wheels(w1=30, w2=30, w3=30, w4=30)
    time.sleep(t)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

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
    time.sleep(3)
    ep_gripper.pause()

    ep_servo.moveto(index=1, angle=45).wait_for_completed()
    ep_servo.moveto(index=1, angle=25).wait_for_completed()
    ep_servo.moveto(index=1, angle=10).wait_for_completed()
    
    ep_servo.moveto(index=2, angle=-45).wait_for_completed()
    ep_servo.moveto(index=2, angle=0).wait_for_completed()
    ep_servo.moveto(index=2, angle=45).wait_for_completed()

def close_robot():
    cv2.destroyAllWindows()
    ep_sensor.unsub_distance()
    ep_chassis.unsub_position()
    # ep_chassis.unsub_attitude()
    ep_camera.stop_video_stream()
    ep_robot.close()
    exit()

def img_process():
    img = ep_camera.read_cv2_image(strategy="newest")
    
    crop = img[200:600, 300:980]
    l = numpy.array([10, 200, 100])
    h = numpy.array([40, 255, 255])
    hsvImg = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    new_img2 = cv2.inRange(hsvImg, l, h)
    new_img2 = cv2.medianBlur(new_img2, 3)
    cv2.imshow("img", crop)
    # cv2.imshow("binary", new_img2)
    # cv2.waitKey(1000)
    contours, hier = cv2.findContours(new_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    have_chicken = []
    center_chicken = []
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 1300:
                x, y, w, hi = cv2.boundingRect(contour)
                # print(x+(w//2))
                cv2.rectangle(crop, (x,y), (x+w, y+hi), (0,255,0), 2)
                live = check_alive_chicken(hsvImg[y:y+hi, x:x+w], hi)
                have_chicken.append(live)
                center_chicken.append(x + (w//2))
                # if live == 1:
                #     cv2.putText(crop, 'alive', (x,y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                # else:
                #     cv2.putText(crop, 'dead', (x,y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)               
    # cv2.imshow("img", crop)
    return have_chicken, center_chicken

def go_center():
    l, r = side_sen()
    while r ==1:
        move_right()
        l, r = side_sen()
    ep_chassis.drive_wheels(w1=20, w2=-20, w3=20, w4=-20)
    time.sleep(1.5)
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    
def home():
    while True:
        move_forward(0.2)
        f_r, f_l = front_sen()
        if low_sen == 1:
            ep_gripper.open(power=50)
            time.sleep(3)
            ep_gripper.pause()
            break
        elif f_l == 0 or f_r == 0:
            ep_chassis.move(x=-0.3, y=0, z=0).wait_for_completed()
            ep_gripper.open(power=50)
            time.sleep(3)
            ep_gripper.pause()
            break
    ep_chassis.move(x=0, y=0, z=90).wait_for_completed()

grip = False

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    # ep_robot.initialize(conn_type="rndis")
    ep_sensor_adaptor = ep_robot.sensor_adaptor
    ep_camera = ep_robot.camera
    ep_servo = ep_robot.servo
    ep_gripper = ep_robot.gripper
    ep_chassis = ep_robot.chassis
    ep_camera.start_video_stream(display=False)
    ep_sensor = ep_robot.sensor
    # ep_sensor_a = ep_robot.sensor_adaptor
    # ep_sensor_adaptor.sub_adapter(freq=7, callback=sub_handler)
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)
    # ep_chassis.sub_position(freq=10, callback=sub_position_handler)
    # go_center()
    ep_chassis.move(x=0, y=0, z=90).wait_for_completed()

    while True:
        if not grip:
            alive = 0
            dead = 0
            dead_cen = 0
            alive_cen = 0
            min_cen = 1000
            h, c = img_process()
            for i in range(len(h)):
                cen = abs(340 - c[i])
                if h[i] == 0:
                    dead += 1
                    if cen < min_cen:
                        min_cen = cen
                        dead_cen = c[i]
                else:
                    alive += 1
                    if cen < min_cen and dead == 0:
                        min_cen = cen
                        alive_cen = c[i]
            if dead != 0:
                if dead_cen < 330:
                    move_left() # เดินซ้าย
                elif dead_cen > 350:
                    move_right() # เดินขวา
                else:
                    print("Hu ray we can do !!!!!!")
                    get_target()
                    go_center()
                    grip = True
            elif alive != 0:
                print("alive")
                if alive_cen < 340:
                    move_right()
                else:
                    move_left()
                move_forward(1.5)
            else:
                move_forward(0.5)
        else:
            home()
            grip = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    ep_sensor.unsub_distance()
    ep_sensor_adaptor.unsub_adapter()
    ep_chassis.unsub_position()
    ep_camera.stop_video_stream()
    ep_robot.close()
