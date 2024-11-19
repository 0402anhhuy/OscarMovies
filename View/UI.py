import sys, os, re
import tkinter as tk
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tkinter import font, ttk, messagebox, Button
from functools import partial
from PIL import Image, ImageTk
from Controller.AddMovieController import add_movie_data
from Controller.DeleteMovieController import delete_movie_data
from Controller.EditMovieController import save_changes_to_csv
from Controller.ChartMovieController import draw_bar_chart, draw_pie_chart, draw_line_chart
from Model.LoadDataModel import load_data

file_path_csv = "ProjectCuoiKy/Data/oscar.csv"
file_path_image = "ProjectCuoiKy/Data/OscarImage.png"

# Hàm tạo cửa sổ chính
def mainWindow():
    window = tk.Tk()
    window.title("Oscar Movie")
    window.configure(bg='#1E1E1E')
    window.state("zoomed")
    return window

def display_paginated_data(tree, data, records_per_page):
    current_page = 1
    total_pages = (len(data) - 1) // records_per_page + 1
    paginated_data = data.copy()

    # Hàm cập nhật dữ liệu trên giao diện
    def update_treeview(page):
        clear_tree(tree)
        start_idx = (page - 1) * records_per_page
        end_idx = start_idx + records_per_page
        current_page_data = paginated_data.iloc[start_idx:end_idx]

        for _, row in current_page_data.iterrows():
            tree.insert("", "end", values=list(row))

    # Hàm xử lý nút Previous
    def previous_page():
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_treeview(current_page)
            page_label.config(text=f"Page {current_page} of {total_pages}")

    # Hàm xử lý nút Next
    def next_page():
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_treeview(current_page)
            page_label.config(text=f"Page {current_page} of {total_pages}")

    # Cập nhật dữ liệu lần đầu
    update_treeview(current_page)

    # Frame chứa nút điều hướng
    nav_frame = createFrame(tree.master, bg="#333333", fill="x", pady=(10, 0))

    # Nút Previous
    prev_button = createButton(nav_frame, text="Previous", command=previous_page, bg="#FF6347", fg="white", font=("Helvetica", 10, "bold"), width=10, side="left", padx=(10, 5), pady=5)

    # Nhãn hiển thị trang hiện tại
    page_label = createLabel(nav_frame, text=f"Page {current_page} of {total_pages}", font=("Helvetica", 10), bg="#333333", fg="white", side="left", padx=5, pady=5)
    
    # Nút Next
    next_button = createButton(nav_frame, text="Next", command=next_page, bg="#FF6347", fg="white", font=("Helvetica", 10, "bold"), width=10, side="left", padx=5, pady=5)


def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)

# Hàm tạo frame
def createFrame(window, bg=None, side=None, fill=None, padx=None, pady=None, expand=None, width=None, height=None, relx=None, rely=None, anchor=None, bd=0, highlightthickness=0, propagate=None, relief=None, borderwidth=None):
    template_frame = tk.Frame(window, bg=bg, width=width, height=height, bd=bd, highlightthickness=highlightthickness, relief=relief, borderwidth=borderwidth)
    if relx is not None and rely is not None:
        template_frame.place(relx=relx, rely=rely, anchor=anchor)
        template_frame.pack_propagate(propagate)
    else:
        template_frame.pack(side=side, fill=fill, padx=padx, pady=pady, expand=expand)
        if propagate is not None:
            template_frame.pack_propagate(propagate)  
    return template_frame

# Hàm tạo font
def createFont(size, weight):
    template_font = font.Font(family="Helvetica", size=size, weight=weight)
    return template_font

# Hàm tạo nhãn
def createLabel(window, text=None, font=None, fg=None, bg=None, padx=0, pady=0, side=None, fill=None, anchor=None, row=None, column=None, columnspan=None, sticky=None, use_grid=False,):
    template_label = tk.Label(window, text=text, font=font, fg=fg, bg=bg)
    if use_grid:
        template_label.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
    else:
        template_label.pack(padx=padx, pady=pady, side=side, fill=fill, anchor=anchor)
    return template_label

# Hàm tạo nút
def createButton(window, text, command=None, width=None, height=None, borderwidth=1, relief="flat", bg=None, fg=None, font=None, side=None, anchor=None, row=None, column=None, padx=0, pady=0, sticky=None, expand=False, use_grid=False):
    button = tk.Button(window, text=text, command=command, width=width, height=height, borderwidth=borderwidth, relief=relief, bg=bg, fg=fg, font=font)
    if use_grid:
        button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    else:
        button.pack(side=side, anchor=anchor, padx=padx, pady=pady, expand=expand)
    return button

# Hàm tạo ô nhập liệu
def createEntry(parent, width=None, bg=None, fg=None, font=None, insertbackground=None, side=None, fill=None, expand=None, ipady=None, padx=None, pady=None, row=None, column=None, use_grid=False):
    template_entry = tk.Entry(parent, width=width, bg=bg, fg=fg, font=font, insertbackground=insertbackground)
    if use_grid:
        template_entry.grid(row=row, column=column, padx=padx, pady=pady)
    else:
        template_entry.pack(side=side, fill=fill, expand=expand, ipady=ipady)
    return template_entry

# Hàm tạo Treeview để hiển thị dữ liệu từ một DataFrame
def createTreeview(window, data, style_name="Custom.Treeview", rowheight=30, bg="#333333", fg="#FFFFFF", selected_bg="#FFD700", selected_fg="#1E1E1E", heading_font=("Helvetica", 11, "bold"), row_font=("Helvetica", 11), selectmode="extended"):
    # Tạo và cấu hình style cho Treeview
    style = ttk.Style()
    style.configure(style_name, background=bg, foreground=fg, rowheight=rowheight, fieldbackground=bg, font=row_font)
    style.map(style_name, background=[("selected", selected_bg)], foreground=[("selected", selected_fg)])
    style.configure(f"{style_name}.Heading", font=heading_font)

    # Tạo Treeview với cột được truyền trực tiếp
    tree = ttk.Treeview(window, columns=list(data.columns), show="headings", style=style_name, selectmode=selectmode)
    tree.pack(side="left", fill="both", expand=True)

    # Thiết lập tiêu đề và cấu hình cột
    for col in data.columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")

    # Thêm dữ liệu vào Treeview
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    return tree

# Hàm xử lý sự kiện khi rê chuột vào nút
def onEnter(e):
    e.widget['bg'] = "#FFD700"

def onLeave(e):
    e.widget['bg'] = "#2E2E2E"

# Hàm xóa các widget con của một widget
def clearWidgets(widget):
    for child in widget.winfo_children():
        child.destroy()

# Thêm thanh cuộn dọc vào cửa sổ
def themThanhCuonDoc(parent, tree):
    y_scroll = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scroll.set)
    y_scroll.pack(side="right", fill="y")

window = mainWindow()

# Tạo font cho tiêu đề và nút
title_font = createFont(size=20, weight="bold")
button_font = createFont(size=10, weight="bold")

# Tạo tiêu đề cho cửa sổ
title_label = createLabel(window, text="Oscar Awards Movie", font=title_font, fg="#FFD700", bg="#1E1E1E", padx=(190, 10), pady=10)

# Tạo frame chứa các nút chức năng
button_frame = createFrame(window, bg="#1E1E1E", side="left", fill="y", padx=20, pady=10, expand=False)


def loadDataUI():
    clearWidgets(display_area)
    data = load_data(file_path_csv)
    if data is not None:
        tree = createTreeview(display_area, data)
        display_paginated_data(tree, data, 50)
        themThanhCuonDoc(display_area, tree)
        clean_button = createButton(display_area, text="Clean Data", command=partial(cleanData, file_path_csv, display_area), width=10, height=2, borderwidth=1, relief="raised", bg="#FF6347", fg="white", font=("Helvetica", 10, "bold"), side="top", anchor="w", padx=10, pady=8)

def cleanData(file_path_csv, display_area):
    data = load_data(file_path_csv)
    if data is not None:
        # Loại bỏ các bản ghi trùng lặp theo tên phim (giữ lại bản ghi đầu tiên)
        data.drop_duplicates(subset="Film", inplace=True)
        
        # Xử lý các năm bị lỗi (ít hơn 4 chữ số)
        def KiemTraNamHopLe(year):
            return 1000 <= year <= 9999
        
        data = data[data['Year'].apply(KiemTraNamHopLe)]
        
        # Loại bỏ các ký tự đặc biệt trong tên phim
        def KiemTraTenMovieHopLe(film_name):
            return bool(re.match(r'^[A-Za-z0-9\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ\s]+$', str(film_name)))
        
        data = data[data['Film'].apply(KiemTraTenMovieHopLe)]
        
        # Ghi lại dữ liệu đã được dọn dẹp vào file CSV
        data.reset_index(drop=True, inplace=True)
        data["ID"] = data.index + 1
        data.to_csv(file_path_csv, index=False)
        loadDataUI()
        
        messagebox.showinfo("Success", "Data has been cleaned and reloaded successfully.")

def addMovie():
    clearWidgets(display_area)

    # Frame hiển thị giao diện thêm phim mới
    main_frame = createFrame(display_area, bg="#333333", width=800, height=500, relx=0.5, rely=0.5, anchor="center", propagate=False)
    
    title_label = createLabel(main_frame, text="Add New Movie", font=title_font, fg="#FFD700", bg="#333333", padx=(50, 15), pady=(0, 15))

    # Hàm tạo hàng nhập liệu
    def create_input_row(parent, label_text):
        row_frame = createFrame(parent, bg="#333333", fill="x", pady=8)
        label = createLabel(row_frame, text=label_text, font=button_font, fg="#FFD700", bg="#333333", padx=(0, 15), side="left")
        entry = createEntry(row_frame, width=45, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700", side="left", fill="x", expand=True)
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
            messagebox.showerror("Invalid Data", "Please enter complete information for all fields.")
            return
        try:
            year = int(year)
            award = int(award)
            nomination = int(nomination)
        except ValueError:
            messagebox.showerror("Invalid Data", "Year, award, and nomination count must be integers.")
            return

        add_movie_data(file_path_csv, film, year, award, nomination)

        # Xóa dữ liệu trong các trường nhập liệu
        film_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        award_entry.delete(0, tk.END)
        nomination_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"The movie '{film}' has been successfully added to the Oscar movie list.")

    save_button = createButton(main_frame, text="Save", command=save_new_movie, fg="#1E1E1E", bg="#FFD700", font=button_font, width=12, pady=20)


def delete_movie():
    clearWidgets(display_area)

    # Frame hiển thị chức năng xóa phim
    delete_frame = createFrame(display_area, bg="#333333", width=display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0, side="left", fill="y", propagate=False)

    # Frame hiển thị kết quả
    result_frame = createFrame(display_area, bg="#1E1E1E", width=3 * display_area.winfo_width() // 4, height=display_area.winfo_height(), bd=0, highlightthickness=0, side="right", fill="both", expand=True, propagate=False)
    
    # Tiêu đề của chức năng xóa phim
    delete_title = createLabel(delete_frame, text="Delete Movie", font=title_font, fg="#FFD700", bg="#333333", pady=(10, 15))

    # Biến lưu trữ nút delete
    delete_button = createButton(delete_frame, text="Delete", bg="#FFD700", fg="#1E1E1E", font=button_font, width=12, pady=20)

    # Hàm hiển thị dữ liệu phim từ file CSV
    def display_data(data=None):
        if data is None:
            data = load_data(file_path_csv)

        clearWidgets(result_frame)
        tree = createTreeview(result_frame, data)
        themThanhCuonDoc(result_frame, tree)

        # Hàm xác nhận xóa phim
        def confirm_delete():
            selected_items = tree.selection()
            selected_movies = [tree.item(item) for item in selected_items]
            delete_movie_data(file_path_csv, selected_movies, display_data)

        # Gán lại sự kiện cho nút delete
        delete_button.config(command=confirm_delete)

    display_data()


def edit_movie():
    clearWidgets(display_area)

    # Frame hiển thị chức năng tìm kiếm phim
    edit_frame = createFrame(display_area, bg="#333333", width=display_area.winfo_width() // 4, height=display_area.winfo_height(), side="left", fill="y", propagate=False)

    # Frame hiển thị kết quả
    result_edit_frame = createFrame(display_area, bg="#1E1E1E", width=3 * display_area.winfo_width() // 4, height=display_area.winfo_height(), side="right", fill="both", expand=True, propagate=False)

    # Tiêu đề của chức năng tìm kiếm phim
    edit_title = createLabel(edit_frame, text="Edit Movie", font=title_font, fg="#FFD700", bg="#333333", pady=(10, 15))

    # Frame chứa trường nhập liệu tìm kiếm
    edit_input_frame = createFrame(edit_frame, bg="#333333", pady=5)

    # Nhãn nhập liệu tìm kiếm
    edit_label = createLabel(edit_input_frame, text="Enter name:", font=button_font, fg="#FFD700", bg="#333333", side="left", padx=(0, 5))

    # Ô nhập liệu tìm kiếm
    edit_entry = createEntry(edit_input_frame, 20, "#2E2E2E", "#FFD700", button_font, "#FFD700", side="left", fill="x", expand=True, ipady=3)

    # Clear button (x)
    clear_button = createButton(edit_input_frame, text="x", command=lambda: clear_search(), font=("Helvetica", 10, "bold"), bg="#FFD700", fg="#333333", width=2, height=1)

    # Frame hiển thị chi tiết bản ghi
    detail_frame = createFrame(edit_frame, bg="#333333", pady=(10, 0))

    # Khung chứa các trường nhập liệu (award và nomination), ẩn mặc định
    center_frame = createFrame(edit_frame, bg="#333333", pady=10, fill="x")

    # Các trường nhập liệu (award và nomination) trong frame mới
    award_label = createLabel(center_frame, text="Enter Award:", font=button_font, fg="#FFD700", bg="#333333", row=0, column=0, padx=5, pady=5, sticky="w", use_grid=True)

    award_entry = createEntry(center_frame, width=10, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700", row=0, column=1, padx=5, pady=5, use_grid=True)

    nomination_label = createLabel(center_frame, text="Enter Nomination:", font=button_font, fg="#FFD700", bg="#333333", row=1, column=0, padx=5, pady=5, sticky="w", use_grid=True)
    
    nomination_entry = createEntry(center_frame, width=10, bg="#2E2E2E", fg="#FFD700", font=button_font, insertbackground="#FFD700", row=1, column=1, padx=5, pady=5, use_grid=True)

    data = load_data(file_path_csv)
    tree = createTreeview(result_edit_frame, data)

    # Hàm hiển thị dữ liệu từ file CSV
    def display_data(data):
        clearWidgets(result_edit_frame)
        tree = createTreeview(result_edit_frame, data)
        themThanhCuonDoc(result_edit_frame, tree)

        # Hàm hiển thị chi tiết bản ghi
        columns = data.columns.tolist()
        def on_double_click(event):
            selected_item = tree.selection()
            if selected_item:
                item_values = tree.item(selected_item[0], "values")
                selected_record = {columns[i]: item_values[i] for i in range(len(columns))}
                show_record_details(selected_record)

        # Ràng buộc sự kiện double click
        tree.bind("<Double-1>", on_double_click)

    # Hiển thị tất cả dữ liệu mặc định
    display_data(data)

    # Hàm hiển thị chi tiết bản ghi
    def show_record_details(record):
        clearWidgets(detail_frame)
        for column, value in record.items():
            label = createLabel(detail_frame, text=f"{column}: {value}", font=button_font, fg="#FFD700", bg="#333333", anchor="w")
        save_button = createButton(detail_frame, text="Save Changes", command=lambda: save_changes(record['Film']), bg="#FFD700", fg="#1E1E1E", font=button_font, width=12, pady=10)

    def save_changes(film_name):
        new_award = award_entry.get()
        new_nomination = nomination_entry.get()
        save_changes_to_csv(film_name, new_award, new_nomination)
        perform_search()

    # Function to perform search
    def perform_search(event=None):
        movie_name = edit_entry.get().strip()
        data = load_data(file_path_csv)

        filtered_data = data[data["Film"].str.contains(movie_name, case=False, na=False)]
        display_data(filtered_data)

        if len(filtered_data) == 1 and event.keysym == "Return":
            show_record_details(filtered_data.iloc[0].to_dict())

    # Hàm xóa nội dung trong ô tìm kiếm
    def clear_search():
        edit_entry.delete(0, "end")
        award_entry.delete(0, "end")
        nomination_entry.delete(0, "end")
        clearWidgets(detail_frame)

    edit_entry.bind("<Return>", perform_search)
    edit_entry.bind("<KeyRelease>", perform_search)


def search_movie():
    clearWidgets(display_area)

    # Frame hiển thị chức năng tìm kiếm phim
    search_frame = createFrame(display_area, bg="#333333", width=display_area.winfo_width() // 4, height=display_area.winfo_height(), side="left", fill="y", propagate=False)

    # Frame hiển thị kết quả
    result_frame = createFrame(display_area, bg="#1E1E1E", width=3 * display_area.winfo_width() // 4, height=display_area.winfo_height(), side="right", fill="both", expand=True, propagate=False)

    # Tiêu đề của chức năng tìm kiếm phim
    search_title = createLabel(search_frame, text="Search Movie", font=title_font, fg="#FFD700", bg="#333333", pady=(10, 15))

    # Frame chứa trường nhập liệu tìm kiếm
    search_input_frame = createFrame(search_frame, bg="#333333", pady=5)

    # Nhãn nhập liệu tìm kiếm
    search_label = createLabel(search_input_frame, text="Enter name:", font=button_font, fg="#FFD700", bg="#333333", side="left", padx=(0, 5))

    # Ô nhập liệu tìm kiếm
    search_entry = createEntry(search_input_frame, 20, "#2E2E2E", "#FFD700", button_font, "#FFD700", side="left", fill="x", expand=True, ipady=3)

    # Clear button (x)
    clear_button = createButton(search_input_frame, text="x", command=lambda: clear_search(), font=("Helvetica", 10, "bold"), bg="#FFD700", fg="#333333", width=2, height=1)

    # Frame hiển thị chi tiết bản ghi
    detail_frame = createFrame(search_frame, bg="#333333", pady=(10, 0))

    data = load_data(file_path_csv)
    tree = createTreeview(result_frame, data)

    # Function to display data in the result frame
    def display_data(data):
        clearWidgets(result_frame)
        tree = createTreeview(result_frame, data)
        themThanhCuonDoc(result_frame, tree)
        # Function to display record details on double-click
        columns = data.columns.tolist()
        def on_double_click(event):
            selected_item = tree.selection()
            if selected_item:
                item_values = tree.item(selected_item[0], "values")
                selected_record = {columns[i]: item_values[i] for i in range(len(columns))}
                show_record_details(selected_record)

        tree.bind("<Double-1>", on_double_click)

    # Function to display record details
    def show_record_details(record):
        clearWidgets(detail_frame)
        for column, value in record.items():
            label = createLabel(detail_frame, text=f"{column}: {value}", font=button_font, fg="#FFD700", bg="#333333", anchor="w")

    # Function to perform search
    def perform_search(event=None):
        movie_name = search_entry.get().strip()
        data = load_data(file_path_csv)

        filtered_data = data[data["Film"].str.contains(movie_name, case=False, na=False)]
        display_data(filtered_data)

        if len(filtered_data) == 1 and event.keysym == "Return":
            show_record_details(filtered_data.iloc[0].to_dict())

    # Hàm xóa nội dung trong ô tìm kiếm
    def clear_search():
        search_entry.delete(0, "end")
        clearWidgets(detail_frame)

    search_entry.bind("<Return>", perform_search)
    search_entry.bind("<KeyRelease>", perform_search)


def print_chart():
    clearWidgets(display_area)
    data = load_data(file_path_csv)
    data = data.head(100)

    chart_frame = createFrame(display_area, bg="#333333", width=display_area.winfo_width() // 3, height=display_area.winfo_height(), side="left", fill="y", propagate=False)

    # Tạo khung phân cách mỏng ở giữa với màu xám
    separator = createFrame(display_area, bg="#808080", width=1, height=display_area.winfo_height(), side="left", fill="y")

    # Tạo frame kết quả bên phải, chiếm 2/3 diện tích display_area, không có viền
    result_frame = createFrame(display_area, bg="#1E1E1E", width=2 * display_area.winfo_width() // 3, height=display_area.winfo_height(), side="right", fill="both", expand=True, propagate=False)

    # Thêm tiêu đề cho khung biểu đồ và căn giữa
    chart_title = createLabel(chart_frame, text="Chart", font=title_font, fg="#FFD700", bg="#333333", row=0, column=0, columnspan=3, pady=(5, 10), sticky="ew")

    def draw_chart(chart_type):
        clearWidgets(result_frame)

        if chart_type == '1':
            draw_bar_chart(data, result_frame)
        elif chart_type == '2':
            draw_pie_chart(data, result_frame)
        elif chart_type == '3':
            draw_line_chart(data, result_frame)

    button_font = createFont(size=10, weight="bold")

    # Tạo 3 nút cho 3 loại biểu đồ và đưa chúng lên góc trên bên trái của chart_frame
    button1 = createButton(chart_frame, text="Biểu đồ cột", command=lambda: draw_chart('1'), bg="#FFD700", fg="#333333", font=button_font, row=1, column=0, padx=5, pady=5, sticky="ew")

    button2 = createButton(chart_frame, text="Biểu đồ tròn", command=lambda: draw_chart('2'), bg="#FFD700", fg="#333333", font=button_font, row=1, column=1, padx=5, pady=5, sticky="ew")

    button3 = createButton(chart_frame, text="Biểu đồ đường", command=lambda: draw_chart('3'), bg="#FFD700", fg="#333333", font=button_font, row=1, column=2, padx=5, pady=5, sticky="ew")

    # Cấu hình hàng và cột trong chart_frame để đảm bảo các nút gọn gàng ở góc trên bên trái và tiêu đề căn giữa
    chart_frame.grid_rowconfigure(1, weight=0)
    chart_frame.grid_columnconfigure(0, weight=1)
    chart_frame.grid_columnconfigure(1, weight=1)
    chart_frame.grid_columnconfigure(2, weight=1)

buttons = [
    ("Load Data", loadDataUI),
    ("Add Movie", addMovie),
    ("Delete Movie", delete_movie),
    ("Edit Movie", edit_movie),
    ("Search Movie", search_movie),
    ("Chart", print_chart)
]

# Thêm nút vào giao diện
for text, command in buttons:
    button = tk.Button(button_frame, text=text, font=button_font, bg="#2E2E2E", fg="#FFD700", width=15, height=2, bd=0, relief="solid", cursor="hand2", activebackground="#FFD700", activeforeground="#1E1E1E", command=command)
    button.pack(pady=5, fill="x")
    button.bind("<Enter>", onEnter)
    button.bind("<Leave>", onLeave)

# Khu vực hiển thị nội dung chính
display_area = createFrame(window, bg="#333333", relief="solid", borderwidth=1, padx=10, pady=10, fill="both", expand=True)


"""Hiển thị hình ảnh Oscar"""
# Load hình ảnh Oscar từ file
image = Image.open(file_path_image)

# Lấy kích thước hình ảnh
image_width, image_height = image.size

# Lấy kích thước của màn hình
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
