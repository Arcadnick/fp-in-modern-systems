"""Действия с файлами: чтение и запись каталога, журнал ошибок."""

import traceback
from datetime import datetime

from filmoteka.catalog import Catalog
from filmoteka.records import films_to_lines, parse_films


def load_catalog(filename):
    with open(filename, encoding="utf-8") as file:
        return Catalog(parse_films(file.read().splitlines()))


def save_catalog(catalog, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(films_to_lines(catalog.all_films())) + "\n")


def write_error_log(err):
    """Дописать ошибку в error_log.txt. Вызывается внутри except: берёт текущий стек."""
    with open("error_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Ошибка: {err}\n")
        log.write(f"Стек вызовов: {traceback.format_exc()}\n")
        log.write(f"{datetime.now()}\n")
        log.write("-" * 150 + "\n")
