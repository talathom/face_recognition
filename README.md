# Overview

Used to detect a trained face and send a ROS message regarding it. picture_take_faces creates the raw dataset, face_trainer creates the trained model and FaceRecognition publishes messages when a trained face is detected.

## FaceRecognition.py

Uses the trained dataset to detect the target face. Whenever this face is found it publishes a ROS message.

## face_trainer.py

Creates a trained model which is used by FaceRecognition.py, requires a raw dataset of images already be stored

## picture_taker_faces.py

Takes pictures of deteced faces and stores them as the dataset which can then be trained on.



