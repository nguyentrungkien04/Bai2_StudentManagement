import psycopg2
from psycopg2 import sql
from tkinter import messagebox

class DatabaseModel:
    def __init__(self, db_name=None, user=None, password=None, host=None, port=None, table_name='students'):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table_name = table_name
        self.connection = None
        self.cursor = None

    def connect(self, db_name, user, password, host, port):
        """ Kết nối tới cơ sở dữ liệu PostgreSQL. """
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            messagebox.showinfo("Thông báo", "Kết nối thành công!")
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Kết nối thất bại: {e}")
            return False

    def fetch_all_data(self):
        """ Lấy tất cả dữ liệu sinh viên từ bảng. """
        query = f"SELECT id, name, birth_year, math_score, literature_score, english_score FROM {self.table_name}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()  # Trả về tất cả dữ liệu
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")
            return []

    def fetch_student_scores(self, student_id):
        """ Lấy điểm của sinh viên theo mã số. """
        query = sql.SQL("SELECT math_score, literature_score, english_score FROM {table} WHERE id = %s").format(
            table=sql.Identifier(self.table_name)
        )
        try:
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()  # Trả về điểm của sinh viên
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy điểm sinh viên: {e}")
            return None

    def insert_data(self, student_id, name, birth_year):
        """ Thêm sinh viên mới vào bảng. """
        insert_query = f"INSERT INTO {self.table_name} (id, name, birth_year) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(insert_query, (student_id[:20], name[:50], birth_year[:4]))
            self.connection.commit()
            messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi thêm sinh viên: {e}")

    def update_data(self, student_id, name, birth_year):
        """ Cập nhật thông tin sinh viên trong bảng. """
        query = f"UPDATE {self.table_name} SET name = %s, birth_year = %s WHERE id = %s"
        try:
            self.cursor.execute(query, (name, birth_year, int(student_id)))
            self.connection.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            messagebox.showinfo("Thông báo", f"Đã cập nhật sinh viên ID: {student_id} với tên: {name}, năm sinh: {birth_year}")
        except Exception as e:
            self.connection.rollback()  # Khôi phục giao dịch nếu có lỗi
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật sinh viên: {e}")

    def delete_data(self, student_id):
        """ Xóa sinh viên khỏi bảng bằng cột id. """
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = %s"
            self.cursor.execute(query, (student_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Khôi phục giao dịch khi gặp lỗi
            messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")


    def enter_scores(self, student_id, math_score, literature_score, english_score):
        """ Nhập điểm cho sinh viên. """
        query = f"UPDATE {self.table_name} SET math_score = %s, literature_score = %s, english_score = %s WHERE id = %s"
        try:
            self.cursor.execute(query, (math_score, literature_score, english_score, student_id))
            self.connection.commit()
            messagebox.showinfo("Thông báo", "Nhập điểm thành công!")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi nhập điểm: {e}")

    def sort_students_by_scores(self):
        """ Sắp xếp sinh viên theo điểm trung bình của các môn từ cao đến thấp. """
        try:
            # Thực hiện truy vấn sắp xếp sinh viên theo điểm trung bình
            query = f"SELECT id, name, birth_year, math_score, literature_score, english_score, " \
                    f"((math_score + literature_score + english_score) / 3.0) as average_score " \
                    f"FROM {self.table_name} ORDER BY average_score DESC"
            self.cursor.execute(query)
            sorted_students = self.cursor.fetchall()

            return sorted_students  # Trả về danh sách sinh viên đã sắp xếp
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sắp xếp sinh viên: {e}")

    def highest_score_by_subject(self):
        """ Tìm sinh viên có điểm cao nhất trong từng môn học. """
        try:
            # Câu truy vấn SQL để tìm sinh viên có điểm cao nhất cho từng môn
            highest_math = f"SELECT id, name, math_score FROM {self.table_name} ORDER BY math_score DESC LIMIT 1"
            highest_literature = f"SELECT id, name, literature_score FROM {self.table_name} ORDER BY literature_score DESC LIMIT 1"
            highest_english = f"SELECT id, name, english_score FROM {self.table_name} ORDER BY english_score DESC LIMIT 1"

            # Thực hiện truy vấn cho từng môn
            self.cursor.execute(highest_math)
            math = self.cursor.fetchone()

            self.cursor.execute(highest_literature)
            literature = self.cursor.fetchone()

            self.cursor.execute(highest_english)
            english = self.cursor.fetchone()

            # Kiểm tra nếu có kết quả và trả về dữ liệu
            if math and literature and english:
                result = {
                    "math": math,
                    "literature": literature,
                    "english": english
                }

                # Hiển thị thông tin sinh viên có điểm cao nhất trên giao diện
                messagebox.showinfo(
                    "Điểm cao nhất",
                    f"Toán: {math[1]} - Điểm: {math[2]}\n"
                    f"Văn: {literature[1]} - Điểm: {literature[2]}\n"
                    f"Anh: {english[1]} - Điểm: {english[2]}"
                )
                return result
            else:
                messagebox.showwarning("Thông báo", "Không có dữ liệu để hiển thị.")
                return None

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm điểm cao nhất: {e}")
            return None

    def export_data(self):
        """ Xuất dữ liệu sinh viên và điểm ra tệp TXT với định dạng mong muốn. """
        try:
            with open("students_scores.txt", mode="w", encoding="utf-8") as file:
                # Dòng tiêu đề không cần thiết vì xuất dữ liệu theo định dạng tự do
                # Ghi các cột cần thiết với định dạng mong muốn
                query = f"SELECT id, name, birth_year, math_score, literature_score, english_score FROM {self.table_name}"
                self.cursor.execute(query)
                students = self.cursor.fetchall()

                for student in students:
                    id, name, birth_year, math, literature, english = student
                    # Ghi thông tin sinh viên theo định dạng yêu cầu
                    file.write(f"Tên: {name}, Mã số: {id}, Năm sinh: {birth_year}, "
                            f"Điểm Toán: {math}, Điểm Văn: {literature}, Điểm Anh: {english}\n")

            messagebox.showinfo("Thông báo", "Dữ liệu đã được xuất ra tệp students_scores.txt thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất dữ liệu: {e}")

    def close(self):
        """ Đóng kết nối cơ sở dữ liệu. """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            messagebox.showinfo("Thông báo", "Đã đóng kết nối cơ sở dữ liệu!")
