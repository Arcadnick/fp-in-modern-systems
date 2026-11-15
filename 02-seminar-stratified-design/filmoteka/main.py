"""Цикл меню фильмотеки: порт Main из Program.cs.

Спросить пункт, выполнить команду, запомнить прошлую версию каталога для отмены.
Всё остальное делают слои ниже: команды, диалоги, каталог.
"""

from filmoteka import dialogs
from filmoteka.catalog import Catalog
from filmoteka.commands import COMMANDS
from filmoteka.history import remember

UNDO = 18


def main():
    dialogs.greet()
    catalog, history = Catalog(), ()
    while True:
        try:
            choice = dialogs.ask_menu_choice(UNDO)
            if choice == 0:
                break
            if choice == UNDO:
                catalog, history = dialogs.undo(catalog, history)
            elif choice in COMMANDS:
                new_catalog = COMMANDS[choice](catalog)
                catalog, history = new_catalog, remember(history, catalog, new_catalog)
            else:
                dialogs.wrong_menu_item()
        except EOFError:
            break
        except Exception as e:
            dialogs.report_error(e)
    dialogs.goodbye()
