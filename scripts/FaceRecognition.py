#!/usr/bin/env python
"""
Last Updated on 1/1/2020

@author: Thomas Talasco
"""

import cv2
from Face import Face
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import math
from face_recognition.msg import FaceMessage

message = FaceMessage()
METERS_PER_FEET = 3.281

class Face_Recognizer:
    
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_color", Image, self.image_callback)
        self.depth_sub = rospy.Subscriber("/camera/depth/image", Image, self.depth_callback)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.faceCascade = cv2.CascadeClassifier("Faces.xml")
        self.pub = rospy.Publisher("/face_recognizer/FaceMessage", FaceMessage, queue_size=10)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.depth_image = [[0 for x in range(640)] for y in range(480)] # initialize zero array
        #iniciate id counter
        self.id = 0
        
        # names related to ids: example ==> Thomas: id=1,  etc
        self.names = ['Unknown', 'Thomas'] 
        
        rospy.spin()
        
    def depth_callback(self, data):
        try:
            self.depth_image = np.asarray(self.bridge.imgmsg_to_cv2(data, '32FC1'))
            # Build a cv_image from the data in the depth image callback
        except CvBridgeError as e:
            print(e)
            
    def image_callback(self, data):
        self.faceCascade = cv2.CascadeClassifier("Faces.xml")
        #print("NEW IMAGE")
        global METERS_PER_FEET
        global message
        try:
            frame = np.asarray(self.bridge.imgmsg_to_cv2(data, "bgr8"))
            #build a color image and check for AR markers in it
        except CvBridgeError as e:
            print(e)
                
        #Set min area to be recognized as a face
        minH = frame.shape[0]*0.1
        minW = frame.shape[1]*0.1
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        faces = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)))
            
        for(x,y,w,h) in faces:
            #print("Saw a Face")
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            self.id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
            
            # Check if confidence is less them 125 ==> "0" is perfect match 
            if (confidence < 125):
                #Detected known face
                self.id = self.names[self.id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                #Flag face as unknown
                self.id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            face = Face(x, y, w, h, -1, str(self.id))
            
            face.z = self.depth_image[int(face.ymid)][int(face.xmid)]*METERS_PER_FEET #Converts meters to feet
            if math.isnan(face.z): # Check if face is too close
                face.z = -1
            #Publish Message    
            message.x = face.x
            message.y = face.y
            message.z = face.z
            message.h = face.h
            message.w = face.w
            message.name = face.name
            self.pub.publish(message)
                    
                    
                    
        
if __name__ == '__main__':
    rospy.init_node('face_detector', anonymous=True)
    face_class = Face_Recognizer()
