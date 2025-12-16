from .storage import load_data, save_data
from .utils import clear_console, display_products_table, textColor


def add_product():
    data = load_data()
    print(data["warehouses"])
    products = data.setdefault("products", [])
    next_id = max([p['id'] for p in products], default=0) + 1
    wid = input("Warehouse ID (leave blank for none): ").strip()
    name = input("Mahsulot Nomi: ").strip()
    qty = input("Miqdori: ").strip()
    try:
        qty = int(qty)
    except:
        qty = 0
    try:
        wid = int(wid) if wid else None
    except:
        wid = None
    price = input("Narxi: ").strip()
    try:
        price = float(price) if price else 0.0
    except:
        price = 0.0
    prod = {"id": next_id, "name": name, "quantity": qty,
            "warehouse_id": wid, "price": price}
    products.append(prod)
    save_data(data)
    clear_console()

    display_products_table([prod], title="➕ Mahsulot qo'shildi")


def update_product():
    data = load_data()
    products = data.setdefault("products", [])
    pid = input("Tahrirlash uchun Mahsulot ID kiriting: ").strip()
    try:
        pid = int(pid)
    except:
        print(textColor("ID mavjud emas", "red", "bold"))
        return
    for p in products:
        if p['id'] == pid:
            p['name'] = input(f"Name ({p['name']}): ") or p['name']
            qty = input(f"Quantity ({p['quantity']}): ").strip()
            if qty:
                try:
                    p['quantity'] = int(qty)
                except:
                    pass
            wid = input(f"Warehouse ID ({p.get('warehouse_id')}): ").strip()
            if wid:
                try:
                    p['warehouse_id'] = int(wid)
                except:
                    p['warehouse_id'] = p.get('warehouse_id')
            price = input(f"Price ({p.get('price')}): ").strip()
            if price:
                try:
                    p['price'] = float(price)
                except:
                    pass
            save_data(data)
            print("Mahsulot yangilandi")
            return
    print("Mahsulot topilmadi")


def delete_product():
    data = load_data()
    products = data.setdefault("products", [])
    pid = input("O'chirish uchun mahsulot ID kiriting: ").strip()
    try:
        pid = int(pid)
    except:
        print(textColor("ID mavjud emas", "red", "bold"))
        return
    for p in products:
        if p['id'] == pid:
            products.remove(p)
            save_data(data)
            print("O'chirildi")
            return
    print("Mahsulot topilmadi")


def list_products(filter_warehouse=None):
    data = load_data()
    products = data.setdefault("products", [])

    if filter_warehouse:
        products = [p for p in products if p.get(
            "warehouse_id") == filter_warehouse]

    display_products_table(products, title="📦 Mahsulotlar ro'yxati")


def search_products():
    data = load_data()
    products = data.setdefault("products", [])
    term = input('Qidirish Nomi yoki ID: ').strip().lower()

    found = []
    for p in products:
        if term == str(p.get('id')) or term in p.get('name', '').lower():
            found.append(p)

    display_products_table(found, title=f"🔍 Qidiruv natijasi: {term}")
