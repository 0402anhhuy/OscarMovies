import pandas as pd
from tkinter import messagebox
from Model.LoadDataModel import load_data

def delete_movie_data(file_path_csv, selected_movies, display_data):
    if not selected_movies:
        messagebox.showerror("Error", "No movie selected. Please select a movie to delete.")
        return

    movie_names = [movie["values"][1] for movie in selected_movies]
    movie_name_str = "\n".join(movie_names)

    confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to permanently remove:\n{movie_name_str}?")
    if confirm:
        data = load_data(file_path_csv)

        for movie_name in movie_names:
            data.drop(data[data["Film"] == movie_name].index, inplace=True)

        data.reset_index(drop=True, inplace=True)
        data["ID"] = data.index + 1
        data.to_csv(file_path_csv, index=False)
        messagebox.showinfo("Success", f"'{movie_name_str}' has been deleted successfully.")
        display_data(data)
