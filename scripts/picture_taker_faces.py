# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:02:58 2019

@author: thomas
"""

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


class pictureTaker:
    def __init__(self, id):        
        self.bridge = CvBridge()
        self.images_taken = 0
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.face_id = id
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_color", Image, self.takePicture)
        rospy.spin()
        
    def takePicture(self, data):
        try:
            frame = np.asarray(self.bridge.imgmsg_to_cv2(data, "bgr8"))
            #build a color image and check for AR markers in it
        except CvBridgeError as e:
            print(e)
            
        if self.images_taken < 100:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
    
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)  
            
                cv2.imwrite('/home/thomas/Desktop/Facial_Recognition/dataset/image'+ str(self.images_taken) +'-'+ str(self.face_id) +'.png', gray[y:y+h,x:x+w])
                print("Took Picture "+ str(self.images_taken))
                self.images_taken += 1



if __name__ == '__main__':
    rospy.init_node('picture_taker', anonymous=True)
    pc = pictureTaker(1)