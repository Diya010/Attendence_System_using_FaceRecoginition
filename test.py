from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak_text(text):
    try:
        if text and isinstance(text, str):
            speak_engine = Dispatch("SAPI.SpVoice")
            speak_engine.Speak(text)
        else:
            print("No text to speak.")
    except Exception as e:
        print(f"Speech error: {e}")

video = cv2.VideoCapture(0)

facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread(r"data/background.png")

COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    if not ret:
        continue

    try:
        frame = cv2.resize(frame, (640, 480))
    except Exception as e:
        print(f"Frame resize error: {e}")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    attendance = None
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        attendance = [str(output[0]), str(timestamp)]

    h_bg, w_bg = imgBackground.shape[:2]
    try:
        imgBackground[120:120+frame.shape[0], 73:73+frame.shape[1]] = frame
    except Exception as e:
        print(f"Background placement error: {e}")

    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)
    if k == ord('A') and attendance:
        speak_text("Attendance done — education pending.")
        time.sleep(1)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
