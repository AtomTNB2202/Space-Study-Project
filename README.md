1️⃣ Overview

This backend is built using FastAPI, served by Uvicorn, and uses Microsoft SQL Server as the main database.
It provides all API endpoints for the Space Study Management System.

2️⃣ System Requirements
🔧 Required Tools
1. Python 3.10+

Download: https://www.python.org/downloads/

2. Microsoft SQL Server

You may use SQL Server Developer or Express:
https://www.microsoft.com/en-us/sql-server/sql-server-downloads

3. SQL Server Management Studio (SSMS)

Used for database management:
https://aka.ms/ssmsfullsetup

3️⃣ Clone the Project
git clone https://github.com/AtomTNB2202/Space-Study-Project
cd Space-Study-Project/Project-Study_Space_Backend

4️⃣ Create Virtual Environment & Install Dependencies
(1) Create virtual environment
python -m venv .venv

(2) Activate the environment

Windows

.venv\Scripts\activate


MacOS/Linux

source .venv/bin/activate

(3) Install dependencies
pip install -r requirements.txt

5️⃣ Database Configuration (SQL Server)

Modify your .env or config.py depending on your project structure:

DB_SERVER=localhost
DB_PORT=1433
DB_NAME=StudySpaceDB
DB_USER=sa
DB_PASSWORD=yourStrong(!)Password
DB_DRIVER=ODBC Driver 17 for SQL Server


⚠️ If you do not have the ODBC driver installed, download it here:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

6️⃣ Initialize the Database
(1) Open SSMS and connect to SQL Server
(2) Create the database
CREATE DATABASE StudySpaceDB;

(3) Import any .sql schema files provided in the project (if available)
7️⃣ Run the Backend
Option 1: Run directly
uvicorn main:app --reload

Option 2: Run with Python module
python -m uvicorn main:app --reload


Backend will be available at:
👉 http://127.0.0.1:8000

8️⃣ API Documentation

FastAPI automatically provides API docs:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

9️⃣ Project Structure
Project-Study_Space_Backend/
│── app/
│   ├── main.py              # Application entry point
│   ├── routers/             # All API routes
│   ├── models/              # Pydantic models
│   ├── controllers/         # Business logic
│   ├── database/            # Database connection logic
│   ├── utils/               # Helper utilities
│── requirements.txt
│── README.md
│── .env
