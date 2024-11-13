import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Hàm vẽ biểu đồ cột
def draw_bar_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#333333")  # Đặt nền màu xám
    award_data.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

    ax.set_title('Tổng số giải thưởng theo năm', fontsize=14, color="White")  # Màu vàng
    ax.set_xlabel('Năm', fontsize=12, color="White")  # Màu vàng
    ax.set_ylabel('Số Giải Thưởng', fontsize=12, color="White")  # Màu vàng
    ax.tick_params(axis='x', colors="White")  # Màu vàng
    ax.tick_params(axis='y', colors="White")  # Màu vàng
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Hàm vẽ biểu đồ tròn
def draw_pie_chart(data, display_area):

    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(8, 8))
    award_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax)

    ax.set_title('Tỷ lệ giải thưởng theo năm', fontsize=14)
    ax.set_ylabel('')  # Xóa nhãn trục Y

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Hàm vẽ biểu đồ đường
def draw_line_chart(data, display_area):

    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    award_data.plot(kind='line', marker='o', color='green', ax=ax)

    ax.set_title('Sự thay đổi số lượng giải thưởng theo năm', fontsize=14)
    ax.set_xlabel('Năm', fontsize=12)
    ax.set_ylabel('Số Giải Thưởng', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
