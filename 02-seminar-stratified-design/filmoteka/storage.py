"""Действия с файлами: чтение и запись каталога."""

from filmoteka.records import catalog_lines, parse_catalog


def load_catalog(filename):
    with open(filename, encoding="utf-8") as file:
        return parse_catalog(file.read().splitlines())


def save_catalog(catalog, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(catalog_lines(catalog)) + "\n")
