Cách chạy backend (FastAPI + PostgreSQL)
1. Yêu cầu môi trường

Python 3.12+

Docker & Docker Compose

Git

Lưu ý: Các lệnh dưới đây demo trên Windows (PowerShell). Trên Linux/macOS chỉ cần bỏ py → python là được.

2. Clone project về máy
git clone https://github.com/AtomTNB2202/Space-Study-Project.git
cd Space-Study-Project


Cấu trúc chính (tóm tắt):

Space-Study-Project/
├── app/
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── schemas/
│   └── crud/
├── Database/
│   └── schema.sql         # file tạo bảng mẫu
├── docker-compose.yml     # chạy Postgres + (tùy) backend
└── README.md

Cách 1: Chạy bằng Docker Compose
Bước 1: Khởi động PostgreSQL
docker compose up -d

PostgreSQL sẽ chạy trong container postgres.

Nếu trong docker-compose.yml đã khai báo service backend thì nó cũng sẽ tự chạy luôn.

Bước 2: (Tuỳ chọn) Import schema mẫu

Nếu bạn muốn tạo sẵn bảng & dữ liệu mẫu từ Database/schema.sql:

docker exec -it postgres bash
psql -U postgres -d studyspace < /app/Database/schema.sql


Tuỳ POSTGRES_DB, POSTGRES_USER trong docker-compose.yml mà bạn chỉnh lại -U và -d cho đúng.

Bước 3: Mở API docs

Mặc định backend chạy ở:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Cách 2: Chạy thủ công bằng Python (dev mode)
Bước 1: Tạo virtualenv và cài thư viện
# Đang đứng trong thư mục Space-Study-Project
py -m venv .venv
.\.venv\Scripts\activate          # Windows
# source .venv/bin/activate       # Linux/macOS

pip install --upgrade pip
pip install -r requirements.txt   # nếu có file requirements.txt


Nếu repo chưa có requirements.txt bạn có thể tự tạo với các package chính:

fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic[email]
passlib[bcrypt]
python-dotenv


Sau đó:

pip install -r requirements.txt

Bước 2: Khởi động PostgreSQL bằng Docker
docker compose up -d postgres

Bước 3: Tạo schema database
docker exec -it postgres bash
psql -U postgres -d studyspace < /app/Database/schema.sql


(hoặc tự psql rồi copy các câu lệnh trong Database/schema.sql chạy bằng tay)

Bước 4: Chạy ứng dụng FastAPI

Từ thư mục gốc project:

uvicorn app.main:app --reload


Nếu PYTHONPATH bị lỗi import app.xxx, có thể chạy:

# Windows PowerShell
$env:PYTHONPATH = "."
uvicorn app.main:app --reload
