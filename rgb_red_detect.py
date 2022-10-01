import cv2
import robomaster
from robomaster import robot
import numpy

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")
    ep_camera = ep_robot.camera

    ep_camera.start_video_stream(display=False)

    # lowrgb = numpy.array([0,0,100])
    # highrgb = numpy.array([70,70,255])
    # low = numpy.array([0,150,100])
    # high = numpy.array([180,255,255])

    low = numpy.array([160,70,50])# hsv
    high = numpy.array([180,255,255])
    # vid = cv2.VideoCapture(0)
    while True:
        # ret, img = vid.read()
        img = ep_camera.read_cv2_image(strategy="newest")
        crop = img[200:650, :300]
        # gaussian_blur = cv2.GaussianBlur(src=img, ksize=(7,7), sigmaX=0, sigmaY=0)
        # median = cv2.medianBlur(img, 5)
        # gauss = cv2.GaussianBlur(img, (5,5), 0)

        # images = numpy.concatenate((median, gauss), axis=1)
        hsvImg = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

        # hslImg = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        # cv2.imshow('hsv', hsvImg)
        # cv2.imshow('hls', hslImg)
        # new_img = cv2.inRange(img, low, high)
        new_img = cv2.inRange(hsvImg, low, high)
        # median = cv2.medianBlur(new_img, 9)
        # print(hslImg[0][0])
        cv2.imshow("origin", crop)
        cv2.imshow("png", new_img)
        # cv2.imshow("b", median)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# # Destroy all the windows
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()

# # import the opencv library
# import cv2


# # define a video capture object
# vid = cv2.VideoCapture(0)

# while(True):
	
# 	# Capture the video frame
# 	# by frame
# 	ret, frame = vid.read()

# 	# Display the resulting frame
# 	cv2.imshow('frame', frame)
	
# 	# the 'q' button is set as the
# 	# quitting button you may use any
# 	# desired button of your choice
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()
