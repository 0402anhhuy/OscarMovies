# OscarMovies 🎬
OscarMovies là một ứng dụng Python mô phỏng hệ thống quản lý phim đạt giải Oscar. Dự án này được xây dựng theo mô hình MVC (Model-View-Controller), giúp phân tách rõ ràng giữa dữ liệu, giao diện người dùng và logic xử lý

## 📌 Tính năng
- Hiển thị danh sách các bộ phim đoạt giải Oscar.
- Tìm kiếm phim theo tên, năm phát hành hoặc thể loại.
- Thêm, sửa, xóa thông tin phim.
- Lưu trữ dữ liệu phim trong file CSV.

## 🛠️ Công nghệ sử dụng
- Ngôn ngữ lập trình: Python
- Mô hình kiến trúc: MVC (Model-View-Controller)
- Lưu trữ dữ liệu: CSV

## 📂 Cấu trúc thư mục

```bash
OscarMovies/
├── Controller/
│   └── movie_controller.py
├── Data/
│   └── movies.csv
├── Model/
│   └── movie.py
├── View/
│   └── movie_view.py
├── main.py
└── README.md
``
- `Controller/`: Xử lý logic nghiệp vụ và tương tác giữa Model và View.
- `Data/`: Chứa dữ liệu phim dưới dạng file CSV.
- `Model/`: Định nghĩa lớp `Movie` và các phương thức liên quan đến dữ liệu.
- `View/`: Quản lý giao diện dòng lệnh và hiển thị thông tin cho người dùng.
- `main.py`: Điểm khởi đầu của ứng dụng.
```

## 🚀 Cách chạy ứng dụng

1. **Clone repository về máy:**
   ```bash
   git clone https://github.com/0402anhhuy/OscarMovies.git
   ```
2. **Di chuyển vào thư mục dự án:**
   ```bash
   cd OscarMovies
   ```
3. **Chạy ứng dụng:**

   ```bash
   python main.py
   ```
## 📌 Ghi chú
Đây là một dự án nhằm thực hành kỹ năng lập trình Python và áp dụng mô hình MVCV. Dự án có thể được mở rộng thêm các tính năng như giao diện đồ họa, kết nối cơ sở dữ liệu, hoặc tích hợp API để lấy dữ liệu phim.

