import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_bar_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#333333")  
    award_data.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

    ax.set_title('Total number of awards by year', fontsize=14, color="White") 
    ax.set_xlabel('Years', fontsize=12, color="White") 
    ax.set_ylabel('Award', fontsize=12, color="White")
    ax.tick_params(axis='x', rotation=0, colors="White") 
    ax.tick_params(axis='y', colors="White")  
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def draw_pie_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#333333")
    
    award_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax, textprops={'color': 'white', 'fontsize': 12})

    ax.set_title('Award rate by year', fontsize=14, color="white")
    ax.set_ylabel('')

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def draw_line_chart(data, display_area):
    award_data = data.groupby('Year')['Award'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#333333")
    award_data.plot(kind='line', marker='o', color='green', ax=ax)

    ax.set_title('Change in number of awards by year', fontsize=14, color="White")
    ax.set_xlabel('Year', fontsize=12, color="White")
    ax.set_ylabel('Award', fontsize=12, color="White")
    ax.tick_params(axis='x', rotation=0, colors="White")
    ax.tick_params(axis='y', colors="White")
    plt.tight_layout()

    ax.grid(True, linestyle='--', color='black', alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=display_area)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
