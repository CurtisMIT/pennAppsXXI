import cv2 
import numpy as np 
  
def contourCoordinates(img):
    image = cv2.imread(img) 
    cv2.waitKey(0) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    edged = cv2.Canny(gray, 30, 200) 
    cv2.waitKey(0) 
  
    # Finding Contours 
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours, hierarchy
    
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 