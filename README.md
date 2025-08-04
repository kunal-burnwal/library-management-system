# 📚 Library Management System – CLI + Web Interface

This is a Python-based Library Management System that offers both **Command Line Interface (CLI)** and **Web Interface** built using FastAPI. It allows users to manage book inventories, issue/return books, and maintain user records with simple yet effective file-based data storage.

---

## 🚀 Features

- 🔐 User login system (for both CLI and web)
- 📘 Add, issue, return, and view books
- 🧾 Book inventory management
- 🌐 Web interface using FastAPI + Jinja2
- 💾 Data persistence using JSON files

---

## 🛠 Tech Stack

| Area              | Tools/Technologies                        |
|-------------------|--------------------------------------------|
| Language          | Python                                     |
| Web Framework     | FastAPI, Jinja2                            |
| Backend Logic     | Python OOP, File Handling (JSON)           |
| Frontend (Web UI) | HTML, CSS (basic), Jinja2 Templates        |
| Deployment        | Localhost via Uvicorn                      |

---

## 📁 Folder Structure

library_system/

── main.py # Entry point for CLI version
── web_main.py # Entry point for FastAPI Web version
── book.py # Book class logic
── library.py # Core library logic
── books.json # Data file for book storage
── users.json # Data file for user credentials
── templates/ # HTML templates for FastAPI (Jinja2)
  ── index.html
  ── login.html
  ── dashboard.html



## 🧪 How to Run
#▶️ Run CLI Version
```bash
python main.py


#🌐 Run Web Version
uvicorn web_main:app --reload
#Open browser at: http://127.0.0.1:8000


🧑‍💻 Author
Kunal Burnwal


