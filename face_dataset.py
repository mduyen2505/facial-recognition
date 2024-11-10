import cv2
import os
import json
import sys

# Kiểm tra xem có đối số dòng lệnh cho tên người dùng không
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print("Vui lòng cung cấp tên người dùng khi chạy script.")
    sys.exit(1)

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height

# Đọc ảnh và phát hiện khuôn mặt trong quá trình tạo dataset
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Đọc danh sách tên hiện có hoặc tạo mới nếu không tồn tại
try:
    with open("names.json", "r") as file:
        names_dict = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    names_dict = {}

# Tạo ID mới
new_id = str(len(names_dict) + 1)

# Thêm tên mới vào từ điển
names_dict[new_id] = name

# Lưu từ điển cập nhật vào file
with open("names.json", "w") as file:
    json.dump(names_dict, file)

print(f"\n [INFO] Bắt đầu chụp ảnh cho {name} (ID: {new_id}). Hãy nhìn vào camera và chờ ...")
count = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1

        # Lưu ảnh vào thư mục dataset
        cv2.imwrite(f"dataset/User.{new_id}.{count}.jpg", gray[y:y+h, x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 30:  # Tăng số lượng ảnh lên 30
        break

print("\n [INFO] Hoàn thành chụp ảnh. Thoát chương trình.")
cam.release()
cv2.destroyAllWindows()