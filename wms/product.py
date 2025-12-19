from .storage import load_data, save_data
from .utils import clear_console, display_products_table, textColor, display_warehouse_table


def add_product():
    data = load_data()
    products = data["products"]
    display_warehouse_table(data["warehouses"])

    max_id = 0
    for p in products:
        if p["id"] > max_id:
            max_id = p["id"]

    warehouseID = input("Ombor ID: ")
    name = input("Mahsulot Nomi: ")

    warehouse_ids = []
    for w in data["warehouses"]:
        warehouse_ids.append(w["id"])

    if name == "":
        clear_console()
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    try:
        warehouseID = int(warehouseID)
    except:
        warehouseID = None

    if warehouseID not in warehouse_ids:
        clear_console()
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    quantity = input("Miqdori: ")
    try:
        quantity = int(quantity)
    except:
        quantity = 0

    price = input("Narxi: ")
    try:
        price = float(price)
    except:
        price = 0.0

    product = {
        "id": max_id + 1,
        "name": name,
        "quantity": quantity,
        "warehouse_id": warehouseID,
        "price": price
    }

    products.append(product)
    save_data(data)

    clear_console()
    display_products_table([product], title="➕ Mahsulot qo'shildi")


def update_product():
    data = load_data()
    products = data["products"]
    display_products_table(products)

    productID = input("Tahrirlash uchun Mahsulot ID kiriting: ")
    try:
        productID = int(productID)
    except:
        print(textColor("ID mavjud emas", "red"))
        return

    for p in products:
        if p["id"] == productID:
            name = input(f"Name ({p['name']}): ")
            if name != "":
                p["name"] = name

            quantity = input(f"Quantity ({str(p['quantity'])}): ")
            if quantity != "":
                try:
                    p["quantity"] = int(quantity)
                except:
                    pass

            warehouseID = input(f"Warehouse ID ({str(p['warehouse_id'])}): ")
            if warehouseID != "":
                try:
                    p["warehouse_id"] = int(warehouseID)
                except:
                    pass

            price = input(f"Price ({str(p['price'])}): ")
            if price != "":
                try:
                    p["price"] = float(price)
                except:
                    pass

            save_data(data)
            print(textColor("Mahsulot yangilandi", "blue"))
            return
    print(textColor("Mahsulot topilmadi", "red", "blue"))


def delete_product():
    data = load_data()
    products = data["products"]
    display_products_table(products)

    productID = input("O'chirish uchun mahsulot ID kiriting: ")
    try:
        productID = int(productID)
    except:
        print(textColor("ID mavjud emas", "red"))
        return

    for p in products:
        if p["id"] == productID:
            products.remove(p)
            save_data(data)
            print(textColor("O'chirildi", "blue", "blue"))
            return
    print(textColor("Mahsulot topilmadi", "red", "blue"))


def list_products():
    data = load_data()
    products = data["products"]
    display_products_table(products, title="📦 Mahsulotlar ro'yxati")


def search_products():
    data = load_data()
    products = data["products"]
    term = input("Qidirish Nomi yoki ID: ").lower()
    found = []

    for p in products:
        if str(p["id"]) == term or term in p["name"].lower():
            found.append(p)

    display_products_table(found, title="🔍 Qidiruv natijasi: " + term)
