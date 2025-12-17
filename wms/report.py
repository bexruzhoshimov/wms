from .storage import load_data
import csv, os

try:
    import pandas as pd
except:
    pd = None

def show_summary():
    data = load_data()
    products = data.get('products', [])
    whs = data.get('warehouses', [])
    print('=== Summary ===')
    total_items = sum([p.get('quantity',0) for p in products])
    print(f'Total distinct products: {len(products)}')
    print(f'Total items (sum qty): {total_items}')
    print(f'Warehouses: {len(whs)}')

def export_to_csv(filename='wms_export.csv'):
    data = load_data()
    products = data.get('products', [])
    fieldnames = ['id','name','quantity','warehouse_id','price']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            writer.writerow({k:p.get(k,'') for k in fieldnames})
    print(f'Exported products to {filename}')

def import_from_csv(filename='wms_import.csv'):
    data = load_data()
    products = data.setdefault('products', [])
    if not os.path.exists(filename):
        print('CSV file not found:', filename); return
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pid = int(row.get('id') or 0)
            except:
                pid = None
            name = row.get('name')
            try:
                qty = int(row.get('quantity') or 0)
            except:
                qty = 0
            try:
                wid = int(row.get('warehouse_id') or 0)
            except:
                wid = None
            try:
                price = float(row.get('price') or 0.0)
            except:
                price = 0.0
            exists = next((x for x in products if x.get('id')==pid), None) if pid else None
            if exists:
                exists.update({'name':name,'quantity':qty,'warehouse_id':wid,'price':price})
            else:
                next_id = max([it['id'] for it in products], default=0) + 1
                products.append({'id': next_id, 'name': name, 'quantity': qty, 'warehouse_id': wid, 'price': price})
    from storage import save_data
    save_data(data)
    print('Imported from CSV (or updated existing).')

def export_to_excel(filename='wms_export.xlsx'):
    data = load_data()
    products = data.get('products', [])
    if pd is None:
        print('pandas not installed — exporting CSV instead.'); export_to_csv(filename='wms_export.csv'); return
    df = pd.DataFrame(products)
    df.to_excel(filename, index=False)
    print(f'Exported to {filename} (xlsx)')

def import_from_excel(filename='wms_import.xlsx'):
    data = load_data()
    products = data.setdefault('products', [])
    if pd is None:
        print('pandas not installed — cannot import xlsx. Place CSV named wms_import.csv instead.'); return
    if not os.path.exists(filename):
        print('Excel file not found:', filename); return
    df = pd.read_excel(filename)
    for _, row in df.iterrows():
        try: pid = int(row.get('id') if not pd.isna(row.get('id')) else 0)
        except: pid = None
        name = row.get('name')
        try: qty = int(row.get('quantity') if not pd.isna(row.get('quantity')) else 0)
        except: qty = 0
        try: wid = int(row.get('warehouse_id') if not pd.isna(row.get('warehouse_id')) else 0)
        except: wid = None
        try: price = float(row.get('price') if not pd.isna(row.get('price')) else 0.0)
        except: price = 0.0
        exists = next((x for x in products if x.get('id')==pid), None) if pid else None
        if exists:
            exists.update({'name':name,'quantity':qty,'warehouse_id':wid,'price':price})
        else:
            next_id = max([it['id'] for it in products], default=0) + 1
            products.append({'id': next_id, 'name': name, 'quantity': qty, 'warehouse_id': wid, 'price': price})
    from storage import save_data
    save_data(data)
    print('Imported from Excel and updated data.')
