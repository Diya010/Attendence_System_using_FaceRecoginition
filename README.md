# Attendence_System_using_FaceRecoginition


This project is a Face Recognition-based Attendance System built with OpenCV and KNN algorithm.
It captures real-time video feed, recognizes faces of registered users, and automatically marks their attendance in a CSV file.
Additionally, the system provides voice feedback using Windows voice service (win32com) whenever attendance is successfully marked.

-->Features

 -Face Registration – Add new users using add_faces.py.
 -Face Recognition – Recognize faces in real-time using KNN classifier.
 -Voice Feedback – Announces "Attendance marked" via win32com voice.
 -CSV Storage – Attendance automatically logged with timestamp in a CSV file.
 -User-Friendly UI – Custom background frame (background.png).

-->Technologies Used

 -Python 3
 -OpenCV (face detection & recognition pipeline)
 -scikit-learn (KNN classifier for recognition)
 -pickle (to save face encodings & names)
 -win32com.client (text-to-speech voice feedback)
 -CSV (attendance storage)
