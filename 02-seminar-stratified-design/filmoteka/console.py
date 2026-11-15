"""Консоль: единственное место с input() и print().

Простейшие действия ввода-вывода, из которых собираются диалоги и команды меню.
"""

from filmoteka.colors import BLACK_ON_GREEN, BLUE, CYAN, GREEN, RED, RESET


def show(line=""):
    print(line)


def show_lines(lines):
    for line in lines:
        print(line)


def success(message):
    print(f"{GREEN}{message}{RESET}")


def error(message):
    print(f"{RED}{message}{RESET}")


def header(message):
    print(f"{CYAN}{message}{RESET}")


def notice(message):
    print(f"{BLACK_ON_GREEN}{message}{RESET}")


def card_title(message):
    print(f"{BLUE}{message}{RESET}")


def banner(title):
    print(f"{BLUE}{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}{RESET}")


def show_section(section):
    """Раздел из views: заголовок цветом, затем строки."""
    title, lines = section
    header(title)
    show_lines(lines)


def ask_text(prompt):
    return input(prompt).strip()


def ask_number(prompt):
    """Число от пользователя; не число — ValueError, его обрабатывает цикл меню."""
    return int(input(prompt))
