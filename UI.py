import sys
import os
import tkinter as tk
import pandas as pd
from tkinter import font, ttk, messagebox
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.LoadDataController import load_data_into_table
from Controller.AddMovieController import add_movie

"""Phần code cho giao diện chính của ứng dụng Oscar Award Winner"""
window = tk.Tk()
window.title("Oscar Movie")
window.configure(bg='#1E1E1E')
window.state("zoomed")

# Tạo font chữ cho tiêu đề, nút và có in đậm
title_font = font.Font(family="Helvetica", size=22, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")

title_label = tk.Label(window, text="OSCAR AWARD WINNER", font=title_font, fg="#FFD700", bg="#1E1E1E")
title_label.pack(pady=10, padx=(190, 10))

button_frame = tk.Frame(window, bg='#1E1E1E')
button_frame.pack(side="left", fill="y", padx=20, pady=10, expand=False)

# Sự kiện hover cho nút
def on_enter(e):
    e.widget['bg'] = "#FFD700"

def on_leave(e):
    e.widget['bg'] = "#2E2E2E"

def print_chart():
    print("Chart")

def add_movie_ui():
    for widget in display_area.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(display_area, bg="#333333", width=800, height=500)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Đảm bảo frame mở rộng theo kích thước chỉ định
    main_frame.pack_propagate(False)

    # Tiêu đề giao diện thêm phim mới
    title_label = tk.Label(main_frame, text="Add New Movie", font=title_font, fg="#FFD700", bg="#333333")
    title_label.pack(pady=(0, 15), padx=(50, 15))

    # Hàm tạo hàng nhập liệu
    def create_input_row(parent, label_text):
        row_frame = tk.Frame(parent, bg="#333333")
        row_frame.pack(fill="x", pady=8)

        label = tk.Label(row_frame, text=label_text, font=button_font, fg="#FFD700", bg="#333333")
        label.pack(side="left", padx=(0, 15))

        entry = tk.Entry(row_frame, width=45, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700")
        entry.pack(side="left", fill="x", expand=True)
        
        return entry

    # Tạo các trường nhập liệu
    film_entry = create_input_row(main_frame, "Film:")
    year_entry = create_input_row(main_frame, "Year:")
    award_entry = create_input_row(main_frame, "Award:")
    nomination_entry = create_input_row(main_frame, "Nomination:")

    # Hàm lưu dữ liệu phim mới
    def save_new_movie():
        # Lấy dữ liệu từ các trường nhập liệu
        film = film_entry.get()
        year = year_entry.get()
        award = award_entry.get()
        nomination = nomination_entry.get()

        # Kiểm tra nếu các trường dữ liệu bắt buộc không được bỏ trống, trừ khi giải thưởng = 0
        if not film or not year or not nomination or (award != '0' and not award):
            messagebox.showerror("Dữ liệu không hợp lệ", "Vui lòng nhập đầy đủ thông tin cho tất cả các trường.")
            return
        
        try:
            # Chuyển năm và các giá trị khác thành số
            year = int(year)
            award = int(award)
            nomination = int(nomination)
        except ValueError:
            messagebox.showerror("Dữ liệu không hợp lệ", "Năm, giải thưởng và số đề cử phải là số nguyên.")
            return

        # Lưu phim mới vào file CSV
        add_movie("Data/oscar.csv", film, year, award, nomination)

        # Sau khi lưu, xóa nội dung trong các ô nhập
        film_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        award_entry.delete(0, tk.END)
        nomination_entry.delete(0, tk.END)

        # Hiển thị thông báo thành công với chủ đề Oscar
        messagebox.showinfo("Phim mới đã được thêm", f"Phim {film} đã được thêm vào danh sách phim Oscar.")

    # Nút lưu phim mới
    save_button = tk.Button(main_frame, text="Save", command=save_new_movie, bg="#FFD700", fg="#1E1E1E", font=button_font, width=12)
    save_button.pack(pady=20)


def delete_movie():
    # Xóa các widget hiện có trong display_area
    for widget in display_area.winfo_children():
        widget.destroy()

    # Tạo frame hiển thị và frame kết quả
    delete_frame = tk.Frame(display_area, bg="#333333", width=display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0)
    delete_frame.pack(side="left", fill="y")
    delete_frame.pack_propagate(False)

    result_frame = tk.Frame(display_area, bg="#1E1E1E", width=3 * display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0)
    result_frame.pack(side="right", fill="both", expand=True)
    result_frame.pack_propagate(False)

    # Tiêu đề của chức năng xóa phim
    delete_title = tk.Label(delete_frame, text="Delete Movie", font=title_font, fg="#FFD700", bg="#333333")
    delete_title.pack(pady=(10, 15))

    # Biến lưu trữ nút delete
    delete_button = tk.Button(delete_frame, text="Delete", bg="#FFD700", fg="#1E1E1E", font=button_font, width=12)
    delete_button.pack(pady=20)

    # Hàm hiển thị dữ liệu phim từ file CSV
    def display_data():
        # Đọc dữ liệu từ file CSV
        data = pd.read_csv("Data/oscar.csv")

        # Xóa các widget cũ trong result_frame
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Tạo Treeview hiển thị dữ liệu
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background="#333333",
                        foreground="#FFFFFF",
                        rowheight=25,
                        fieldbackground="#333333")
        style.map("Custom.Treeview", background=[("selected", "#FFD700")], foreground=[("selected", "#1E1E1E")])

        columns = data.columns.tolist()
        tree = ttk.Treeview(result_frame, columns=columns, show="headings", style="Custom.Treeview", selectmode = "extended")

        # Thiết lập tiêu đề cột
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=150)

        # Thêm dữ liệu vào Treeview
        for _, row in data.iterrows():
            tree.insert("", "end", values=row.tolist())

        tree.pack(side="left", fill="both", expand=True)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

        # Hàm xác nhận xóa phim
        def confirm_delete():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "No movie selected. Please select a movie to delete.")
                return

            # Lấy danh sách của các phim được chọn
            selected_movies = [tree.item(item)["values"][1] for item in selected_item]
            movie_name = "/n".join(selected_movies)

            # Xác nhận xóa
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{movie_name}'?")
            if confirm:
                # Xóa dữ liệu khỏi DataFrame
                for movie_name in selected_movies:
                    data.drop(data[data["Film"] == movie_name].index, inplace=True)
                # Cập nhật lại cột ID
                data.reset_index(drop=True, inplace=True)
                data["ID"] = data.index + 1  # ID bắt đầu từ 1
                # Cập nhật lại file CSV
                data.to_csv("Data/oscar.csv", index=False)
                # Hiển thị thông báo thành công
                messagebox.showinfo("Success", f"'{movie_name}' has been deleted successfully.")
                # Tải lại dữ liệu sau khi xóa
                display_data()

        # Gán lại sự kiện cho nút delete
        delete_button.config(command=confirm_delete)

    # Hiển thị dữ liệu ban đầu
    display_data()

def edit_movie():
    print("Edit")

def search_movie():
    # Xóa các widget hiện có trong display_area
    for widget in display_area.winfo_children():
        widget.destroy()

    # Tạo frame tìm kiếm bên trái, chiếm 1/4 diện tích display_area, không có viền
    search_frame = tk.Frame(display_area, bg="#333333", width=display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0)
    search_frame.pack(side="left", fill="y")
    search_frame.pack_propagate(False)

    # Tạo frame kết quả bên phải, chiếm 3/4 diện tích display_area, không có viền
    result_frame = tk.Frame(display_area, bg="#1E1E1E", width=3 * display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0)
    result_frame.pack(side="right", fill="both", expand=True)
    result_frame.pack_propagate(False)

    # Thêm tiêu đề cho khung tìm kiếm
    search_title = tk.Label(search_frame, text="Search Movie", font=title_font, fg="#FFD700", bg="#333333")
    search_title.pack(pady=(10, 15))

    # Ô nhập liệu cho tìm kiếm phim
    search_label = tk.Label(search_frame, text="Enter movie name:", font=button_font, fg="#FFD700", bg="#333333")
    search_label.pack(pady=5)
    
    search_entry = tk.Entry(search_frame, width=25, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700")
    search_entry.pack(pady=5)

    # Frame hiển thị chi tiết bản ghi
    detail_frame = tk.Frame(search_frame, bg="#333333")
    detail_frame.pack(pady=(10, 0))

    # Hàm tải và hiển thị dữ liệu toàn bộ hoặc kết quả tìm kiếm
    def display_data(data):
        # Xóa các widget cũ trong result_frame
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Tạo Treeview để hiển thị dữ liệu dạng bảng với màu sắc tùy chỉnh
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#333333", foreground="#FFFFFF", rowheight=25, fieldbackground="#333333")
        style.map("Custom.Treeview", background=[("selected", "#FFD700")], foreground=[("selected", "#1E1E1E")])

        # Khởi tạo Treeview
        columns = data.columns.tolist()
        tree = ttk.Treeview(result_frame, columns=columns, show="headings", style="Custom.Treeview")

        # Thiết lập tiêu đề cho mỗi cột với kích thước chữ lớn
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=150)  # Đặt độ rộng cột tùy ý

        # Thêm dữ liệu vào Treeview
        for _, row in data.iterrows():
            tree.insert("", "end", values=row.tolist())

        # Gói Treeview vào result_frame
        tree.pack(side="left", fill="both", expand=True)

        # Tạo thanh cuộn dọc bên phải của tree
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

        # Gán sự kiện click vào dòng để hiển thị chi tiết nếu chỉ có 1 kết quả
        def on_select(event):
            selected_item = tree.selection()
            if selected_item and len(selected_item) == 1:
                selected_record = data.iloc[int(selected_item[0])].to_dict()
                show_record_details(selected_record)
        tree.bind("<<TreeviewSelect>>", on_select)

    # Hàm hiển thị chi tiết bản ghi
    def show_record_details(record):
        # Xóa các widget trong detail_frame
        for widget in detail_frame.winfo_children():
            widget.destroy()

        # Hiển thị dữ liệu theo từng hàng
        for column, value in record.items():
            label = tk.Label(detail_frame, text=f"{column}: {value}", bg="#333333", fg="#FFD700", font=button_font)
            label.pack(anchor="w")

    # Hàm tìm kiếm phim khi nhấn Enter hoặc khi thay đổi ký tự
    def perform_search(event=None):
        movie_name = search_entry.get().strip()
        data = pd.read_csv("Data/oscar.csv")

        # Lọc chính xác theo tên phim
        filtered_data = data[data["Film"].str.contains(movie_name, case=False, na=False)]
        
        # Hiển thị dữ liệu tìm thấy
        display_data(filtered_data)

        # Nếu tìm thấy duy nhất 1 kết quả và nhấn Enter, hiển thị chi tiết bản ghi
        if len(filtered_data) == 1 and event.keysym == "Return":
            show_record_details(filtered_data.iloc[0].to_dict())

    # Gán sự kiện nhấn Enter và KeyRelease cho ô nhập liệu
    search_entry.bind("<Return>", perform_search)
    search_entry.bind("<KeyRelease>", perform_search)


buttons = [
    ("Load Data", lambda: load_data_into_table(display_area, 'Data/oscar.csv')),
    ("Add Movie", add_movie_ui),
    ("Delete Movie", delete_movie),
    ("Edit Movie", edit_movie),
    ("Search Movie", search_movie),
    ("Chart", print_chart)
]

# Thêm nút vào giao diện
for text, command in buttons:
    button = tk.Button(button_frame, text=text, font=button_font, bg="#2E2E2E", fg="#FFD700", width=15, height=2, bd=0, relief="solid", cursor="hand2", activebackground="#FFD700", activeforeground="#1E1E1E", command=command)
    button.pack(pady=5, fill="x")
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Khu vực hiển thị nội dung chính
display_area = tk.Frame(window, bg="#333333", relief="solid", borderwidth=1)
display_area.pack(pady=10, padx=10, fill="both", expand=True)

# Hiển thị hình ảnh
image = Image.open('Data/OscarImage.png')
image_width, image_height = image.size
window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()

max_width = window_width // 3
max_height = window_height // 3

aspect_ratio = image_width / image_height
if image_width > max_width or image_height > max_height:
    if image_width / max_width > image_height / max_height:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
else:
    new_width, new_height = image_width, image_height

image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
image_tk = ImageTk.PhotoImage(image_resized)
image_label = tk.Label(window, image=image_tk, bg='#1E1E1E')
image_label.place(x=0, rely=1, anchor="sw")

window.mainloop()