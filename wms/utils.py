from rich.console import Console  # type: ignore
from rich.table import Table  # type: ignore
import os
import curses
console = Console()

COLORS = {
    "reset": "\033[0m",
    "red": "\033[31m",
    "blue": "\033[34m",
}

def display_products_table(products, title="📦 Mahsulotlar ro'yxati"):
    if not products:
        console.print("[red]Malumot topilmadi[/red]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID")
    table.add_column("Nomi")
    table.add_column("Soni")
    table.add_column("Narxi")
    table.add_column("Ombor ID")

    for p in products:
        table.add_row(
            str(p.get("id", "-")),
            str(p.get("name", "-")),
            str(p.get("quantity", 0)),
            str(p.get("price", 0)),
            str(p.get("warehouse_id", "-"))
        )

    console.print(table)


def display_tranzaksiya_table(items, title="🔁 Tranzaksiyalar"):
    if not items:
        console.print("[red]Malumot topilmadi[/red]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("Nomi")
    table.add_column("Turi")
    table.add_column("ID")
    table.add_column("Miqdor")
    table.add_column("From")
    table.add_column("To")
    table.add_column("Vaqt")

    for t in items:
        table.add_row(
            str(t.get("product_name", "-")),
            str(t.get("type", "-")),
            str(t.get("product_id", "-")),
            str(t.get("quantity", "-")),
            str(t.get("from", "-")),
            str(t.get("to", "-")),
            str(t.get("timestamp", "-"))
        )

    console.print(table)


def display_warehouse_table(items, title="🏢 Omborlar"):
    if not items:
        console.print("[red]Malumot topilmadi[/red]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID")
    table.add_column("Nomi")
    table.add_column("Hozirgi")
    table.add_column("Sig'im")
    table.add_column("Joylashuv")

    for w in items:
        table.add_row(
            str(w.get("id", "-")),
            str(w.get("name", "-")),
            str(w.get("current", 0)),
            str(w.get("capacity", 0)),
            str(w.get("location", "-"))
        )
    console.print(table)


def textColor(text, *styles):
    code = "".join(COLORS[s] for s in styles if s in COLORS)
    return f"{code}{text}{COLORS['reset']}"


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def run_menu_curses(stdscr, title, options):
    curses.curs_set(0)
    stdscr.keypad(True)
    menu = options
    idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, title, curses.A_BOLD)

        for i, item in enumerate(menu):
            label = item.get("label", "")
            if i == idx:
                stdscr.addstr(i + 2, 2, "> " + label, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 4, label)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(menu) - 1:
            idx += 1
        elif key in (10, 13):
            item = menu[idx]
            if "action" in item:
                if "stdscr" in item["action"].__code__.co_varnames:
                    item["action"](stdscr)
                else:
                    restore_terminal()
                    clear_console()
                    item["action"]()
                    input("\nDavom etish uchun Enter...")
                    stdscr = curses.initscr()
                    curses.curs_set(0)
                    stdscr.keypad(True)
            elif item.get("back"):
                return
            elif item.get("quit"):
                exit()
            elif item.get("logout"):
                item["logout"]()
                exit()


def restore_terminal():
    try:
        curses.endwin()
    except:
        pass
