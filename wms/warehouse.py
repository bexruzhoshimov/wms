from storage import load_data, save_data

def list_warehouses():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    if not whs:
        print("No warehouses defined.")
        return
    print("=== Warehouses ===")
    for w in whs:
        print(f"ID:{w['id']}  Name:{w['name']}")

def add_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    next_id = max([w['id'] for w in whs], default=0) + 1
    name = input("Warehouse name: ").strip()
    whs.append({"id": next_id, "name": name})
    save_data(data)
    print("Warehouse added.")

def update_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    wid = input("Enter warehouse ID to update: ").strip()
    try:
        wid = int(wid)
    except:
        print("Invalid ID"); return
    for w in whs:
        if w['id']==wid:
            w['name'] = input(f"Name ({w['name']}): ").strip() or w['name']
            save_data(data)
            print("Updated.")
            return
    print("Warehouse not found.")

def delete_warehouse():
    data = load_data()
    whs = data.setdefault("warehouses", [])
    wid = input("Enter warehouse ID to delete: ").strip()
    try:
        wid = int(wid)
    except:
        print("Invalid ID"); return
    for w in whs:
        if w['id']==wid:
            products = data.setdefault('products', [])
            for p in products:
                if p.get('warehouse_id')==wid:
                    p['warehouse_id'] = None
            whs.remove(w)
            save_data(data)
            print("Deleted.")
            return
    print("Warehouse not found.")
