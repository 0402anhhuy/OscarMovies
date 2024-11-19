import pandas as pd
from tkinter import messagebox
from Model.LoadDataModel import load_data

# Hàm xóa dữ liệu phim được chọn
def delete_movie_data(file_path_csv, selected_movies, display_data):
    # Kiểm tra nếu không có phim nào được chọn
    if not selected_movies:
        messagebox.showerror("Error", "No movie selected. Please select a movie to delete.")
        return  # Thoát khỏi hàm nếu không có phim nào được chọn

    # Lấy danh sách tên các phim được chọn từ `selected_movies`
    movie_names = [movie["values"][1] for movie in selected_movies]
    # Ghép các tên phim thành chuỗi để hiển thị trong thông báo xác nhận
    movie_name_str = "\n".join(movie_names)

    # Hiển thị hộp thoại xác nhận trước khi xóa các phim được chọn
    confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to permanently remove:\n{movie_name_str}?")
    if confirm:  # Nếu người dùng chọn "Yes" trong hộp thoại xác nhận
        # Đọc dữ liệu từ file CSV
        data = load_data(file_path_csv)

        # Xóa từng phim có tên trong danh sách `movie_names`
        for movie_name in movie_names:
            # Tìm các dòng có tên phim khớp và xóa chúng
            data.drop(data[data["Film"] == movie_name].index, inplace=True)

        # Đặt lại chỉ số index cho dataframe sau khi xóa
        data.reset_index(drop=True, inplace=True)
        # Cập nhật cột ID để đảm bảo dữ liệu đồng bộ
        data["ID"] = data.index + 1

        # Ghi dữ liệu đã xóa vào file CSV
        data.to_csv(file_path_csv, index=False)
        
        # Hiển thị thông báo xóa thành công
        messagebox.showinfo("Success", f"'{movie_name_str}' has been deleted successfully.")
        
        # Cập nhật dữ liệu hiển thị trên giao diện sau khi xóa
        display_data(data)
