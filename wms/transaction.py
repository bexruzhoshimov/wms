from .storage import load_data, save_data
from datetime import datetime

def list_transactions():
    data = load_data()
    tx = data.setdefault('transactions', [])
    if not tx:
        print('No transactions.'); return
    for t in tx:
        print(f"{t['timestamp']} | {t['type']} | PID:{t.get('product_id')} | QTY:{t.get('quantity')} | From:{t.get('from')} | To:{t.get('to')}")

def write_transaction(t_type, product_id, quantity, from_wh=None, to_wh=None):
    data = load_data()
    tx = data.setdefault('transactions', [])
    tx.append({
        'timestamp': datetime.now().isoformat(sep=' '),
        'type': t_type,
        'product_id': product_id,
        'quantity': quantity,
        'from': from_wh,
        'to': to_wh
    })
    save_data(data)

def inbound():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input('Product ID for inbound: ').strip()
    try: pid = int(pid)
    except: print('Invalid ID'); return
    qty = input('Quantity to add: ').strip()
    try: qty = int(qty)
    except: print('Invalid qty'); return
    for p in products:
        if p['id']==pid:
            p['quantity'] += qty
            save_data(data)
            write_transaction('INBOUND', pid, qty, from_wh=None, to_wh=p.get('warehouse_id'))
            print('Inbound done.'); return
    print('Product not found.')

def outbound():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input('Product ID for outbound: ').strip()
    try: pid = int(pid)
    except: print('Invalid ID'); return
    qty = input('Quantity to remove: ').strip()
    try: qty = int(qty)
    except: print('Invalid qty'); return
    for p in products:
        if p['id']==pid:
            if p['quantity'] < qty:
                print('Not enough stock!'); return
            p['quantity'] -= qty
            save_data(data)
            write_transaction('OUTBOUND', pid, qty, from_wh=p.get('warehouse_id'), to_wh=None)
            print('Outbound done.'); return
    print('Product not found.')

def transfer():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input('Product ID to transfer: ').strip()
    try: pid = int(pid)
    except: print('Invalid ID'); return
    to_w = input('Destination warehouse ID: ').strip()
    try: to_w = int(to_w)
    except: print('Invalid warehouse ID'); return
    qty = input('Quantity to move: ').strip()
    try: qty = int(qty)
    except: print('Invalid qty'); return
    for p in products:
        if p['id']==pid:
            if p['quantity'] < qty:
                print('Not enough stock to transfer'); return
            src_w = p.get('warehouse_id')
            p['quantity'] -= qty
            found = None
            for q in products:
                if q['name']==p['name'] and q.get('warehouse_id')==to_w:
                    found = q; break
            if found:
                found['quantity'] += qty
            else:
                next_id = max([it['id'] for it in products], default=0) + 1
                products.append({'id': next_id, 'name': p['name'], 'quantity': qty, 'warehouse_id': to_w, 'price': p.get('price',0.0)})
            save_data(data)
            write_transaction('TRANSFER', pid, qty, from_wh=src_w, to_wh=to_w)
            print('Transfer done.'); return
    print('Product not found.')
