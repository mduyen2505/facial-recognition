def run_dataset_with_name():
    name = simpledialog.askstring("Nhập Tên", "Nhập tên người dùng và nhấn Enter ==>")
    if name:
        subprocess.Popen(["python", "face_dataset.py", name])
