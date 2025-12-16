from .storage import load_data, save_data
from .utils import input_password, textColor, clear_console


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
    print(f"printbu{username}")
    password = input_password("Password: ")
    print(f"printbu{password}")
    user = find_user(username)
    if user and user.get("password") == password:
        data = load_data()
        data["login"] = user
        save_data(data)
        return user
    clear_console()
    print(textColor("Foydalanuvchi mavjud emas", "red", "bold"))


def ensure_admin_exists():
    data = load_data()
    users = data.setdefault("users", [])
    if not any(u.get("username") == "admin" for u in users):
        users.append(
            {"username": "admin", "password": "admin", "role": "admin"})
        save_data(data)


def logout():
    data = load_data()
    data["login"] = {}
    save_data(data)
    while True:
        clear_console()
        user = None
        while not user:
            user = login()
        # main_menu()
