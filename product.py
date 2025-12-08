from storage import load_data, save_data

def list_products(filter_warehouse=None):
    data = load_data()
    products = data.setdefault("products", [])
    if not products:
        print("No products."); return
    print("=== Products ===")
    for p in products:
        if filter_warehouse and p.get('warehouse_id')!=filter_warehouse:
            continue
        print(f"ID:{p['id']} | Name:{p['name']} | Qty:{p['quantity']} | Warehouse:{p.get('warehouse_id')}")

def add_product():
    data = load_data()
    products = data.setdefault("products", [])
    next_id = max([p['id'] for p in products], default=0) + 1
    name = input("Product name: ").strip()
    qty = input("Initial quantity: ").strip()
    try:
        qty = int(qty)
    except:
        qty = 0
    wid = input("Warehouse ID (leave blank for none): ").strip()
    try:
        wid = int(wid) if wid else None
    except:
        wid = None
    price = input("Price (optional): ").strip()
    try:
        price = float(price) if price else 0.0
    except:
        price = 0.0
    prod = {"id": next_id, "name": name, "quantity": qty, "warehouse_id": wid, "price": price}
    products.append(prod)
    save_data(data)
    print("Product added.")

def update_product():
    data = load_data()
    products = data.setdefault("products", [])
    pid = input("Enter product ID to update: ").strip()
    try:
        pid = int(pid)
    except:
        print("Invalid ID"); return
    for p in products:
        if p['id']==pid:
            p['name'] = input(f"Name ({p['name']}): ") or p['name']
            qty = input(f"Quantity ({p['quantity']}): ").strip()
            if qty:
                try: p['quantity']=int(qty)
                except: pass
            wid = input(f"Warehouse ID ({p.get('warehouse_id')}): ").strip()
            if wid:
                try: p['warehouse_id']=int(wid)
                except: p['warehouse_id']=p.get('warehouse_id')
            price = input(f"Price ({p.get('price')}): ").strip()
            if price:
                try: p['price']=float(price)
                except: pass
            save_data(data)
            print("Product updated."); return
    print("Product not found.")

def delete_product():
    data = load_data()
    products = data.setdefault("products", [])
    pid = input("Enter product ID to delete: ").strip()
    try: pid = int(pid)
    except: print("Invalid ID"); return
    for p in products:
        if p['id']==pid:
            products.remove(p)
            save_data(data)
            print("Deleted."); return
    print("Product not found.")

def search_products():
    data = load_data()
    products = data.setdefault('products', [])
    term = input('Search by name or ID: ').strip().lower()
    found = []
    for p in products:
        if term == str(p.get('id')) or term in p.get('name','').lower():
            found.append(p)
    if not found:
        print('No matches.'); return
    for p in found:
        print(f"ID:{p['id']} | Name:{p['name']} | Qty:{p['quantity']} | Warehouse:{p.get('warehouse_id')}")
