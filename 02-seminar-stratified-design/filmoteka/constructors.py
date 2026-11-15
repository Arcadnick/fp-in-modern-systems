"""Конструкторы: тестовые данные. Разбор строк файла — в records.py."""

from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial


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
    return (Catalog(make_test_films())
            .with_viewer("Алексей", ["Comedy", "Adventure"])
            .with_viewer("Мария", ["Fantasy", "Detective", "Family"]))
