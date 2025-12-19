from .storage import load_data, save_data
import csv
import os

def show_summary():
    data = load_data()
    products = data["products"]
    warehouses = data["warehouses"]
    print("    === Summary ===\n")

    total_items = 0
    for p in products:
        total_items += p.get("quantity", 0)

    print("Mahsulotlar turi:", len(products))
    print("Mahsulotlar soni:", total_items)
    print("Omborlar soni:", len(warehouses))

def export_to_csv(filename="wms_export.csv"):
    data = load_data()
    products = data["products"]
    fieldnames = ["id", "name", "quantity", "warehouse_id", "price"]

    f = open(filename, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for p in products:
        row = {}
        for key in fieldnames:
            if key in p:
                row[key] = p[key]
            else:
                row[key] = ""
        writer.writerow(row)

    f.close()
    print("Muvaffaqiyatli export qilindi:", filename)

def import_from_csv(filename="wms_import.csv"):
    data = load_data()
    products = data["products"]

    if not os.path.exists(filename):
        print("CSV file topilmadi:", filename)
        return

    f = open(filename, "r", encoding="utf-8")
    reader = csv.DictReader(f)

    for row in reader:
        try:
            productID = int(row["id"])
        except:
            productID = None

        name = row.get("name")

        try:
            quantity = int(row.get("quantity"))
        except:
            quantity = 0

        try:
            warehouseID = int(row.get("warehouse_id"))
        except:
            warehouseID = None

        try:
            price = float(row.get("price"))
        except:
            price = 0.0

        found = None
        if productID is not None:
            for p in products:
                if p["id"] == productID:
                    found = p
                    break

        if found is not None:
            found["name"] = name
            found["quantity"] = quantity
            found["warehouse_id"] = warehouseID
            found["price"] = price
        else:
            max_id = 0
            for p in products:
                if p["id"] > max_id:
                    max_id = p["id"]

            new_product = {
                "id": max_id + 1,
                "name": name,
                "quantity": quantity,
                "warehouse_id": warehouseID,
                "price": price
            }
            products.append(new_product)

    f.close()
    save_data(data)
    print("Muvaffaqiyatli import qilindi.")
