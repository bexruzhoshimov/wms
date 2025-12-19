from .storage import load_data, save_data
from .utils import textColor, display_warehouse_table, clear_console


def list_warehouses():
    data = load_data()
    warehouses = data.setdefault("warehouses", [])
    display_warehouse_table(warehouses)


def add_warehouse():
    data = load_data()
    warehouses = data.setdefault("warehouses", [])
    name = input("Ombor nomi: ")

    if name == "":
        clear_console()
        print(textColor("Ma'lumot kiritilmadi", "red"))
        return
    location = input("Ombor joylashuvi: ")
    capacity_input = input("Ombor sig'imi: ")

    try:
        capacity = int(capacity_input)
    except:
        capacity = 0

    max_id = 0
    for warehouse in warehouses:
        if warehouse["id"] > max_id:
            max_id = warehouse["id"]

    warehouses.append({
        "id": max_id+1,
        "name": name,
        "location": location,
        "capacity": capacity,
        "current": 0
    })

    save_data(data)
    display_warehouse_table([warehouses[-1]], title="➕ Ombor qo'shildi")


def update_warehouse():
    data = load_data()
    warehouses = data.setdefault("warehouses", [])
    display_warehouse_table(warehouses)
    warehouseID = input("Tahrirlash uchun ombor ID kiriting: ")

    try:
        warehouseID = int(warehouseID)
    except:
        print(textColor("ID noto'g'ri", "red"))
        return

    for warehouse in warehouses:
        if warehouse["id"] == warehouseID:
            new_name = input(f"Nomi ({warehouse['name']}): ")
            new_location = input(f"Joylashuvi ({warehouse['location']}): ")
            new_capacity = input(f"Sig'imi ({warehouse['capacity']}): ")

            if new_name != "":
                warehouse["name"] = new_name

            if new_location != "":
                warehouse["location"] = new_location

            if new_capacity.isdigit():
                warehouse["capacity"] = int(new_capacity)

            save_data(data)
            print(textColor("Tahrirlandi", "blue"))
            return
    print(textColor("Ombor topilmadi", "red"))


def delete_warehouse():
    data = load_data()
    warehouses = data.setdefault("warehouses", [])
    display_warehouse_table(warehouses)
    warehouseID = input("O'chirish uchun ombor ID kiriting: ")

    try:
        warehouseID = int(warehouseID)
    except:
        print(textColor("ID noto'g'ri", "red"))
        return

    for warehouse in warehouses:
        if warehouse["id"] == warehouseID:
            products = data.setdefault("products", [])
            for p in products:
                if p.get("warehouse_id") == warehouseID:
                    p["warehouse_id"] = None

            warehouses.remove(warehouse)
            save_data(data)
            print(textColor("O'chirildi", "blue"))
            return

    print(textColor("Ombor topilmadi", "red"))
