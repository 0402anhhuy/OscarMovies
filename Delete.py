import sys
import os
import tkinter as tk
from tkinter import font, ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

buttons = [
    # ("Load Data", lambda: load_data(display_area)),
    # ("Add Movie", add_movie),
    ("Delete Movie", delete_movie),
    # ("Edit Movie", edit_movie),
    # ("Search Movie", search_movie),
    # ("Chart", print_chart)
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