from .storage import load_data, save_data
from .utils import textColor, display_warehouse_table, clear_console


def list_warehouses():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    display_warehouse_table(whs)


def add_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    next_id = max([w['id'] for w in whs], default=0) + 1
    name = input("Ombor nomi: ").strip()
    if (name == ""):
        clear_console()
        print(textColor("Ma'lumot kiritilmadi", "red", "bold"))
    else:
        location = input("Ombor Joylashuvi: ").strip()
        capacityInput = input("Ombor sig'imi: ").strip()
        capacity = int(capacityInput) if capacityInput.isdigit() else 0
        whs.append({"id": next_id, "name": name,
                    "location": location, "capacity": capacity, "current": 0})
        save_data(data)
        display_warehouse_table([whs[-1]], title="➕ Ombor qo'shildi")


def update_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    display_warehouse_table(whs)
    wid = input("Tahrirlash uchun ombor ID kiriting: ").strip()
    try:
        wid = int(wid)
    except:
        print(textColor("ID mavjud emas", "red", "bold"))
        return
    for w in whs:
        if w['id'] == wid:
            w['name'] = input(f"Name ({w['name']}): ").strip() or w['name']
            w['location'] = input(
                f"Sig'imi ({w['location']}): ").strip() or w['location']
            w['capacity'] = int(
                input(f"Sig'imi ({w['capacity']}): ").strip()) or w['capacity']

            save_data(data)
            print(textColor("Tahrirlandi", "blue", "bold"))
            print("")
            return
    print(textColor("Ombor topilmadi", "red", "bold"))


def delete_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    display_warehouse_table(whs)
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
