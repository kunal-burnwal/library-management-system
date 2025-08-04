from fastapi import FastAPI, Request, Form, Depends, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ensure 'static' directory exists before mounting
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DATA_DIR = os.path.dirname(__file__)
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BORROWED_FILE = os.path.join(DATA_DIR, "borrowed_books.json")

def read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data else default
    except Exception:
        return default

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_user(username, password=None):
    users = read_json(USERS_FILE, [])
    for u in users:
        if u["username"] == username and (password is None or u["password"] == password):
            return u
    return None

def create_user(username, password):
    users = read_json(USERS_FILE, [])
    if any(u["username"] == username for u in users):
        return False
    users.append({"username": username, "password": password})
    write_json(USERS_FILE, users)
    return True

def get_books():
    return read_json(BOOKS_FILE, [])

def borrow_book(isbn, username):
    books = read_json(BOOKS_FILE, [])
    borrowed = read_json(BORROWED_FILE, {})
    for book in books:
        if book["isbn"] == isbn:
            if book["is_borrowed"]:
                return False
            book["is_borrowed"] = True
            borrowed.setdefault(username, []).append(isbn)
            write_json(BOOKS_FILE, books)
            write_json(BORROWED_FILE, borrowed)
            return True
    return False

def return_book(isbn, username):
    books = read_json(BOOKS_FILE, [])
    borrowed = read_json(BORROWED_FILE, {})
    if username not in borrowed or isbn not in borrowed[username]:
        return False
    for book in books:
        if book["isbn"] == isbn:
            book["is_borrowed"] = False
            borrowed[username].remove(isbn)
            if not borrowed[username]:
                del borrowed[username]
            write_json(BOOKS_FILE, books)
            write_json(BORROWED_FILE, borrowed)
            return True
    return False

def get_borrowed_books(username):
    borrowed = read_json(BORROWED_FILE, {})
    books = read_json(BOOKS_FILE, [])
    isbns = borrowed.get(username, [])
    return [book for book in books if book["isbn"] in isbns]

# Simple session management
def get_current_user(request: Request):
    username = request.cookies.get("username")
    if username and get_user(username):
        return username
    return None

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    if get_user(username, password):
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="username", value=username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@app.post("/register")
def register(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    if create_user(username, password):
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        return response
    return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    borrowed = get_borrowed_books(user)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "borrowed_books": borrowed})

@app.get("/books", response_class=HTMLResponse)
def book_list(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    books = get_books()
    return templates.TemplateResponse("book_list.html", {"request": request, "user": user, "books": books})

@app.post("/borrow")
def borrow(request: Request, isbn: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    if borrow_book(isbn, user):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/books", status_code=status.HTTP_302_FOUND)

@app.post("/return")
def return_b(request: Request, isbn: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    if return_book(isbn, user):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie("username")
    return response
