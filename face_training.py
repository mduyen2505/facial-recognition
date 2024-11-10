import cv2
import numpy as np
import os
import json
from skimage.feature import hog
import joblib

# Đường dẫn đến thư mục chứa ảnh
path = 'dataset'

# Khởi tạo mô hình LBPH và bộ phát hiện khuôn mặt Haar Cascade
lbph_recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def extract_features(image):
    """Trích xuất đặc trưng HOG từ ảnh."""
    image = cv2.resize(image, (64, 64))  # Đảm bảo ảnh có kích thước chuẩn
    features = hog(image, orientations=8, pixels_per_cell=(8, 8),
                   cells_per_block=(1, 1), visualize=False)
    return features

def getImagesAndLabels(path):
    """Đọc ảnh và nhãn từ thư mục đã chỉ định."""
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]  # Chỉ đọc ảnh jpg
    faceSamples = []
    ids = []
    hog_features = []

    for imagePath in imagePaths:
        # Đọc ảnh với màu xám (grayscale) để dễ dàng phát hiện khuôn mặt
        PIL_img = cv2.imread(imagePath, 0)
        if PIL_img is None:
            print(f"Không thể đọc ảnh: {imagePath}")
            continue
        
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])  # Giả sử ID nằm trong tên file

        # Phát hiện khuôn mặt trong ảnh
        faces = detector.detectMultiScale(img_numpy, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = img_numpy[y:y + h, x:x + w]
            face_resized = cv2.resize(face, (64, 64))  # Resize khuôn mặt về kích thước cố định
            
            faceSamples.append(face_resized)
            hog_features.append(extract_features(face_resized))
            ids.append(id)

    return faceSamples, np.array(hog_features), np.array(ids)

def main():
    """Chương trình chính để huấn luyện mô hình LBPH."""
    print("\n [INFO] Đang huấn luyện khuôn mặt. Vui lòng đợi ...")
    
    # Lấy dữ liệu ảnh và nhãn
    faces, hog_features, ids = getImagesAndLabels(path)
    
   
    # Huấn luyện mô hình LBPH với dữ liệu ảnh và nhãn
    lbph_recognizer.train(faces, np.array(ids))
    
    # Lưu mô hình LBPH vào tệp .yml
    lbph_recognizer.write('trainer/lbph_trainer.yml')
    
    print(f"\n [INFO] Đã huấn luyện {len(np.unique(ids))} khuôn mặt:")
    for id in np.unique(ids):
        # Tạo tên danh sách khuôn mặt (có thể thay đổi theo cách bạn muốn)
        print(f"ID {id}: {id}")  # Bạn có thể thay đổi ở đây để lấy tên từ file json nếu có.
    
    print("Mô hình LBPH đã được lưu thành công.")

if __name__ == "__main__":
    main()
