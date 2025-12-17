from datetime import datetime
from rich.console import Console  # type: ignore
from rich.table import Table  # type: ignore
import os
import sys
import curses

console = Console()
COLORS = {
    "reset": "\033[0m",

    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",

    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",

    "bold": "\033[1m",
    "underline": "\033[4m",
}


def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    pwd = ""
    if os.name == "nt":
        import msvcrt
        while True:
            ch = msvcrt.getch()
            if ch in (b"\r", b"\n"):
                print()
                break
            elif ch == b"\x08":
                if pwd:
                    pwd = pwd[:-1]
                    print("\b \b", end="", flush=True)
            else:
                pwd += ch.decode("utf-8", errors="ignore")
                print("*", end="", flush=True)
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        try:
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\n", "\r"):
                    print()
                    break
                elif ch == "\x7f":  # Backspace
                    if pwd:
                        pwd = pwd[:-1]
                        print("\b \b", end="", flush=True)
                else:
                    pwd += ch
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    return pwd


def display_products_table(products, title="📦 Mahsulotlar ro'yxati"):
    if not products:
        console.print("[red]Malumot topilmadi.[/red]")
        return
    table = Table(
        title=title,
        header_style="bold cyan",
        show_lines=True
    )
    table
    table.add_column("ID", justify="right", style="bold")
    table.add_column("Nomi")
    table.add_column("Soni", justify="right")
    table.add_column("Narxi", justify="right")
    table.add_column("Ombor ID", justify="center")

    for p in products:
        qty_style = "red" if p.get("quantity", 0) <= 0 else "green"
        table.add_row(
            str(p.get("id", "-")),
            p.get("name", "-"),
            f"[{qty_style}]{p.get('quantity', 0)}[/{qty_style}]",
            f"$ {p.get('price', 0)}".replace(".0", ""),
            str(p.get("warehouse_id", "-"))
        )

    console.print(table)


def display_tranzaksiya_table(products, title="🔁 Tranzaksiyalar ro'yxati"):
    if not products:
        console.print("[red]Malumot topilmadi.[/red]")
        return
    table = Table(
        title=title,
        header_style="bold cyan",
        show_lines=True
    )
    table
    table.add_column("Mahsulot Nomi", justify="right", style="bold")
    table.add_column("Turi", justify="right")
    table.add_column("Mahsulot ID", justify="right")
    table.add_column("Miqdor", justify="right")
    table.add_column("Qayerdan", justify="right")
    table.add_column("Qayerga", justify="right")
    table.add_column("Vaqti", justify="right")

    for p in products:
        table.add_row(
            str(p.get("product_name", "-")),
            str(p.get("type", "-")),
            str(p.get("product_id", "-")),
            str(p.get("quantity", "-")),
            str(p.get("from", "-")),
            str(p.get("to", "-")),
            str(to_seconds(p.get("timestamp", "-"))),
        )

    console.print(table)


def display_warehouse_table(products, title="🏢 Omborlar ro'yxati"):
    if not products:
        console.print("[red]Malumot topilmadi.[/red]")
        return
    table = Table(
        title=title,
        header_style="bold cyan",
        show_lines=True
    )
    table.add_column("ID", justify="right", style="bold")
    table.add_column("Nomi")
    table.add_column("Mahsulotlar soni", justify="right")
    table.add_column("Sig'imi", justify="right")
    table.add_column("Location", justify="right")

    for p in products:
        current_style = warehouse_status_color(
            p.get("current", 0), p.get("capacity", 0))
        table.add_row(
            str(p.get("id", "-")),
            p.get("name", "-"),
            f"[{current_style}]{p.get('current', 0)}[/{current_style}]",
            f"{p.get('capacity', 0)}",
            str(p.get("location", "-"))
        )
    console.print(table)


def textColor(text, *styles):
    code = "".join(COLORS[s] for s in styles if s in COLORS)
    return f"{code}{text}{COLORS['reset']}"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_menu_curses(stdscr, title, options, role=None):
    curses.curs_set(0)
    stdscr.keypad(True)
    menu_items = [i for i in options if not i.get(
        "role") or i.get("role") == role]
    idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"=== {title} ===", curses.A_BOLD)
        for i, item in enumerate(menu_items):
            label = item.get("label", "")
            if i == idx:
                stdscr.addstr(i+2, 2, f"> {label}", curses.A_REVERSE)
            else:
                stdscr.addstr(i+2, 4, label)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(menu_items)-1:
            idx += 1
        elif key in (10, 13):
            item = menu_items[idx]
            if item.get("action"):
                func = item["action"]
                if func.__name__ in ["warehouse_menu", "product_menu", "reports_menu", "transaction_menu"]:
                    func(stdscr)
                else:
                    restore_terminal()
                    clear_console()
                    func()
                    try:
                        input("\nDavom etish uchun Enter tugmasini bosing...")
                    except:
                        pass
                    stdscr = curses.initscr()
                    curses.curs_set(0)
                    stdscr.keypad(True)
            elif item.get("quit"):
                clear_console()
                exit()
            elif item.get("back"):
                return
            elif item.get("logout"):
                item["logout"]()
                exit()
                return


def restore_terminal():
    try:
        curses.endwin()
    except curses.error:
        pass
    if os.name != 'nt':
        os.system('stty sane')


def warehouse_status_color(current: int, capacity: int) -> str:
    if capacity <= 0:
        return "gray"

    percent = (current / capacity) * 100

    if percent <= 60:
        return "green"
    elif percent <= 80:
        return "yellow"
    elif percent <= 100:
        return "red"
    else:
        return "gray"


def to_seconds(timestamp: str) -> str:
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S")
