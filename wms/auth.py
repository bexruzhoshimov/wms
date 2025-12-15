from storage import load_data, save_data
from funksions import input_password

def get_users():
    data = load_data()
    return data.setdefault("users", [])

def find_user(username):
    users = get_users()
    for u in users:
        if u.get("username") == username:
            return u
    return None

def login():
    print("=== WMS LOGIN ===\n")
    username = input("Username: ").strip()
    password = input_password("Password: ")
    user = find_user(username)
    if user and user.get("password") == password:
        print(f"Login successful. Role: {user.get('role')}")
        return user
    print("Login failed.")
    return None

def ensure_admin_exists():
    data = load_data()
    users = data.setdefault("users", [])
    if not any(u.get("username")=="admin" for u in users):
        users.append({"username":"admin","password":"admin123","role":"admin"})
        save_data(data)

def logout():
    print("Logging out...")
    # Here you can also clear session data or perform any other actions needed
    return None

def exit_system():
    print("Exiting the system...")
    # Here you can perform any cleanup actions before the program terminates, if necessary
    exit()