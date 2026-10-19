"""Конструкторы: функции, которые собирают объекты предметной области из данных."""

from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.exceptions import InvalidPropertyException, ReadingFromFileException
from filmoteka.playlist import Playlist


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


def parse_playlist(lines):
    """Строки файла -> Playlist. Первая строка — количество записей."""
    try:
        n = int(lines[0])
        return Playlist([parse_cinematography(line) for line in lines[1:n + 1]])
    except (ValueError, IndexError, InvalidPropertyException) as e:
        raise ReadingFromFileException(f"Некорректные данные: {e}")


def make_test_films():
    return [
        Film("Inception", "Nolan C.", "Fantasy", 2010, 10, 160000000, "Yes"),
        Film("End of Watch", "Ayer D.", "Action", 2012, 5, 20000000, "No"),
        Film("Barbie", "Gerwig G.", "Comedy", 2023, 7, 145000000, "No"),
        Film("The Grand Budapest Hotel", "Anderson W.", "Criminal", 2014, 10, 100000000, "Yes"),
        Serial("Smeshariki", "Chernov D.", "Comedy", 2008, 3, "Krosh, Ejik", "Serial", 180, 2),
        Cartoon("Cars", "Ranft J.", "Family", 2006, 10, "Mq.Queen", "Full"),
        Serial("Gravity Falls", "Springer A.", "Detective", 2012, 10, "Dipper, Mabel", "Serial", 41, 2),
        Cartoon("WALL-E", "Stanton A.", "Adventure", 2008, 10, "WALL-E", "Full"),
        Serial("Rick and Morty", "Roiland J.", "Comedy, Science fiction, Adventure", 2013, 8,
               "Rick, Morty", "Serial", 62, 7),
    ]


def make_test_catalog():
    catalog = Catalog(Playlist(make_test_films()))
    catalog.register_viewer("Алексей", ["Comedy", "Adventure"])
    catalog.register_viewer("Мария", ["Fantasy", "Detective", "Family"])
    return catalog
