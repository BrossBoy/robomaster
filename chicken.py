import numpy as np
import cv2 as cv

def check_alive_chicken(hsv_img, high):
    org_l = np.array([5, 150, 100])
    org_h = np.array([20, 255, 255])
    chicken_org = cv.inRange(hsv_img, org_l, org_h)
    chicken_org = cv.medianBlur(chicken_org, 7)
    contours, hier = cv.findContours(chicken_org, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    y = 0
    max_arae = 0
    if len(contours) != 0:
        max_arae = 0
        for contour in contours:
            arae = cv.contourArea(contour)
            if arae > max_arae:
                x, y, w, hi = cv.boundingRect(contour)
                max_arae = arae
    if y > (high//2)  :
        return 1
    else:
        return 0

if __name__ == "__main__":
    yellow_l = np.array([10, 100, 20])
    yellow_h = np.array([35, 255, 255])

    img = cv.imread('test_chicken.jpg')
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    detect = cv.inRange(hsv_img, yellow_l, yellow_h)

    contours, hier = cv.findContours(detect, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        for contour in contours:
            if cv.contourArea(contour) > 1500:
                x, y, w, hi = cv.boundingRect(contour)
                y = y + (hi//2)
                check_alive_chicken(hsv_img[y:y+hi, x:x+w], detect[y:y+hi, x:x+w])
                
    # cv.imshow("origin", img)
    cv.imshow("yellow_a_org", detect)
    cv.waitKey(0)
    cv.destroyAllWindows()
    pass
