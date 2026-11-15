"""Формат файла с каталогом: первая строка — количество, затем по произведению в строке.

Строка произведения: «Тип|поле|поле|...», поля — в порядке FIELDS класса.
"""

from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.exceptions import InvalidPropertyException, ReadingFromFileException
from filmoteka.playlist import Playlist


def to_record(film):
    """Film(...) -> «Film|Inception|Nolan C.|...»."""
    return "|".join([type(film).__name__] + [str(getattr(film, name)) for name in film.FIELDS])


def catalog_lines(catalog):
    """Каталог -> строки файла."""
    films = catalog.all_films()
    return [str(len(films))] + [to_record(film) for film in films]


def make_film(parts):
    return Film(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]), int(parts[6]), parts[7])


def make_cartoon(parts):
    return Cartoon(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]), parts[6], parts[7])


def make_serial(parts):
    return Serial(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]), parts[6], parts[7],
                  int(parts[8]), int(parts[9]))


# Первое поле строки файла -> конструктор произведения
MAKERS = {
    "Film": make_film,
    "Cartoon": make_cartoon,
    "Serial": make_serial,
}


def parse_cinematography(line):
    """«Film|Inception|Nolan C.|...» -> Film(...)."""
    parts = line.strip().split("|")
    maker = MAKERS.get(parts[0])
    if maker is None:
        raise InvalidPropertyException(f"Неизвестный тип произведения: {parts[0]}")
    return maker(parts)


def parse_catalog(lines):
    """Строки файла -> каталог без зрителей. Первая строка — количество записей."""
    try:
        n = int(lines[0])
        return Catalog(Playlist([parse_cinematography(line) for line in lines[1:n + 1]]))
    except (ValueError, IndexError, InvalidPropertyException) as e:
        raise ReadingFromFileException(f"Некорректные данные: {e}")


def with_default_extension(filename):
    return filename if "." in filename else filename + ".txt"
