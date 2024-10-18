import tkinter as tk
from tkinter import messagebox
from model import DatabaseModel
from view import LoginView, MainView

class Controller:
    def __init__(self, root):
        # Khởi tạo model với bảng students trong PostgreSQL
        self.model = DatabaseModel(db_name='', user='', password='', host='', port='', table_name='students')
        self.root = root
        self.login_view = None
        self.main_view = None
        self.show_login_view()  # Hiển thị giao diện đăng nhập khi khởi động

    def show_login_view(self):
        """ Hiển thị giao diện đăng nhập. """
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.login_view = LoginView(self.root, self)

    def show_main_view(self):
        """ Hiển thị giao diện chính (MainView) sau khi đăng nhập thành công. """
        for widget in self.root.winfo_children():
            widget.destroy()  # Xóa các widget của giao diện đăng nhập

        self.main_view = MainView(self.root, self)
        self.main_view.load_students()  # Tải danh sách sinh viên từ cơ sở dữ liệu

    def login(self, host, database, user, password, port):
        """ Phương thức đăng nhập để kết nối với cơ sở dữ liệu PostgreSQL. """
        if self.model.connect(db_name=database, user=user, password=password, host=host, port=port):
            self.show_main_view()  # Mở giao diện chính nếu kết nối thành công
            return True
        else:
            messagebox.showerror("Đăng nhập thất bại", "Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra lại thông tin.")
            return False

    def logout(self):
        """ Đăng xuất và quay lại giao diện đăng nhập. """
        self.model.close()  # Đóng kết nối cơ sở dữ liệu
        self.show_login_view()  # Hiển thị lại giao diện đăng nhập

    def add_student(self, name, student_id, birth_year):
        """ Thêm sinh viên mới vào cơ sở dữ liệu và cập nhật giao diện. """
        try:
            self.model.insert_data(student_id, name, birth_year)
            self.main_view.load_students()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")

    def fetch_all_students(self):
        """ Lấy toàn bộ danh sách sinh viên từ cơ sở dữ liệu. """
        return self.model.fetch_all_data()  # Gọi phương thức trong model

    def fetch_student_scores(self, student_id):
        """ Lấy điểm của sinh viên theo mã số. """
        return self.model.fetch_student_scores(student_id)  # Gọi phương thức trong model

    def update_student(self, student_id, name, birth_year):
        """ Cập nhật thông tin sinh viên trong cơ sở dữ liệu. """
        try:
            self.model.update_data(student_id, name, birth_year)
            messagebox.showinfo(f"Cập nhật thành công sinh viên ID: {student_id} với tên: {name}, năm sinh: {birth_year}")
            self.main_view.load_students()  # Cập nhật lại danh sách sinh viên sau khi cập nhật
        except Exception as e:
            messagebox.showerror(f"Lỗi khi cập nhật sinh viên: {e}")

    def delete_student(self, student_id):
        """ Xóa sinh viên khỏi cơ sở dữ liệu và cập nhật giao diện. """
        try:
            # Gọi model để xóa sinh viên bằng id
            self.model.delete_data(student_id)
            # Cập nhật lại giao diện sau khi xóa
            self.main_view.load_students()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")

    def enter_scores(self, student_id, math_score, literature_score, english_score):
        """ Nhập điểm cho sinh viên trong cơ sở dữ liệu và cập nhật giao diện. """
        try:
            self.model.enter_scores(student_id, math_score, literature_score, english_score)
            self.main_view.load_students()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập điểm: {e}")

    def sort_by_scores(self):
        """ Sắp xếp sinh viên theo điểm. """
        try:
            sorted_students = self.model.sort_students_by_scores()
            self.main_view.display_sorted_students(sorted_students)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sắp xếp: {e}")

    def highest_score_by_subject(self):
        """ Tìm sinh viên có điểm cao nhất theo từng môn và hiển thị kết quả. """
        try:
            highest_scores = self.model.highest_score_by_subject()
            self.main_view.display_highest_scores(highest_scores)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm điểm cao nhất: {e}")

    def export_data(self):
        """ Xuất dữ liệu sinh viên và điểm ra tệp TXT. """
        try:
            self.model.export_data()
            messagebox.showinfo("Xuất dữ liệu", "Dữ liệu đã được xuất ra tệp students_scores.txt thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {e}")

    def close_connection(self):
        """ Đóng kết nối với cơ sở dữ liệu. """
        self.model.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
