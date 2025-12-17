from .storage import load_data
from .utils import textColor
import csv
import os

pd = None


def show_summary():
    data = load_data()
    products = data.get('products', [])
    whs = data.get('warehouses', [])
    print(textColor("    === Summary ===\n", "white", "bold"))
    total_items = sum([p.get('quantity', 0) for p in products])
    print(f'Mahsulotlar turi: {len(products)}')
    print(f'Mahsulotlar soni: {total_items}')
    print(f'Omborlar soni: {len(whs)}')


def export_to_csv(filename='wms_export.csv'):
    data = load_data()
    products = data.get('products', [])
    fieldnames = ['id', 'name', 'quantity', 'warehouse_id', 'price']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            writer.writerow({k: p.get(k, '') for k in fieldnames})
    print(f'Muvaffaqiyatli export qilindi {filename}')


def import_from_csv(filename='wms_import.csv'):
    data = load_data()
    products = data.setdefault('products', [])
    if not os.path.exists(filename):
        print('CSV file topilmadi:', filename)
        return
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
            exists = next((x for x in products if x.get(
                'id') == pid), None) if pid else None
            if exists:
                exists.update({'name': name, 'quantity': qty,
                              'warehouse_id': wid, 'price': price})
            else:
                next_id = max([it['id'] for it in products], default=0) + 1
                products.append(
                    {'id': next_id, 'name': name, 'quantity': qty, 'warehouse_id': wid, 'price': price})
    from storage import save_data
    save_data(data)
    print('Muvaffaqiyatli import qilindi.')
