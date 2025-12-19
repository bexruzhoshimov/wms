import json
DATA_FILE = "data.json"

def load_data():
    try:
        f = open(DATA_FILE, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        return {}
    except:
        return {}


def save_data(data):
    f = open(DATA_FILE, "w", encoding="utf-8")
    json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()
