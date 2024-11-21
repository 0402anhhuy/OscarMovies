import pandas as pd

def load_data(file_path_csv):
    try:
        data = pd.read_csv(file_path_csv)
        return data
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu!")
        return None