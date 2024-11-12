import sys
import os
import tkinter as tk
from tkinter import font, simpledialog, ttk
import pandas as pd
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Service.LoadData import load_data

window = tk.Tk()
window.title("Oscar Movie")
window.configure(bg='#1E1E1E')
window.state("zoomed")

title_font = font.Font(family="Helvetica", size=22, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")

title_label = tk.Label(window, text="OSCAR AWARD WINNER", font=title_font, fg="#FFD700", bg="#1E1E1E")
title_label.pack(pady=10, anchor="center")

button_frame = tk.Frame(window, bg='#1E1E1E')
button_frame.pack(side="left", fill="y", padx=20, pady=10, expand=False)

def on_enter(e):
    e.widget['bg'] = "#FFD700"

def on_leave(e):
    e.widget['bg'] = "#2E2E2E"

def print_chart():
    print("Chart")

def add_movie():
    print("Add")

def delete_movie():
    print("Delete")

def edit_movie():
    print("Edit")

def search_movie():
    print("Search")

buttons = [
    ("Load Data", lambda: load_data(display_area)),
    ("Add", add_movie),
    ("Delete", delete_movie),
    ("Edit", edit_movie),
    ("Search", search_movie),
    ("Chart", print_chart)
]

for text, command in buttons:
    button = tk.Button(button_frame, text=text, font=button_font, bg="#2E2E2E", fg="#FFD700",
                    width=15, height=2, bd=0, relief="solid", cursor="hand2",
                    activebackground="#FFD700", activeforeground="#1E1E1E", command=command)
    button.pack(pady=5, fill="x")
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

display_area = tk.Frame(window, bg="#333333", relief="solid", borderwidth=1)
display_area.pack(pady=10, padx=10, fill="both", expand=True)

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
