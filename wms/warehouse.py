from .storage import load_data, save_data
from .utils import textColor, clear_console


def list_warehouses():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    if not whs:
        print(textColor("Ombor mavjud emas", "red"))
        return
    clear_console()
    print(textColor("\n=== Warehouses ===\n", "green", "bold"))
    for w in whs:
        print(f"ID:{w['id']}  Name:{w['name']}")


def add_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    next_id = max([w['id'] for w in whs], default=0) + 1
    name = input("Warehouse name: ").strip()
    whs.append({"id": next_id, "name": name})
    save_data(data)
    print("Ombor qo'shildi")


def update_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    wid = input("Tahrirlash uchun ombor ID kiriting: ").strip()
    try:
        wid = int(wid)
    except:
        print(textColor("ID mavjud emas", "red", "bold"))
        return
    for w in whs:
        if w['id'] == wid:
            w['name'] = input(f"Name ({w['name']}): ").strip() or w['name']
            save_data(data)
            print(textColor("Tahrirlandi", "blue", "bold"))
            print("")
            return
    print(textColor("Ombor topilmadi", "red", "bold"))


def delete_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    wid = input("O'chirish uchun ombor ID kiriting: ").strip()
    try:
        wid = int(wid)
    except:
        print(textColor("ID mavjud emas", "red", "bold"))
        return
    for w in whs:
        if w['id'] == wid:
            products = data.setdefault('products', [])
            for p in products:
                if p.get('warehouse_id') == wid:
                    p['warehouse_id'] = None
            whs.remove(w)
            save_data(data)
            print("O'chirildi")
            return
    print("Ombor topilmadi")
