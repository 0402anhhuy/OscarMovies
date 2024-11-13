import sys
import os
import tkinter as tk
from tkinter import font, simpledialog, ttk
from tkinter import messagebox  # Thêm import để sử dụng messagebox
import pandas as pd
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Service.LoadData import load_data
from Service.AddFilm import add_movie_data 

# Khởi tạo giao diện chính
window = tk.Tk()
window.title("Oscar Movie")
window.configure(bg='#1E1E1E')
window.state("zoomed")

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

def add_movie():
    # Xóa các widget hiện có trong display_area
    for widget in display_area.winfo_children():
        widget.destroy()
    
    # Tiêu đề giao diện thêm phim mới
    title_label = tk.Label(display_area, text="Add New Movie", font=title_font, fg="#FFD700", bg="#333333")
    title_label.pack(pady=(200, 15), padx=(50, 15))

    # Tạo một frame chứa toàn bộ các ô nhập liệu và nút
    input_frame = tk.Frame(display_area, bg="#333333")
    input_frame.pack(pady=0)
    input_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Hàm tạo hàng nhập liệu và gán key binding cho Enter
    def create_input_row(parent, label_text, next_entry=None):
        row_frame = tk.Frame(parent, bg="#333333")
        row_frame.pack(fill="x", pady=8)

        label = tk.Label(row_frame, text=label_text, font=button_font, fg="#FFD700", bg="#333333")
        label.pack(side="left", padx=(0, 15))

        entry = tk.Entry(row_frame, width=45, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700")
        entry.pack(side="left", fill="x", expand=True)

        # Bind the Enter key to focus on the next entry field
        if next_entry:
            entry.bind("<Return>", lambda event, next_field=next_entry: next_field.focus_set())
        
        return entry

    # Tạo các trường nhập liệu và chỉ định trường kế tiếp khi nhấn Enter
    film_entry = create_input_row(input_frame, "Film:", next_entry=None)
    year_entry = create_input_row(input_frame, "Year:", next_entry=film_entry)
    award_entry = create_input_row(input_frame, "Award:", next_entry=year_entry)
    nomination_entry = create_input_row(input_frame, "Nomination:", next_entry=award_entry)

    # Hàm lưu dữ liệu phim mới
    def save_new_movie():
        # Lấy dữ liệu từ các trường nhập liệu
        film = film_entry.get()
        year = year_entry.get()
        award = award_entry.get()
        nomination = nomination_entry.get()

        # Kiểm tra nếu các trường dữ liệu bắt buộc không được bỏ trống, trừ khi giải thưởng = 0
        if not film or not year or not nomination or (award != '0' and not award):
            messagebox.showerror("Input Error", "All fields must be filled except for the Award (if it's 0).")
            return
        
        try:
            # Chuyển năm và các giá trị khác thành số
            year = int(year)
            award = int(award)
            nomination = int(nomination)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for Year, Award, and Nomination.")
            return

        # Lưu phim mới vào file CSV
        add_movie_data("ProjectCuoiKy/Data/oscar.csv", film, year, award, nomination)

        # Sau khi lưu, xóa nội dung trong các ô nhập
        film_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        award_entry.delete(0, tk.END)
        nomination_entry.delete(0, tk.END)

        # Hiển thị thông báo thành công với chủ đề Oscar
        messagebox.showinfo("Oscar Success", f"'{film}' has been added to the Oscar list successfully!")

    # Nút lưu phim mới
    save_button = tk.Button(input_frame, text="Save", command=save_new_movie, bg="#FFD700", fg="#1E1E1E", font=button_font, width=12)
    save_button.pack(pady=20)

    # Bind the Enter key on the last field to trigger the Save function
    nomination_entry.bind("<Return>", lambda event: save_new_movie())




def delete_movie():
    print("Delete")

def edit_movie():
    print("Edit")

def search_movie():
    print("Search")

buttons = [
    ("Load Data", lambda: load_data(display_area)),
    ("Add Movie", add_movie),
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
image = Image.open('ProjectCuoiKy/Data/OscarImage.png')
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
