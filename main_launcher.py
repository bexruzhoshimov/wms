# convenience launcher
from auth import login, ensure_admin_exists
ensure_admin_exists()
from main import main_menu
user = None
while not user:
    user = login()
main_menu(user)
