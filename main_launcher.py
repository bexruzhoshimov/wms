import sys
import os

# wms papkasini pathga qo'shamiz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "wms"))  # wms papkasi

# wms papkasidagi main.py dan main_menu funksiyasini import qilamiz
from main import main_menu
from auth import login, ensure_admin_exists

if __name__ == "__main__":
    ensure_admin_exists()  # Ensures at least one admin exists

    while True:
        user = None
        while not user:
            user = login()  # Login function
        quit_app = main_menu(user)  # Main menu with user
        if quit_app:
            break
