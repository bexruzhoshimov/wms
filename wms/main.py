from .auth import logout
from .storage import load_data, save_data
from .warehouse import list_warehouses, add_warehouse, update_warehouse, delete_warehouse
from .product import list_products, add_product, update_product, delete_product, search_products
from .transaction import list_transactions, inbound, outbound, transfer
from .report import show_summary, export_to_csv, import_from_csv, export_to_excel, import_from_excel
from .utils import run_menu_curses
import curses


def warehouse_menu(stdscr):
    data = load_data()
    role = data["login"]["role"]
    warehouse_totals = {}
    for p in data["products"]:
        wid = p.get("warehouse_id")
        if wid is not None:
            warehouse_totals[wid] = warehouse_totals.get(
                wid, 0) + p["quantity"]

    for w in data["warehouses"]:
        w["current"] = warehouse_totals.get(w["id"], 0)

    save_data(data)
    run_menu_curses(stdscr, "Ombor Menu", warehauseMenu, role)


def product_menu(stdscr):
    role = load_data()["login"]["role"]
    run_menu_curses(stdscr, "Mahsulotlar Menu", productMenu, role)


def transaction_menu(stdscr):
    role = load_data()["login"]["role"]
    run_menu_curses(stdscr, "Tranzaksiyalar Menu", tranzaksiyaMenu, role)


def reports_menu(stdscr):
    role = load_data()["login"]["role"]
    run_menu_curses(stdscr, "Hisobotlar Menu", reportsMenu, role)


def main_menu():
    role = load_data()["login"]["role"]
    curses.wrapper(run_menu_curses, "WMS MENU", mainMenu, role)


mainMenu = [
    {"label": "Ombor boshqaruvi", "action": warehouse_menu},
    {"label": "Mahsulot boshqaruvi", "action": product_menu, "role": "admin"},
    {"label": "Tranzaksiyalar", "action": transaction_menu},
    {"label": "Hisobotlar", "action": reports_menu, "role": "admin"},
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
    {"label": "Mahsulotlarni CSVga eksport qilish (wms_export.csv)",
     "action": export_to_csv},
    {"label": "CSV dan mahsulotlarni import qilish (wms_import.csv)",
     "action": import_from_csv},
    {"label": "Excelga eksport qilish", "action": export_to_excel},
    {"label": "Exceldan import qilish", "action": import_from_excel},
    {"label": "Orqaga", "back": True}
]

tranzaksiyaMenu = [
    {"label": "Tranzaksiyalar ro'yxati", "action": list_transactions},
    {"label": "Kirim (omborga qabul qilish)", "action": inbound},
    {"label": "Chiqim (ombordan jo'natish)", "action": outbound},
    {"label": "Omborlar o'rtasida ko'chirish", "action": transfer},
    {"label": "Orqaga qaytish", "back": True}
]