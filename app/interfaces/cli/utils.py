import os
import sys

def is_pycharm() -> bool:
    return os.getenv("PYCHARM_HOSTED") == "1"

def is_real_terminal() -> bool:
    return sys.stdout.isatty()

def clear_screen():
    if not is_real_terminal:
        return
    elif os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')