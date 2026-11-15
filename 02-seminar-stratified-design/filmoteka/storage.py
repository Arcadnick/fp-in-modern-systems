"""Действия с файлами: чтение и запись каталога."""

from filmoteka.catalog import Catalog
from filmoteka.constructors import parse_playlist
from filmoteka.records import playlist_to_lines


def load_catalog(filename):
    with open(filename, encoding="utf-8") as file:
        lines = file.read().splitlines()
    return Catalog(parse_playlist(lines))


def save_catalog(catalog, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(playlist_to_lines(catalog.all_films())) + "\n")
