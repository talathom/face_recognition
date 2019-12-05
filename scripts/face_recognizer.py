#!/usr/bin/env python
"""
Created on Tue Nov 26 15:08:33 2019

@author: thomas
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
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.pub = rospy.Publisher("/face_recognizer/FaceMessage", ArucoMessage, queue_size=10)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        #iniciate id counter
        self.id = 0
        
        # names related to ids: example ==> Thomas: id=1,  etc
        self.names = ['Unknown', 'Thomas'] 
        
    def image_callback(self, data):
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
        
        while True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
            faces = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)),)
            
            for(x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                self.id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
            
            # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = self.names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                distance = self.depth_image[int(y)][int(x)]*METERS_PER_FEET #Converts meters to feet
                if math.isnan(distance): # Check if face is too close
                    distance = -1
                face = Face(x, y, w, h, distance, 0, str(id))
                midPt = (face.xmid, face.ymid)
                print(str(midPt))
                  #TO DO: PUBLISH MESSAGE
                message.x = face.x
                message.y = face.y
                message.z = face.z
                message.name = face.name
                self.pub.publish(message)
                    
                    
                    
        
if __name__ == '__main__':
    rospy.init_node('face_detector', anonymous=True)
    face_class = Face_Recognizer()
