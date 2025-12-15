from warehouse import list_warehouses, add_warehouse, update_warehouse, delete_warehouse
from product import list_products, add_product, update_product, delete_product, search_products
from transaction import list_transactions, inbound, outbound, transfer
from report import show_summary, export_to_csv, import_from_csv, export_to_excel, import_from_excel
from auth import logout, exit_system
from funksions import clear_console

def pause():
    input("\nDavom etish uchun Enter↩ bosing")

def warehouse_menu(role):
    while True:
        clear_console()
        clear_console()
        print("\n=== Ombor Menu ===\n")
        print("1. Ombor ro'yxati")
        if role == 'admin':
            print("2. Ombor qo'shish")
            print("3. Ombor tahrirlash")
            print("4. Ombor o'chirish")
        print("0. Orqaga")
        choice = input("Tanlash: ").strip()
        if choice == '1':
            list_warehouses()
        elif choice == '2' and role == 'admin':
            add_warehouse()
        elif choice == '3' and role == 'admin':
            update_warehouse()
        elif choice == '4' and role == 'admin':
            delete_warehouse()
        elif choice == '0':
            break
        else:
            print("Notogri tanlov")
        pause()

def product_menu(role):
    clear_console()
    while True:
        clear_console()
        print("\n=== Mahsulotlar Menu ===\n")
        print("1. Mahsulotlar ro'yxati")
        if role == 'admin':
            print("2. Add product")
            print("3. Update product")
            print("4. Delete product")
        print("5. Search products")
        print("0. Orqaga")
        choice = input("Tanlash: ").strip()
        if choice == '1':
            list_products()
        elif choice == '2' and role == 'admin':
            add_product()
        elif choice == '3' and role == 'admin':
            update_product()
        elif choice == '4' and role == 'admin':
            delete_product()
        elif choice == '5':
            search_products()
        elif choice == '0':
            break
        else:
            print("Notogri tanlov.")
        pause()

def transaction_menu(role):
    clear_console()
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
            print("Notogri tanlov.")
        pause()

def reports_menu(role):
    clear_console()
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
            print("Notogri tanlov")
        pause()

def main_menu(user):
    clear_console()   
    role = user.get('role')
    while True:
        clear_console()
        print("\n=== WMS MENU ===\n")
        print("1. Ombor boshqaruvi")
        print("2. Mahsulot boshqaruvi")
        print("3. Tranzaksiyalar")
        print("4. Hisobotlar")
        print("5. Hisobdan chiqish")
        print("0. chiqish")
        
        choice = input("Tanlash: ").strip()

        if choice == '1':
            warehouse_menu(role)
        
        elif choice == '2':
            product_menu(role)
        
        elif choice == '3':
            transaction_menu(role)
        
        elif choice == '4':
            reports_menu(role)
        
        
        elif choice == '5':
            logout()
            return False
        
        elif choice == '0':
            print("Exiting...")
            exit_system()
            return True
        
        else:
            print("Notogri tanlov.")


