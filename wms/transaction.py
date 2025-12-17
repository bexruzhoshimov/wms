from .storage import load_data, save_data
from datetime import datetime
from .utils import clear_console, textColor, display_tranzaksiya_table


def list_transactions():
    data = load_data()
    tx = data.setdefault('transactions', [])
    display_tranzaksiya_table(tx)


def write_transaction(t_type, product_id, product_name, quantity, from_wh=None, to_wh=None):
    data = load_data()
    tx = data.setdefault('transactions', [])
    tx.append({
        'timestamp': datetime.now().isoformat(sep=' '),
        'type': t_type,
        'product_id': product_id,
        'product_name': product_name,
        'quantity': quantity,
        'from': from_wh,
        'to': to_wh
    })
    save_data(data)


def inbound():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input('Kirim uchun Mahsulot ID kiritig: ').strip()
    try:
        pid = int(pid)
    except:
        clear_console()
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red", "bold"))
        return
    qty = input("Qo'shiladigan miqdor: ").strip()
    try:
        qty = int(qty)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red", "bold"))
        return
    for p in products:
        if p['id'] == pid:
            p['quantity'] += qty
            save_data(data)
            write_transaction('Kirim', pid, p['name'], qty, from_wh=None,
                              to_wh=p.get('warehouse_id'))
            print(textColor("Kirim qilindi", "blue", "bold"))
            return
    print(textColor("Mahsulot topilmadi", "red", "bold"))


def outbound():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input('Chiqim uchun Mahsulot ID kiritig: ').strip()
    try:
        pid = int(pid)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red", "bold"))
        return
    qty = input("Ayiriladigan miqdor: ").strip()
    try:
        qty = int(qty)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red", "bold"))
        return
    for p in products:
        if p['id'] == pid:
            if p['quantity'] < qty:
                print('Mahsulot yetarli miqdorda emas')
                return
            p['quantity'] -= qty
            save_data(data)
            write_transaction('Chiqim', pid, p['name'], qty,
                              from_wh=p.get('warehouse_id'), to_wh=None)
            print(textColor("Chiqim qilindi", "blue", "bold"))
            return
    print(textColor("Mahsulot topilmadi", "red", "blue"))


def transfer():
    data = load_data()
    products = data.setdefault('products', [])
    pid = input("Transfer mahsulot ID: ").strip()
    try:
        pid = int(pid)
    except:
        print(textColor("Mahsulot topilmadi", "red", "blue"))
        return
    to_w = input('Ombor ID: ').strip()
    try:
        to_w = int(to_w)
    except:
        print(textColor("Ombor topilmadi", "red", "blue"))
        return
    qty = input("Ko'chirish miqdori: ").strip()
    try:
        qty = int(qty)
    except:
        print(textColor("Ma'lumot to'g'ri kiritilmadi", "red", "bold"))
        return
    for p in products:
        if p['id'] == pid:
            if p['quantity'] < qty:
                print("O'tkazish uchun yetarli miqdor yo'q")
                return
            src_w = p.get('warehouse_id')
            p['quantity'] -= qty
            found = None
            for q in products:
                if q['name'] == p['name'] and q.get('warehouse_id') == to_w:
                    found = q
                    break
            if found:
                found['quantity'] += qty
            else:
                next_id = max([it['id'] for it in products], default=0) + 1
                products.append(
                    {'id': next_id, 'name': p['name'], 'quantity': qty, 'warehouse_id': to_w, 'price': p.get('price', 0.0)})
            save_data(data)
            write_transaction('TRANSFER', pid, "", qty, from_wh=src_w, to_wh=to_w)
            print(textColor("Transfer qilindi", "blue", "bold"))
            return
    print(textColor("Mahsulot topilmadi", "red", "blue"))
