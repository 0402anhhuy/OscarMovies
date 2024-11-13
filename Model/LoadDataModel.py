import pandas as pd

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu!")
    except pd.errors.EmptyDataError:
        print("Dữ liệu trong file rỗng!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    return None