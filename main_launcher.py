from wms.auth import login, ensure_admin_exists
from wms.main import main_menu
from wms.utils import clear_console
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "wms"))


def starting():
    while True:
        clear_console()
        user = None
        while not user:
            user = login()

        quit_app = main_menu()
        if quit_app:
            break


if __name__ == "__main__":
    ensure_admin_exists()
starting()
