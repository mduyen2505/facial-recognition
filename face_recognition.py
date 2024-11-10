import cv2
import numpy as np
import json
from collections import deque
from skimage.feature import hog
import joblib

# Khởi tạo LBPH recognizer
lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
lbph_recognizer.read('trainer/lbph_trainer.yml')

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# Đọc tên từ file JSON
with open("names.json", "r") as file:
    names_dict = json.load(file)

cam = cv2.VideoCapture(0)
cam.set(3, 1280)  # set video width
cam.set(4, 720)  # set video height

minW = 0.05 * cam.get(3)
minH = 0.05 * cam.get(4)

# Lưu trữ kết quả nhận dạng qua các khung hình
face_history = {}
HISTORY_LENGTH = 10
CONFIDENCE_THRESHOLD = 10

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt với Viola-Jones
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    # Giới hạn số lượng khuôn mặt được xử lý
    faces = faces[:5]  # Xử lý tối đa 5 khuôn mặt

    if len(faces) == 0:
        cv2.putText(img, "Unknown", (10, 30), font, 1, (0, 0, 255), 2)
    else:
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_id = f"{x}_{y}"

            if face_id not in face_history:
                face_history[face_id] = deque(maxlen=HISTORY_LENGTH)

            face_img = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, (64, 64))
            
            # LBPH prediction
            lbph_id, lbph_confidence = lbph_recognizer.predict(face_resized)
            lbph_confidence = 100 - lbph_confidence  # Convert to percentage

            name = names_dict.get(str(lbph_id), "unknown")

            face_history[face_id].append((name, lbph_confidence))

            # Tính toán kết quả ổn định
            names, confidences = zip(*face_history[face_id])
            stable_name = max(set(names), key=names.count)
            stable_confidence = sum(conf for n, conf in face_history[face_id] if n == stable_name) / names.count(stable_name)

            # Hiển thị kết quả
            label = f"{i+1}. {stable_name}"
            cv2.putText(img, label, (x+5, y-5), font, 0.8, (255, 255, 255), 2)
            cv2.putText(img, f"{stable_confidence:.2f}%", (x+5, y+h-5), font, 0.8, (255, 255, 0), 1)

    # Hiển thị số người được nhận diện
    cv2.putText(img, f"Detected: {len(faces)}", (10, 30), font, 1, (0, 255, 0), 2)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

print("\n [INFO] Thoát chương trình")
cam.release()
cv2.destroyAllWindows()
