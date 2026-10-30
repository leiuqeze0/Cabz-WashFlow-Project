# ============================================================
# CABZ LAUNDRY SYSTEM - GENERAL UTILITIES (CONSOLE DESIGN)
# ============================================================
# Ang tanang "hitsura" sa console naa dinhi: boxes, tables,
# colors, ug menu styles. Ang ubang files mo-tawag ra niini
# para parehas ang design sa tanang screen.
# ============================================================

import os
import sys
import textwrap

from config import USE_COLORS

# Para dili mag-error ang box characters sa Windows console
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Kini nag-enable sa colors sa Windows terminal
if os.name == "nt":
    os.system("")

WIDTH = 70

# Colors mugawas lang kung naa sa tinuod nga terminal
COLOR_ON = USE_COLORS and sys.stdout.isatty() and not os.environ.get("NO_COLOR")

# Tanang colors naa dinhi. Kung gusto nimo usbon ang color,
# usba lang ang numero human sa "38;5;" (0-255).
# Soft ug dili hayag sa mata, ug klaro ang mga label (dili na gray nga hapaw).

def hex_color(code, bold=False, background=False):
    """'#5fafd7' -> ANSI code para sa terminal."""
    code = code.lstrip("#")
    r, g, b = int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16)
    kind = 48 if background else 38
    text = f"{kind};2;{r};{g};{b}"
    return ("1;" + text) if bold else text

STYLES = {
    "bold":       "1",
    "cyan":       "38;5;74",        # borders / frames  (soft teal-blue)
    "green":      "38;5;114",       # success, READY     (soft green)
    "yellow":     "38;5;179",       # NOT READY          (soft amber)
    "red":        "38;5;167",       # errors             (soft red)
    "title":      "1;38;5;255",     # title text         (bright white, bold)
    "subtitle":   "38;5;152",       # title subtext      (pale cyan)
    "heading":    "1;38;5;179",     # section headings   (soft gold, bold)
    "label":      "38;5;146",       # field labels       (light lavender-gray)
    "muted":      "38;5;103",       # divider lines      (muted violet-gray)
    "hint":       "38;5;250",       # hint text          (light gray)
    "key":        "1;38;5;79",      # menu numbers [1]   (mint, bold)
    "ok":         "1;38;5;114",     # [✓] success tag
    "bad":        "1;38;5;167",     # [x] error tag
    "caution":    "1;38;5;215",     # [!] warning tag    (soft orange)
    "note":       "1;38;5;110",     # [i] info tag       (soft blue)
    "total":      "1;38;5;114",     # TOTAL SERVICE CHARGE value
    "badge_green":  "1;38;5;16;48;5;114",   # READY TO PICK UP badge
    "badge_yellow": "1;38;5;16;48;5;179",   # NOT READY badge
}


# ============================================================
# COLORS
# ============================================================

def paint(text, *styles):
    """Butangan og color ang text (kung naka-on ang colors)."""

    if not COLOR_ON:
        return text

    codes = ";".join(STYLES[style] for style in styles)
    return f"\033[{codes}m{text}\033[0m"


def badge(status):
    """Pickup status nga naay color: green kung ready, yellow kung dili pa."""

    if not COLOR_ON:
        return status

    if status.startswith("READY"):
        return paint(f" {status} ", "badge_green")

    return paint(f" {status} ", "badge_yellow")


# ============================================================
# TITLES AND SECTIONS
# ============================================================

def banner(title, *subtitles):
    """Dako nga title box sa ibabaw sa kada screen."""

    inner = WIDTH - 2

    print()
    print(paint("╔" + "═" * inner + "╗", "cyan"))
    print(paint("║", "cyan") + paint(title.center(inner), "title") + paint("║", "cyan"))

    for subtitle in subtitles:
        print(paint("║", "cyan") + paint(subtitle.center(inner), "subtitle") + paint("║", "cyan"))

    print(paint("╚" + "═" * inner + "╝", "cyan"))


def section(title):
    """Gamay nga heading sulod sa screen."""

    print()
    print("  " + paint(title, "heading"))
    print("  " + paint("─" * (WIDTH - 4), "muted"))


def rule():
    print("  " + paint("─" * (WIDTH - 4), "muted"))


def display_header():
    """Main header sa programa."""

    banner(
        "C A B Z   W A S H F L O W",
        "Laundry Services and Pickup Status",
        "CABZ Laundry Hub",
    )


# ============================================================
# LINES OF TEXT
# ============================================================

def field(label, value, bold=False):
    """Usa ka linya pareha sa:  Customer Name        : James"""

    label_text = label.ljust(22)
    value_text = str(value)

    if bold:
        print("  " + paint(label_text, "title") + paint(": ", "muted") + paint(value_text, "total"))
    else:
        print("  " + paint(label_text, "label") + paint(": ", "muted") + value_text)


def menu_item(key, text):
    print("  " + paint(f"[{key}]", "key") + "  " + text)


def success(message):
    print("  " + paint("[✓]", "ok") + " " + message)


def error(message):
    print("  " + paint("[x]", "bad") + " " + message)


def warn(message):
    print("  " + paint("[!]", "caution") + " " + message)


def info(message):
    print("  " + paint("[i]", "note") + " " + message)


def hint(message):
    print("  " + paint(message, "hint"))


def ask(text):
    """Pangutana sa user (parehas ra sa input() pero mas nindot tan-awon)."""

    return input("  » " + text)


def pause():
    input("\n  » Press Enter to continue...")


# ============================================================
# BOXES AND TABLES
# ============================================================

def box(lines, color="cyan"):
    """Gamay nga box para sa importanteng mensahe."""

    content_width = WIDTH - 8
    wrapped = []

    for line in lines:
        wrapped.extend(textwrap.wrap(line, content_width) or [""])

    print()
    print("  " + paint("┌" + "─" * (content_width + 2) + "┐", color))

    for line in wrapped:
        print(
            "  " + paint("│", color) + " "
            + line.ljust(content_width) + " "
            + paint("│", color)
        )

    print("  " + paint("└" + "─" * (content_width + 2) + "┘", color))


def fit(text, width):
    """Putlon ang text kung taas kaayo, para dili mabuak ang table."""

    text = str(text)

    if len(text) > width:
        text = text[: width - 1] + "…"

    return text.ljust(width)


def table(headers, widths, rows, status_col=None):
    """
    Mag-print og table nga naay borders.
    headers    - listahan sa column titles
    widths     - gilapdon sa matag column
    rows       - listahan sa rows (matag row kay listahan sa values)
    status_col - index sa column nga Pickup Status (para kolor-an)
    """

    def border(left, middle, right):
        return "  " + paint(
            left + middle.join("─" * (w + 2) for w in widths) + right,
            "cyan",
        )

    bar = paint("│", "cyan")

    print(border("┌", "┬", "┐"))

    head_cells = [paint(fit(h, w), "title") for h, w in zip(headers, widths)]
    print("  " + bar + (" " + (" " + bar + " ").join(head_cells) + " ") + bar)

    print(border("├", "┼", "┤"))

    for row in rows:
        cells = []

        for index, (value, w) in enumerate(zip(row, widths)):
            cell = fit(value, w)

            if index == status_col and COLOR_ON:
                color = "green" if str(value).startswith("READY") else "yellow"
                cell = paint(cell, color)

            cells.append(cell)

        print("  " + bar + (" " + (" " + bar + " ").join(cells) + " ") + bar)

    print(border("└", "┴", "┘"))
