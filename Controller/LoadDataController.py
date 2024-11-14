from tkinter import ttk
from Model.LoadDataModel import load_data

def load_data_into_table(display_area, file_path):
    data = load_data(file_path)
    if data is not None:
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
        style.configure("mystyle.Treeview", background="#333333", foreground="#FFFFFF", rowheight=30, fieldbackground="black", font=("Helvetica", 12))
        style.map('mystyle.Treeview', background=[('selected', '#FFD700')], foreground=[('selected', 'black')])
        style.configure("mystyle.Treeview.Heading", font=("Helvetica", 12, "bold"))