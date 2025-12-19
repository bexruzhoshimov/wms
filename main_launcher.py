from wms.auth import login
from wms.main import main_menu
from wms.storage import load_data
from wms.utils import clear_console
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "wms"))

if __name__ == "__main__":
    data = load_data()
    if (data["login"] != {}):
        main_menu()
    else:
        while True:
            clear_console()
            user = None
            while not user:
                user = login()
            main_menu()
