from library import Library

def main():
    lib = Library()

    print("=== Welcome to Library System ===")
    print("\n1. Login\n2. Register")
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        username = input("Username: ")
        password = input("Password: ")
        if not lib.login_user(username, password):
            print("Invalid credentials. Exiting.")
            return
        print(f"Welcome back, {username}!")

    elif choice == '2':
        username = input("Choose username: ")
        password = input("Choose password: ")
        if not lib.register_user(username, password):
            return
        print(f"User '{username}' registered successfully.")
    else:
        print("Invalid choice.")
        return

    while True:
        print("\n=== Library Menu ===")
        print("1. Display all books")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search books")
        print("5. View my borrowed books")
        print("6. Change password")
        print("7. Delete my account")
        print("8. Logout & Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            lib.display_books()
        elif choice == '2':
            isbn = input("Enter ISBN of book to borrow: ")
            lib.borrow_book(isbn, username)
        elif choice == '3':
            isbn = input("Enter ISBN of book to return: ")
            lib.return_book(isbn, username)
        elif choice == '4':
            keyword = input("Enter keyword to search: ")
            lib.search_book(keyword)
        elif choice == '5':
            lib.display_borrowed_books(username)
        elif choice == '6':
            new_password = input("Enter new password: ")
            lib.change_password(username, new_password)
        elif choice == '7':
            confirm = input("Are you sure you want to delete your account? (y/n): ")
            if confirm.lower() == 'y':
                lib.delete_user(username)
                lib.save_data()
                print("Account deleted. Exiting.")
                break
        elif choice == '8':
            lib.save_data()
            print("Exiting. Data saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
