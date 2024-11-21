from tkinter import messagebox
from Model.LoadDataModel import load_data

file_path_csv = "ProjectCuoiKy/Data/oscar.csv"

def save_changes_to_csv(film_name, new_award, new_nomination):
    try:
        new_award = int(new_award)
        new_nomination = int(new_nomination)
    except ValueError:
        messagebox.showerror("Invalid Input", "Award and Nomination must be integers.")
        return

    data = load_data(file_path_csv)
    data.loc[data['Film'] == film_name, 'Award'] = new_award
    data.loc[data['Film'] == film_name, 'Nomination'] = new_nomination
    data.to_csv(file_path_csv, index=False)
    messagebox.showinfo("Success", f"Updated {film_name} successfully.")