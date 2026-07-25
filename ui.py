import sys

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    GOLD = '\033[33m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def header(title):
    width = 58
    print(f"\n{Colors.BOLD}{Colors.PURPLE}╔{'═' * (width - 2)}╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}║ {title.center(width - 4)} ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}╚{'═' * (width - 2)}╝{Colors.END}\n")

def subheader(text):
    print(f"{Colors.BOLD}{Colors.CYAN}➤ {text}{Colors.END}")

def success(text):
    print(f"{Colors.GREEN}✔ {text}{Colors.END}")

def failure(text):
    print(f"{Colors.RED}✘ {text}{Colors.END}")

def print_kv(key, value, color=Colors.GOLD):
    print(f"  {Colors.BOLD}{key:18}{Colors.END} : {color}{value}{Colors.END}")

class Table:
    def __init__(self, headers, widths):
        self.headers = headers
        self.widths = widths
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def render(self):
        sep_top = "┌" + "┬".join("─" * w for w in self.widths) + "┐"
        sep_mid = "├" + "┼".join("─" * w for w in self.widths) + "┤"
        sep_bot = "└" + "┴".join("─" * w for w in self.widths) + "┘"
        print(sep_top)
        hdr = "│" + "│".join(f" {h}".ljust(w) for h, w in zip(self.headers, self.widths)) + "│"
        print(f"{Colors.BOLD}{hdr}{Colors.END}")
        print(sep_mid)
        for row in self.rows:
            cells = []
            for r, w in zip(row, self.widths):
                s = str(r)
                visible_len = len(s) - sum(10 for c in s if c == '\033')
                cells.append(f" {s}{' ' * (w - 1 - visible_len)}" if visible_len < w else f" {s[:w-1]}")
            print("│" + "│".join(cells) + "│")
        print(sep_bot)
