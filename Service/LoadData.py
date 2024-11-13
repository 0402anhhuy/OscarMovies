import pandas as pd
from tkinter import ttk

def load_data(display_area):
    file_path = 'ProjectCuoiKy/Data/oscar.csv'
    try:
        # Đọc dữ liệu từ file CSV
        data = pd.read_csv(file_path)
        
        # Xóa các widget hiện có trong display_area
        for widget in display_area.winfo_children():
            widget.destroy()
    
        # Tạo Treeview để hiển thị dữ liệu
        tree = ttk.Treeview(display_area, show="headings", style="mystyle.Treeview")
        tree.pack(side="left", fill="both", expand=True)
        
        # Cấu hình các cột trong Treeview
        tree["columns"] = list(data.columns)
        
        # Tạo tiêu đề và các cột
        for col in data.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=150, anchor="center")
        
        # Thêm dữ liệu vào Treeview
        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))
        
        # Thêm thanh cuộn dọc
        y_scroll = ttk.Scrollbar(display_area, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.pack(side="right", fill="y")
        
        # Tùy chỉnh kiểu cho Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", 
                        background="#333333", 
                        foreground="white", 
                        rowheight=30, 
                        fieldbackground="#333333",
                        font=("Segoe UI", 12))  # Điều chỉnh kích thước font chữ
        style.map('mystyle.Treeview', background=[('selected', '#444444')])
        
        # Tùy chỉnh font chữ cho tiêu đề (heading)
        style.configure("mystyle.Treeview.Heading", font=("Segoe UI", 14, "bold"))

    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu!")
    except pd.errors.EmptyDataError:
        print("Dữ liệu trong file rỗng!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
