# import os
# import cv2
# import face_recognition
# import numpy as np
#
# path = '../media/images'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)
#
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)
#
#
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#
#     return encodeList
#
#
# encodeListKnown = findEncodings(images)
# print('Encoding complete', len(encodeListKnown), encodeListKnown[0])
#
# cap = cv2.VideoCapture(0)
#
# while True:
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#
#     for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#
#         matchIndex = np.argmin(faceDis)
#
#         if matches[matchIndex] and min(faceDis) < 0.5:
#             name = classNames[matchIndex].upper()
#             print(name)
#         else:
#             name = "Unknown"
#
#         y1, x2, y2, x1 = faceLoc
#         y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
#
#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)


# import cv2
# import face_recognition
# from .models import User, AttendanceRecord
# from datetime import date
# import numpy as np
#
#
# # Load all registered users and their face encodings
# def load_user_encodings():
#     users = User.objects.all()
#     user_encodings = []
#     user_ids = []
#
#     for user in users:
#         if user.face_embedding:
#             user_encodings.append(np.frombuffer(user.face_embedding, dtype=np.float64))
#             user_ids.append(user.user_id)
#
#     return user_encodings, user_ids
#
#
# def mark_attendance(user_id):
#     """Marks attendance for a recognized user"""
#     user = User.objects.get(user_id=user_id)
#     attendance = AttendanceRecord.objects.create(
#         user=user,
#         attendance_date=date.today(),
#         status="present",  # Automatically mark as present
#         note="Face recognized"
#     )
#     attendance.save()
#
#
# def recognize_faces_from_camera():
#     """Capture video feed, detect faces, and mark attendance"""
#     video_capture = cv2.VideoCapture(0)  # Use 0 for default camera
#
#     user_encodings, user_ids = load_user_encodings()
#
#     while True:
#         ret, frame = video_capture.read()
#
#         if not ret:
#             print("Failed to grab frame")
#             break
#
#         # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
#         rgb_frame = frame[:, :, ::-1]
#
#         # Find all face locations and face encodings in the current frame
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         # Loop over the faces found in the current frame
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             # Compare the face encoding with the known encodings
#             matches = face_recognition.compare_faces(user_encodings, face_encoding)
#
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 recognized_user_id = user_ids[first_match_index]
#
#                 # Mark attendance automatically for the recognized user
#                 mark_attendance(recognized_user_id)
#
#                 # Draw a rectangle around the face
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#                 # Label the face with the user's name
#                 user = User.objects.get(user_id=recognized_user_id)
#                 cv2.putText(frame, user.name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
#
#         # Display the resulting image
#         cv2.imshow("Face Recognition Attendance", frame)
#
#         # Break the loop if the user presses 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     video_capture.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     recognize_faces_from_camera()
