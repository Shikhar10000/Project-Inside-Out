#!/usr/bin/env python
# coding: utf-8

# In[ ]:




import cv2
import numpy as np
from keras.models import load_model
from statistics import mode
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import random
import time


from firestore import fs
i=0
USE_WEBCAM = True 
Emotion_score_array=[0.5]*30

emotion_model_path = './models/emotion_model.hdf5'
emotion_labels = get_labels('fer2013')


frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model_path)


emotion_target_size = emotion_classifier.input_shape[1:3]


emotion_window = []


cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(0)

# Select video or webcam feed
cap = None
if (USE_WEBCAM == True):
    cap = cv2.VideoCapture(0) # Webcam source
else:
    cap = cv2.VideoCapture(u'basic_emotion.mp4') # Video file source

while cap.isOpened(): # True:
    ret, bgr_image = cap.read()

    #bgr_image = video_capture.read()[1]

    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(.22)
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(-0.4)
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(0.9)
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(.61)
        elif emotion_text == 'disgust':
            color = emotion_probability * np.asarray((0, 255, 0))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(.001)
        elif emotion_text == 'fear':
            color = emotion_probability * np.asarray((0, 255, 0))
            Emotion_score_array.pop(0)
            Emotion_score_array.append(.1)
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image)
    # print(Emotion_score_array)
    i=i+1

    if i==100:
        Emotion_score=np.array(Emotion_score_array)
        a=np.mean(Emotion_score)+random.uniform(0.001,0.07)
        a=round(a,2)
        if a<=0.1:
            a=0.1
        if a>=0.99:
            a=0.99
        print(a)
        timestamp = int(time.time())
        fs(a,timestamp,u'actual')
        #appreciation
        if a<=0.65:
            ap=a+random.uniform(0.01,0.09)
        else:
            ap=a
        print(round(ap,2))
        fs(round(ap,2),timestamp,u'appreciation')
        i=0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

