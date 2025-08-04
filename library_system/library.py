import json
from book import Book

class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.borrowed_books = {}  # username -> list of ISBNs
        self.load_data()

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        for book in self.books:
            print(book)

    def display_borrowed_books(self, username):
        borrowed = self.borrowed_books.get(username, [])
        if not borrowed:
            print("You have not borrowed any books.")
            return
        for isbn in borrowed:
            for book in self.books:
                if book.isbn == isbn:
                    print(book)

    def borrow_book(self, isbn, username):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed:
                    print("Book not available.")
                    return
                book.is_borrowed = True
                self.borrowed_books.setdefault(username, []).append(isbn)
                print(f"{username} borrowed '{book.title}'.")
                return
        print("Book not found.")

    def return_book(self, isbn, username):
        for book in self.books:
            if book.isbn == isbn and book.is_borrowed:
                if username in self.borrowed_books and isbn in self.borrowed_books[username]:
                    book.is_borrowed = False
                    self.borrowed_books[username].remove(isbn)
                    print(f"Returned '{book.title}'.")
                    return
                else:
                    print("You did not borrow this book.")
                    return
        print("Book not found or not borrowed.")

    def search_book(self, keyword):
        found = False
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                print(book)
                found = True
        if not found:
            print("No books found.")

    def register_user(self, username, password):
        if username in self.users:
            print("User already exists.")
            return False
        self.users[username] = password
        print(f"User '{username}' registered successfully.")
        return True

    def login_user(self, username, password):
        return self.users.get(username) == password

    def change_password(self, username, new_password):
        if username in self.users:
            self.users[username] = new_password
            print("Password changed successfully.")
        else:
            print("User not found.")

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.borrowed_books.pop(username, None)
            print("User deleted.")
        else:
            print("User not found.")

    def save_data(self):
        with open('books.json', 'w') as f:
            json.dump([book.__dict__ for book in self.books], f)
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
        with open('borrowed_books.json', 'w') as f:
            json.dump(self.borrowed_books, f)

    def load_data(self):
        try:
            with open('books.json', 'r') as f:
                books_data = json.load(f)
                self.books = [Book(**data) for data in books_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = [
                Book("Python Crash Course", "Eric Matthes", "1001"),
                Book("Clean Code", "Robert C. Martin", "1002"),
                Book("Automate the Boring Stuff", "Al Sweigart", "1003"),
            ]

        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

        try:
            with open('borrowed_books.json', 'r') as f:
                self.borrowed_books = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.borrowed_books = {}
