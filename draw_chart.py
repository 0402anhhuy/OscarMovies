import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_bar_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#333333")  
    award_data.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

    ax.set_title('Tổng số giải thưởng theo năm', fontsize=14, color="White") 
    ax.set_xlabel('Năm', fontsize=12, color="White") 
    ax.set_ylabel('Số Giải Thưởng', fontsize=12, color="White")
    ax.tick_params(axis='x', rotation=45, colors="White") 
    ax.tick_params(axis='y', colors="White")  
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def draw_pie_chart(data, display_area):
    # Group data by 'Year' and sum the 'Award' column
    award_data = data.groupby('Year')['Award'].sum()

    # Create the figure and axis with dark background
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#333333")
    
    # Plot the pie chart
    award_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax, textprops={'color': 'white', 'fontsize': 12})

    # Set the title with white font
    ax.set_title('Tỷ lệ giải thưởng theo năm', fontsize=14, color="white")
    ax.set_ylabel('')

    # Add the pie chart to the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def draw_line_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#333333")
    award_data.plot(kind='line', marker='o', color='green', ax=ax)

    ax.set_title('Sự thay đổi số lượng giải thưởng theo năm', fontsize=14, color="White")
    ax.set_xlabel('Năm', fontsize=12, color="White")
    ax.set_ylabel('Số Giải Thưởng', fontsize=12, color="White")
    ax.tick_params(axis='x', rotation=45, colors="White")
    ax.tick_params(axis='y', colors="White")
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

