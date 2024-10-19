import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.create_login_screen()

    def create_login_screen(self):
        self.root.title("Đăng Nhập")
        self.root.geometry("300x250")

        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.pack(pady=10, padx=10)

        self.db_name = tk.StringVar(value='postgres')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')

        tk.Label(self.connection_frame, text="Database App", fg="blue", font="Helvetica 14 bold").grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.connection_frame, text="DB Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.connection_frame, textvariable=self.db_name).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.connection_frame, text="User:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.connection_frame, textvariable=self.user).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.connection_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.connection_frame, textvariable=self.password, show="*").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.connection_frame, text="Host:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.connection_frame, textvariable=self.host).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.connection_frame, text="Port:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.connection_frame, textvariable=self.port).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Button(self.connection_frame, text="Connect", command=self.login).grid(row=6, column=0, columnspan=2, pady=10)

    def login(self):
        database = self.db_name.get()
        user = self.user.get()
        password = self.password.get()
        host = self.host.get()
        port = self.port.get()

        if self.controller.login(host, database, user, password, port):
            self.controller.show_main_view()  # Mở giao diện chính nếu đăng nhập thành công
        else:
            messagebox.showerror("Lỗi", "Đăng nhập thất bại")

class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.create_main_screen()   

    def create_main_screen(self):
        self.root.title("ỨNG DỤNG QUẢN LÝ SINH VIÊN")
        self.root.geometry("600x500")

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True)

        # Tạo Tab 1 và thêm vào notebook
        self.tab1 = ttk.Frame(notebook)
        notebook.add(self.tab1, text="Quản Lý Sinh Viên")

        self.tab2 = ttk.Frame(notebook)
        notebook.add(self.tab2, text="Quản lý điểm")

        # Tạo tiêu đề cho Tab 1
        title_label = tk.Label(self.tab1, text="ỨNG DỤNG QUẢN LÝ SINH VIÊN", fg="red", font="helvetica 16 bold", width=30)
        title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Tạo Listbox để hiển thị danh sách sinh viên
        self.listbox_tab1 = tk.Listbox(self.tab1, width=70, height=10)
        self.listbox_tab1.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Tạo Entry để nhập thông tin sinh viên
        tk.Label(self.tab1, text="Nhập tên Sinh Viên:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.tab1, width=40)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab1, text="Nhập mã số Sinh Viên:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.id_entry = tk.Entry(self.tab1, width=40)
        self.id_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab1, text="Nhập năm sinh Sinh Viên:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.birth_year_entry = tk.Entry(self.tab1, width=40)
        self.birth_year_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Tạo các Button để thêm, sửa, xóa sinh viên
        button_frame = tk.Frame(self.tab1)
        button_frame.grid(row=5, column=0, columnspan=4, pady=10)

        tk.Button(button_frame, text="Thêm", command=self.add_student, width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Sửa", command=self.edit_student, width=10).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_student, width=10).grid(row=0, column=2, padx=5)

        # Cấu hình lưới để giãn nở Listbox
        self.tab1.grid_rowconfigure(1, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)

        # Tạo tiêu đề cho Tab 2
        title_label = tk.Label(self.tab2, text="QUẢN LÝ ĐIỂM", fg="red", font="helvetica 16 bold", width=30)
        title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.listbox_scores = tk.Listbox(self.tab2, width=70, height=10)
        self.listbox_scores.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        tk.Button(self.tab2, text="Cập nhật dữ liệu", command=self.load_students).grid(row=6, column=0, columnspan=4, pady=10)

        # Tạo Label và Entry cho các môn học trong Tab 2
        self.math_label = tk.Label(self.tab2, text="Nhập điểm Toán:")
        self.math_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.math_entry = tk.Entry(self.tab2, width=20)
        self.math_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.literature_label = tk.Label(self.tab2, text="Nhập điểm Văn:")
        self.literature_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.literature_entry = tk.Entry(self.tab2, width=20)
        self.literature_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.english_label = tk.Label(self.tab2, text="Nhập điểm Anh:")
        self.english_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.english_entry = tk.Entry(self.tab2, width=20)
        self.english_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Tạo các Button cho các chức năng trong Tab 2
        scores_button_frame = tk.Frame(self.tab2)
        scores_button_frame.grid(row=5, column=0, columnspan=4, pady=10)

        tk.Button(scores_button_frame, text="Nhập Điểm", command=self.enter_scores, width=10).grid(row=0, column=0, padx=5)
        tk.Button(scores_button_frame, text="Sắp Xếp Điểm", command=self.sort_by_scores, width=10).grid(row=0, column=1, padx=5)
        tk.Button(scores_button_frame, text="Điểm Cao Nhất", command=self.highest_score_by_subject, width=10).grid(row=0, column=2, padx=5)
        tk.Button(scores_button_frame, text="Xuất Dữ Liệu", command=self.controller.export_data, width=20).grid(row=0, column=3, padx=5)

        # Cấu hình lưới để giãn nở Listbox
        self.tab2.grid_rowconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(1, weight=1)

    def load_students(self):
        """ Cập nhật dữ liệu trong Listbox của cả hai Tab. """
        self.listbox_tab1.delete(0, tk.END)
        self.listbox_scores.delete(0, tk.END)

        students = self.controller.fetch_all_students()
        for student in students:
            # Cập nhật Listbox trong Tab 1
            student_info_tab1 = f"{student[1]} - {student[0]} - {student[2]}"
            self.listbox_tab1.insert(tk.END, student_info_tab1)

            # Cập nhật Listbox trong Tab 2 (Quản lý điểm)
            scores_info = f" - Toán: {student[3]}, Văn: {student[4]}, Anh: {student[5]}"
            student_info_tab2 = f"{student[0]} - {student[1]} - {student[2]}{scores_info}"
            self.listbox_scores.insert(tk.END, student_info_tab2)

    def add_student(self):
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        birth_year = self.birth_year_entry.get()

        if name and student_id and birth_year:
            self.controller.add_student(name, student_id, birth_year)
            self.clear_entries()
            self.load_students()  # Cập nhật lại danh sách

    def edit_student(self):
        selected_index = self.listbox_tab1.curselection()
        if not selected_index:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn sinh viên để sửa.")
            return
        
        # Lấy chuỗi thông tin sinh viên từ Listbox
        student_info = self.listbox_tab1.get(selected_index)
        
        # Tách các thành phần thông tin sinh viên, đảm bảo lấy đúng ID
        student_info_parts = student_info.split(" - ")
        if len(student_info_parts) >= 2:
            student_id = student_info_parts[1].strip()  # ID sinh viên
            name = self.name_entry.get()
            birth_year = self.birth_year_entry.get()
            
            if name and student_id and birth_year:
                try:
                    # Gọi hàm update_student trong controller để cập nhật vào cơ sở dữ liệu
                    self.controller.update_student(student_id, name, birth_year)
                    
                    # Cập nhật lại Listbox
                    self.load_students()
                    messagebox.showinfo("Thành công", "Sửa thông tin sinh viên thành công.")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể sửa sinh viên: {e}")
            else:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
        else:
            messagebox.showerror("Lỗi", "Không thể lấy ID sinh viên từ Listbox.")


    def delete_student(self):
        selected_index = self.listbox_tab1.curselection()
        if not selected_index:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn sinh viên để xóa.")
            return
        
        # Lấy thông tin sinh viên từ Listbox
        student_info = self.listbox_tab1.get(selected_index)
        
        # Lấy id từ chuỗi sinh viên (phần tử thứ hai sau dấu gạch ngang đầu tiên)
        id = student_info.split(" - ")[1]  # Lấy đúng giá trị id
        
        # Kiểm tra nếu student_id có phải là số không
        try:
            id = int(id)  # Chuyển đổi thành số nguyên
        except ValueError:
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return

        # Xóa sinh viên khỏi cơ sở dữ liệu
        self.controller.delete_student(id)
        
        # Cập nhật lại Listbox
        self.load_students()  # Gọi lại phương thức này để tải lại danh sách sinh viên
        self.clear_entries()  # Xóa thông tin đã nhập

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.birth_year_entry.delete(0, tk.END)
        self.math_entry.delete(0, tk.END)
        self.literature_entry.delete(0, tk.END)
        self.english_entry.delete(0, tk.END)

    def enter_scores(self):
        selected_index = self.listbox_scores.curselection()  # Chọn sinh viên từ listbox_tab1
        if not selected_index:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn sinh viên để nhập điểm.")
            return
        
        # Lấy mã sinh viên từ danh sách đã chọn
        student_info = self.listbox_scores.get(selected_index).split(" - ")
        student_id = student_info[0]  # Giả sử mã sinh viên là phần đầu tiên
        
        math_score = self.math_entry.get()
        literature_score = self.literature_entry.get()
        english_score = self.english_entry.get()
        
        # Kiểm tra xem điểm có hợp lệ không
        if math_score and literature_score and english_score:
            # Cập nhật điểm vào cơ sở dữ liệu
            self.controller.enter_scores(student_id, math_score, literature_score, english_score)
            
            # Cập nhật lại Listbox hiển thị điểm
            self.load_students()  # Gọi lại phương thức để cập nhật danh sách sinh viên
            self.clear_entries()  # Xóa các ô nhập sau khi nhập điểm thành công
        else:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin điểm.")

    def sort_by_scores(self):
        """ Hiển thị sinh viên theo thứ tự điểm trung bình từ cao đến thấp. """
        try:
            # Lấy danh sách sinh viên đã sắp xếp từ model
            sorted_students = self.controller.model.sort_students_by_scores()

            # Xóa nội dung hiện tại trong Listbox
            self.listbox_tab1.delete(0, tk.END)
            self.listbox_scores.delete(0, tk.END)

            # Hiển thị danh sách sinh viên đã sắp xếp
            for student in sorted_students:
                student_info_tab1 = f"{student[1]} - {student[0]} - {student[2]}"
                self.listbox_tab1.insert(tk.END, student_info_tab1)

                scores_info = f" Trung bình: {student[6]:.2f}"
                student_info_tab2 = f"{student[0]} - {student[1]} - {student[2]}{scores_info}"
                self.listbox_scores.insert(tk.END, student_info_tab2)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sắp xếp sinh viên: {e}")

    def highest_score_by_subject(self):
        """ Tìm sinh viên có điểm cao nhất trong từng môn và hiển thị trong Listbox """
        try:
            # Lấy sinh viên có điểm cao nhất từ model
            highest_scores = self.controller.model.highest_score_by_subject()

            # Hiển thị kết quả trong Listbox tab2
            self.listbox_scores.delete(0, tk.END)  # Xóa dữ liệu cũ

            # Hiển thị sinh viên có điểm cao nhất Toán
            math_student = highest_scores['math']
            if math_student:
                self.listbox_scores.insert(tk.END, f"Điểm Toán cao nhất: {math_student[1]} - {math_student[2]} điểm")
            
            # Hiển thị sinh viên có điểm cao nhất Văn
            literature_student = highest_scores['literature']
            if literature_student:
                self.listbox_scores.insert(tk.END, f"Điểm Văn cao nhất: {literature_student[1]} - {literature_student[2]} điểm")
            
            # Hiển thị sinh viên có điểm cao nhất Anh
            english_student = highest_scores['english']
            if english_student:
                self.listbox_scores.insert(tk.END, f"Điểm Anh cao nhất: {english_student[1]} - {english_student[2]} điểm")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm điểm cao nhất: {e}")


    def export_data(self):
        with open("students_scores.txt", mode="w", encoding="utf-8") as file:
            file.write("Mã số\tTên\tNăm sinh\tĐiểm Toán\tĐiểm Văn\tĐiểm Anh\n")
            file.write("="*60 + "\n")

            for index in range(self.listbox_scores.size()):
                student = self.listbox_scores.get(index)
                student_info = student.split(" - ")
                
                # Đảm bảo đủ số lượng phần tử trước khi xử lý
                if len(student_info) >= 4:
                    id_name_birth = student_info[:3]  # Lấy ID, tên, năm sinh
                    scores = student_info[3].split(", ")  # Lấy điểm
                    scores_values = [score.split(": ")[1] for score in scores]

                    # Ghi dữ liệu vào file
                    file.write(f"{id_name_birth[0]}\t{id_name_birth[1]}\t{id_name_birth[2]}\t" +
                            f"{scores_values[0]}\t{scores_values[1]}\t{scores_values[2]}\n")

            messagebox.showinfo("Xuất dữ liệu", "Dữ liệu đã được xuất ra tệp students_scores.txt thành công!")

