from tkinter import messagebox
from Model.LoadDataModel import load_data

# Hàm xóa dữ liệu phim được chọn
def delete_movie_data(file_path_csv, selected_movies, display_data):
    # Lấy danh sách các phim được chọn từ `selected_movies`
    if len(selected_movies) == 1:  # Chỉ xử lý nếu có đúng một phim được chọn
        movie_name = selected_movies[0]["values"][1]  # Lấy tên phim từ bản ghi đầu tiên
        # Hiển thị hộp thoại xác nhận
        confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to permanently remove '{movie_name}'?")
        if confirm:  # Nếu người dùng xác nhận
            # Đọc dữ liệu từ file CSV
            data = load_data(file_path_csv)

            # Tìm và xóa bản ghi trong DataFrame
            indices = data[data["Film"] == movie_name].index
            if len(indices) > 0:
                data.drop(indices[0], inplace=True)  # Chỉ xóa bản ghi đầu tiên tìm thấy
                messagebox.showinfo("Success", f"'{movie_name}' has been deleted successfully.")
            else:
                messagebox.showwarning("Not Found", f"'{movie_name}' not found in the database.")
    else:
        messagebox.showwarning("Invalid Selection", "Please select exactly one record to delete.")

    # Đặt lại chỉ số index cho dataframe sau khi xóa
    data.reset_index(drop=True, inplace=True)
    # Cập nhật cột ID để đảm bảo dữ liệu đồng bộ
    data["ID"] = data.index + 1

    # Ghi dữ liệu đã xóa vào file CSV
    data.to_csv(file_path_csv, index=False)
        
    # Cập nhật dữ liệu hiển thị trên giao diện sau khi xóa
    display_data(data)
