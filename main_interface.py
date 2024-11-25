import tkinter as tk
from tkinter import simpledialog
import subprocess

def run_dataset_with_name():
    name = simpledialog.askstring("Nhập Tên", "Nhập tên người dùng và nhấn Enter ==>")
    if name:
        subprocess.Popen(["python", "face_dataset.py", name])

def run_file(file_name):
    subprocess.Popen(["python", file_name])

root = tk.Tk()
root.title("NHÓM 6 - XỬ LÝ ẢNH")

# Cấu hình cửa sổ
root.configure(bg='gray')
root.geometry("500x500")

# Tạo frame chính
main_frame = tk.Frame(root, bg='gray')
main_frame.place(relx=0.5, rely=0.5, anchor='center')
group_label = tk.Label(main_frame, 
                       text="HỆ THỐNG NHẬN DẠNG KHUÔN MẶT \nNHÓM 6 - Xử lý ảnh \nGiảng viên: Hồ Văn Quí", 
                       bg='gray', fg='black', 
                       font=('Arial', 16, ), 
                       relief=tk.RAISED, bd=5, padx=20, pady=20)
group_label.pack(pady=25)

# Tạo và định vị các nút
btn_dataset = tk.Button(main_frame, text="HÌNH ẢNH", command=run_dataset_with_name, 
                        width=40, height=4, bg='white', relief=tk.RAISED)
btn_dataset.pack(pady=10)

btn_training = tk.Button(main_frame, text="HUẤN LUYỆN", command=lambda: run_file("face_training.py"), 
                         width=40, height=4, bg='white', relief=tk.RAISED)
btn_training.pack(pady=10)

btn_recognition = tk.Button(main_frame, text="TRÍCH XUẤT", command=lambda: run_file("face_recognition.py"), 
                            width=40, height=4, bg='white', relief=tk.RAISED)
btn_recognition.pack(pady=10)

root.mainloop()