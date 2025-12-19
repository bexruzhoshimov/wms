from .storage import load_data, save_data
from .utils import textColor, clear_console

def get_users():
    data = load_data()
    return data["users"]


def find_user(username):
    users = get_users()

    for user in users:
        if user["username"] == username:
            return user
    return None


def login():
    print("    === WMS LOGIN ===\n")

    username = input("Username: ")
    password = input("Password: ")

    user = find_user(username)

    if user is not None:
        if user["password"] == password:
            data = load_data()
            data["login"] = user
            save_data(data)
            return user

    clear_console()
    print(textColor("Foydalanuvchi mavjud emas", "red"))
    return None


def logout():
    data = load_data()
    data["login"] = {}
    save_data(data)
