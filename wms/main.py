from .auth import logout, exit_system
from .storage import load_data, save_data
from .warehouse import list_warehouses, add_warehouse, update_warehouse, delete_warehouse
from .product import list_products, add_product, update_product, delete_product, search_products
from .transaction import list_transactions, inbound, outbound, transfer
from .report import show_summary, export_to_csv, import_from_csv, export_to_excel, import_from_excel
from .utils import clear_console, run_menu_curses
# from .menus import productMenu, warehauseMenu
import curses


def pause():
    input("\nDavom etish uchun Enter bosing")


def warehouse_menu():
    role = load_data()["login"]["role"]
    curses.wrapper(run_menu_curses, "Ombor Menu", warehauseMenu, role)


def product_menu():
    role = load_data()["login"]["role"]
    curses.wrapper(run_menu_curses, "Mahsulotlar Menu", productMenu, role)


def transaction_menu():
    role = load_data()["login"]["role"]
    while True:
        clear_console()
        print("\n=== Tranzaksiyalar Menu ===\n")
        print("1. Tranzaksiyalar Ro'yxati")
        if role in ['admin', 'user']:
            print("2. Inbound (receive)")
            print("3. Outbound (ship)")
            print("4. Transfer between warehouses")
        print("0. Orqaga")
        choice = input("Tanlash: ").strip()
        if choice == '1':
            list_transactions()
        elif choice == '2' and role in ['admin', 'user']:
            inbound()
        elif choice == '3' and role in ['admin', 'user']:
            outbound()
        elif choice == '4' and role in ['admin', 'user']:
            transfer()
        elif choice == '0':
            break
        else:
            print("Notog'ri tanlov.")
        pause()


def reports_menu():
    # role = load_data()["login"]["role"]
    while True:
        clear_console()
        print("\n=== Hisobotlar Menu ===\n")
        print("1. Xulosa ko'rsatish")
        print("2. Mahsulotlarni CSVga eksport qilish (wms_export.csv)")
        print("3. CSV dan mahsulotlarni import qilish (wms_import.csv)")
        print("4. Excelga eksport qilish")
        print("5. Exceldan import qilish")
        print("0. Orqaga")
        choice = input("Tanlash: ").strip()
        if choice == '1':
            show_summary()
        elif choice == '2':
            export_to_csv()
        elif choice == '3':
            import_from_csv()
        elif choice == '4':
            export_to_excel()
        elif choice == '5':
            import_from_excel()
        elif choice == '0':
            break
        else:
            print("Notog'ri tanlov")
        pause()


def main_menu():
    role = load_data()["login"]["role"]
    print(role)
    curses.wrapper(run_menu_curses, "WMS MENU", mainMenu, role)

    # while True:
    #     clear_console()
    #     print("\n===  ===\n")
    #     print("1. Ombor boshqaruvi")
    #     print("2. Mahsulot boshqaruvi")
    #     print("3. Tranzaksiyalar")
    #     print("4. Hisobotlar")
    #     print("5. Hisobdan chiqish")
    #     print("0. chiqish")

    #     choice = input("Tanlash: ").strip()

    #     if choice == '1':
    #         warehouse_menu()

    #     elif choice == '2':
    #         product_menu()

    #     elif choice == '3':
    #         transaction_menu()

    #     elif choice == '4':
    #         reports_menu()

    #     elif choice == '5':
    #         logout()
    #         return False

    #     elif choice == '0':
    #         print("Exiting...")
    #         exit_system()
    #         return True

    #     else:
    #         print("Notogri tanlov.")


mainMenu = [
    {"label": "Ombor boshqaruvi", "action": warehouse_menu},
    {"label": "Mahsulot boshqaruvi", "action": product_menu, "role": "admin"},
    {"label": "Tranzaksiyalar", "action": transaction_menu},
    {"label": "Hisobotlar", "action": reports_menu, "role": "admin"},
    {"label": "Hisobdan chiqish", "action": logout, "role": "admin"},
    {"label": "Chiqish", "exit": True}
]

warehauseMenu = [
    {"label": "Ombor ro'yxati", "action": list_warehouses},
    {"label": "Ombor qo'shish", "action": add_warehouse},
    {"label": "Ombor tahrirlash", "action": update_warehouse},
    {"label": "Ombor o'chirish", "action": delete_warehouse},
    {"label": "Orqaga", "exit": True}
]

productMenu = [
    {"label": "Mahsulotlar ro'yxati", "action": list_products},
    {"label": "Mahsulot qo'shish", "action": add_product},
    {"label": "Mahsulot tahrirlash", "action": update_product},
    {"label": "Mahsulot o'chirish", "action": delete_product},
    {"label": "Mahsulot qidirish", "action": search_products},
    {"label": "Orqaga", "exit": True}
]
