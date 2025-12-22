from .auth import logout
from .storage import load_data, save_data
from .warehouse import list_warehouses, add_warehouse, update_warehouse, delete_warehouse
from .product import list_products, add_product, update_product, delete_product, search_products
from .transaction import list_transactions, inbound, outbound, transfer
from .report import show_summary, export_to_csv, import_from_csv
from .utils import run_menu_curses
import curses


def warehouse_menu(stdscr):
    data = load_data()
    warehouse_totals = {}

    for product in data["products"]:
        warehouseID = product["warehouse_id"]

        if warehouseID is not None:
            if warehouseID not in warehouse_totals:
                warehouse_totals[warehouseID] = 0

            warehouse_totals[warehouseID] = warehouse_totals[warehouseID] + \
                product["quantity"]

    for warehouse in data["warehouses"]:
        warehouseID = warehouse["id"]

        if warehouseID in warehouse_totals:
            warehouse["current"] = warehouse_totals[warehouseID]
        else:
            warehouse["current"] = 0

    save_data(data)
    run_menu_curses(stdscr, "Ombor Menu", warehauseMenu)


def product_menu(stdscr):
    run_menu_curses(stdscr, "Mahsulotlar Menu", productMenu)


def transaction_menu(stdscr):
    run_menu_curses(stdscr, "Tranzaksiyalar Menu", tranzaksiyaMenu)


def reports_menu(stdscr):
    run_menu_curses(stdscr, "Hisobotlar Menu", reportsMenu)


def main_menu():
    curses.wrapper(run_menu_curses, "WMS MENU", mainMenu)


mainMenu = [
    {"label": "Ombor boshqaruvi", "action": warehouse_menu},
    {"label": "Mahsulot boshqaruvi", "action": product_menu},
    {"label": "Tranzaksiyalar", "action": transaction_menu},
    {"label": "Hisobotlar", "action": reports_menu},
    {"label": "Hisobdan chiqish", "logout": logout},
    {"label": "Chiqish", "quit": True}
]


warehauseMenu = [
    {"label": "Ombor ro'yxati", "action": list_warehouses},
    {"label": "Ombor qo'shish", "action": add_warehouse},
    {"label": "Ombor tahrirlash", "action": update_warehouse},
    {"label": "Ombor o'chirish", "action": delete_warehouse},
    {"label": "Orqaga", "back": True}
]


productMenu = [
    {"label": "Mahsulotlar ro'yxati", "action": list_products},
    {"label": "Mahsulot qo'shish", "action": add_product},
    {"label": "Mahsulot tahrirlash", "action": update_product},
    {"label": "Mahsulot o'chirish", "action": delete_product},
    {"label": "Mahsulot qidirish", "action": search_products},
    {"label": "Orqaga", "back": True}
]


reportsMenu = [
    {"label": "Xulosa ko'rsatish", "action": show_summary},
    {"label": "Eksport qilish (wms_export.csv)", "action": export_to_csv},
    {"label": "Import qilish (wms_import.csv)", "action": import_from_csv},
    {"label": "Orqaga", "back": True}
]


tranzaksiyaMenu = [
    {"label": "Tranzaksiyalar ro'yxati", "action": list_transactions},
    {"label": "Kirim (omborga qabul qilish)", "action": inbound},
    {"label": "Chiqim (ombordan jo'natish)", "action": outbound},
    {"label": "Omborlar o'rtasida ko'chirish", "action": transfer},
    {"label": "Orqaga qaytish", "back": True}
]
