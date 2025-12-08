from storage import load_data, save_data

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
    print("=== WMS LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
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
