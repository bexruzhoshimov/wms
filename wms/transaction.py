from .storage import load_data, save_data
from datetime import datetime
from .utils import clear_console, textColor, display_tranzaksiya_table


def list_transactions():
    data = load_data()
    transactions = data["transactions"]
    display_tranzaksiya_table(transactions)


def write_transaction(t_type, product_id, product_name, quantity, from_wh=None, to_wh=None):
    data = load_data()
    transactions = data["transactions"]

    transactions.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": t_type,
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "from": from_wh,
        "to": to_wh
    })

    save_data(data)


def inbound():
    data = load_data()
    products = data["products"]
    productID = input("Kirim uchun Mahsulot ID kiritig: ")

    try:
        productID = int(productID)
    except:
        clear_console()
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    quantity = input("Qo'shiladigan miqdor: ")
    try:
        quantity = int(quantity)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    for p in products:
        if p["id"] == productID:
            p["quantity"] = p["quantity"] + quantity
            save_data(data)

            write_transaction(
                "Kirim",
                productID,
                p["name"],
                quantity,
                from_wh=None,
                to_wh=p["warehouse_id"]
            )

            print(textColor("Kirim qilindi", "blue"))
            return

    print(textColor("Mahsulot topilmadi", "red"))


def outbound():
    data = load_data()
    products = data["products"]
    productID = input("Chiqim uchun Mahsulot ID kiritig: ")

    try:
        productID = int(productID)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    quantity = input("Ayiriladigan miqdor: ")
    try:
        quantity = int(quantity)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    for p in products:
        if p["id"] == productID:
            if p["quantity"] < quantity:
                print("Mahsulot yetarli miqdorda emas")
                return

            p["quantity"] = p["quantity"] - quantity
            save_data(data)

            write_transaction(
                "Chiqim",
                productID,
                p["name"],
                quantity,
                from_wh=p["warehouse_id"],
                to_wh=None
            )

            print(textColor("Chiqim qilindi", "blue"))
            return

    print(textColor("Mahsulot topilmadi", "red", "blue"))


def transfer():
    data = load_data()
    products = data["products"]
    productID = input("Transfer mahsulot ID: ")

    try:
        productID = int(productID)
    except:
        print(textColor("Mahsulot topilmadi", "red", "blue"))
        return

    to_warehouse = input("Ombor ID: ")
    try:
        to_warehouse = int(to_warehouse)
    except:
        print(textColor("Ombor topilmadi", "red", "blue"))
        return

    quantity = input("Ko'chirish miqdori: ")
    try:
        quantity = int(quantity)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red"))
        return

    for product in products:
        if product["id"] == productID:
            if product["quantity"] < quantity:
                print("O'tkazish uchun yetarli miqdor yo'q")
                return

            source_wh = product["warehouse_id"]
            product["quantity"] = product["quantity"] - quantity

            target_product = None
            for q in products:
                if q["name"] == product["name"] and q["warehouse_id"] == to_warehouse:
                    target_product = q
                    break

            if target_product is not None:
                target_product["quantity"] = target_product["quantity"] + quantity
            else:
                max_id = 0
                for item in products:
                    if item["id"] > max_id:
                        max_id = item["id"]

                products.append({
                    "id": max_id + 1,
                    "name": product["name"],
                    "quantity": quantity,
                    "warehouse_id": to_warehouse,
                    "price": product.get("price", 0.0)
                })

            save_data(data)

            write_transaction(
                "TRANSFER",
                productID,
                product["name"],
                quantity,
                from_wh=source_wh,
                to_wh=to_warehouse
            )

            print(textColor("Transfer qilindi", "blue"))
            return

    print(textColor("Mahsulot topilmadi", "red", "blue"))
