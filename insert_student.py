import mysql.connector
import os

def connect_to_database():
    """Kết nối đến cơ sở dữ liệu MySQL"""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="diem_danh"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối cơ sở dữ liệu: {err}")
        return None

def insert_student(name, lop, khoa, anh_dai_dien):
    """Chèn thông tin sinh viên vào cơ sở dữ liệu"""
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    # Kiểm tra xem ảnh có tồn tại không
    if not os.path.exists(anh_dai_dien):
        print("Ảnh không tồn tại.")
        return

    sql = "INSERT INTO sinhvien (ten_sinh_vien, lop, khoa, anh_dai_dien) VALUES (%s, %s, %s, %s)"
    val = (name, lop, khoa, anh_dai_dien)
    mycursor.execute(sql, val)

    mydb.commit()
    print("Đã thêm sinh viên thành công.")



if __name__ == "__main__":
    main()