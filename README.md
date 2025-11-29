# Space-Study-Project (Backend)

## Giới thiệu / Introduction  
Space-Study-Project là backend cung cấp API & kết nối database cho hệ thống quản lý Study Space (hệ thống Study Space Management System). /  
Space-Study-Project is the backend part implementing database & REST API for the Study Space Management System.

---

## Yêu cầu trước / Prerequisites  

- Python ≥ 3.10  
- Microsoft SQL Server (Developer / Express / tương đương)  
- (Tùy chọn nhưng khuyến nghị) SQL Server Management Studio (SSMS) để quản lý database dễ dàng  

---

## Cài đặt / Installation  

1. Clone repo và chuyển tới thư mục backend  
   ```bash
   git clone https://github.com/AtomTNB2202/Space-Study-Project.git  
   cd Space-Study-Project/Project-Study_Space_Backend  
Tạo môi trường ảo (virtual environment) và kích hoạt nó

Windows:

bat
Sao chép mã
python -m venv .venv  
.venv\Scripts\activate
macOS / Linux:

bash
Sao chép mã
python -m venv .venv  
source .venv/bin/activate
Cài các dependencies

bash
Sao chép mã
pip install -r requirements.txt
Cấu hình Database / Database Configuration
Trong file .env hoặc config.py (tùy cấu trúc code), chỉnh các biến môi trường sau cho phù hợp với máy bạn:

ini
Sao chép mã
DB_SERVER=localhost  
DB_PORT=1433  
DB_NAME=StudySpaceDB  
DB_USER=sa  
DB_PASSWORD=yourStrong(!)Password  
DB_DRIVER=ODBC Driver 17 for SQL Server  
⚠️ Nếu máy bạn chưa có driver ODBC cho SQL Server — hãy cài đặt driver phù hợp theo hướng dẫn chính thức Microsoft.

Sau đó, khởi tạo database:

Mở SSMS → connect tới SQL Server → tạo database:

sql
Sao chép mã
CREATE DATABASE StudySpaceDB;
(Nếu có提供 script schema .sql): import schema / bảng dữ liệu mẫu nếu có

Khởi chạy Backend / Run Backend
Có 2 cách để chạy server:

Cách 1: trực tiếp với uvicorn

bash
Sao chép mã
uvicorn main:app --reload
Cách 2: bằng module Python

bash
Sao chép mã
python -m uvicorn main:app --reload
Sau khi chạy, backend sẽ lắng nghe mặc định tại:

cpp
Sao chép mã
http://127.0.0.1:8000  
API Documentation
Backend sử dụng FastAPI — nên bạn có thể truy cập tài liệu API tự động tại:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Cấu trúc dự án / Project Structure
bash
Sao chép mã
Project-Study_Space_Backend/
├── app/
│   ├── main.py            # application entry point
│   ├── routers/           # định nghĩa các route / API endpoints  
│   ├── controllers/       # logic xử lý nghiệp vụ  
│   ├── models/            # mô hình dữ liệu / Pydantic models  
│   ├── database/          # logic kết nối DB  
│   └── utils/             # helper / công cụ phụ trợ  
├── requirements.txt  
├── README.md  
└── .env                   # (hoặc config file) chứa cấu hình DB / environment  
