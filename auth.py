import bcrypt
import os


def hash_password(plain_text_password):
    """Hashes a plain text password using bcrypt."""
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def verify_password(plain_text_password, hashed_password):
    """Verifies a password against its hash."""
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


USER_DATA_FILE = "users.txt"


def register_user(username, password):
    """Registers a new user and saves to users.txt."""
    if user_exists(username):
        print("Error: Username already exists.")
        return False

    hashed_pw = hash_password(password)
    with open(USER_DATA_FILE, "ab") as file:
        file.write(username.encode('utf-8') + b":" + hashed_pw + b"\n")

    print(f"User '{username}' registered successfully!")
    return True


def user_exists(username):
    """Checks if a username already exists in the file."""
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "rb") as file:
        for line in file:
            stored_username, _ = line.strip().split(b":")
            if stored_username.decode('utf-8') == username:
                return True
    return False


def login_user(username, password):
    """Authenticates a user by verifying credentials from users.txt."""
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "rb") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(b":")
            if stored_username.decode('utf-8') == username:
                if verify_password(password, stored_hash):
                    return True
                else:
                    print("Error: Incorrect password.")
                    return False

    print("Error: Username not found.")
    return False


def display_menu():
    """Displays the main menu options."""
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def validate_username(username):
    """Check that the username is at least 3 characters and alphanumeric."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    return True, ""


def validate_password(password):
    """Check that the password is at least 6 characters long."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the database)")
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
