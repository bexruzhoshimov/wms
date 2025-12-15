import os
import sys


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



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')