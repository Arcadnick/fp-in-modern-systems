"""Консольное меню фильмотеки: порт Program.cs.

Единственное место с вводом-выводом. Каждое действие меню получает текущий
каталог аргументом и возвращает каталог, с которым работать дальше.
"""

import traceback
from datetime import datetime

from filmoteka.calculations import better_of, genre_matches, item_at, parse_genres, with_default_extension
from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.colors import BLACK_ON_GREEN, BLUE, CYAN, GREEN, RED, RESET
from filmoteka.exceptions import (
    FilmotekaError,
    IdenticalMoviesException,
    NoDataUploadedException,
    NumberFilmException,
    RatingException,
)
from filmoteka.playlist import Playlist


def success(message):
    print(f"{GREEN}{message}{RESET}")


def error(message):
    print(f"{RED}{message}{RESET}")


def header(message):
    print(f"{CYAN}{message}{RESET}")


def print_lines(lines):
    for line in lines:
        print(line)


def the_first_word():
    print(f"{BLUE}{'=' * 60}")
    print("  Фильмотека: фильмы, мультфильмы и мультсериалы")
    print(f"{'=' * 60}{RESET}")


def print_menu():
    print()
    print("Введите номер функции")
    print(" 1. Загрузить данные из файла")
    print(" 2. Сохранить данные в файл")
    print(" 3. Загрузить тестовые данные")
    print(" 4. Вывести данные на экран")
    print(" 5. Поднять рейтинг фильму на 1")
    print(" 6. Сравнить два фильма")
    print(" 7. Сортировка по названию")
    print(" 8. Сортировка по рейтингу")
    print(" 9. Фильтр по жанру или типу")
    print("10. Удалить дубликаты")
    print("11. Зарегистрировать зрителя")
    print("12. Зритель смотрит фильм")
    print("13. Зритель ставит оценку")
    print("14. Добавить фильм в плейлист зрителя")
    print("15. Профиль зрителя")
    print("16. Рекомендации зрителю")
    print("17. Статистика каталога")
    print(" 0. Выход")
    return int(input("> "))


def check_data(catalog):
    if catalog is None or len(catalog.films) == 0:
        raise NoDataUploadedException()


def print_playlist(playlist):
    print("Список произведений:")
    print_lines(playlist.numbered_lines())


def get_data(catalog):
    filename = input("Введите имя файла (или путь к файлу) с расширением: ").strip()
    if filename == "":
        error("Имя файла не введено")
        return catalog
    playlist = Playlist()
    try:
        playlist.load_from_file(filename)
    except FileNotFoundError:
        error(f"Файл {filename} не найден. Введите корректное имя файла или путь.")
        return catalog
    print(f"{BLACK_ON_GREEN}Данные успешно загружены{RESET}")
    return Catalog(playlist)


def get_file(catalog):
    check_data(catalog)
    filename = input("Введите имя файла, который хотите создать: ").strip()
    if filename == "":
        error("Имя файла не введено")
        return catalog
    if with_default_extension(filename) != filename:
        filename = with_default_extension(filename)
        print("Имя было указано без расширения, поэтому файлу присвоено расширение .txt")
    try:
        catalog.films.save_to_file(filename)
        success(f"Данные сохранены в {filename}")
    except OSError:
        error("Ошибка при выводе данных в файл.")
    return catalog


def writer(catalog):
    check_data(catalog)
    for film in catalog.films:
        print(f"{BLUE}\nИнформация о произведении:{RESET}")
        print_lines(film.details())
        print(film.describe())
    return catalog


def choose_film(films, prompt):
    """Спросить номер произведения. 0 — отказ, вернёт None."""
    print_playlist(films)
    while True:
        try:
            n = int(input(f"{prompt} (0 — выход): "))
            if n == 0:
                return None
            film = item_at(films.get_all(), n)
            if film is not None:
                return film
            raise NumberFilmException()
        except NumberFilmException as e:
            error(e)


def raise_up(catalog):
    check_data(catalog)
    while True:
        film = choose_film(catalog.films, "Введите номер фильма, рейтинг которого хотите поднять")
        if film is None:
            return catalog
        try:
            rating = film.raise_rating()
            success(f"Рейтинг «{film.title}» успешно поднят на одно значение и составляет {rating}")
            return catalog
        except RatingException as e:
            error(e)
            header("Выберите другой фильм или введите 0 для выхода")


def compare(catalog):
    check_data(catalog)
    first = choose_film(catalog.films, "Введите номер первого фильма для сравнения")
    if first is None:
        return catalog
    second = choose_film(catalog.films, "Введите номер второго фильма для сравнения")
    if second is None:
        return catalog
    if first is second:
        raise IdenticalMoviesException()
    better = better_of(first, second)
    if better is None:
        print(f"У фильмов одинаковый рейтинг: {first.rating}")
    else:
        worse = second if better is first else first
        print("У фильмов разный рейтинг")
        print(f"«{better.title}» ({better.rating}) лучше, чем «{worse.title}» ({worse.rating})")
    return catalog


def sort_by_name(catalog):
    check_data(catalog)
    catalog.films.sort_by_name()
    print_playlist(catalog.films)
    return catalog


def sort_by_rating(catalog):
    check_data(catalog)
    catalog.films.sort_by_rating()
    print_playlist(catalog.films)
    return catalog


def filter_films(catalog):
    check_data(catalog)
    print("1. По жанру")
    print("2. По типу (Film, Cartoon, Serial)")
    choice = input("> ").strip()
    if choice == "1":
        genre = input("Введите жанр: ").strip()
        result = catalog.films.find_all(lambda item: genre_matches(item, genre))
    elif choice == "2":
        kind = input("Введите тип: ").strip()
        types = {"film": Film, "cartoon": Cartoon, "serial": Serial}
        if kind.lower() not in types:
            error("Такого типа нет")
            return catalog
        result = catalog.films.find_all(lambda item: type(item) is types[kind.lower()])
    else:
        error("Введён некорректный пункт")
        return catalog
    if result.count == 0:
        print("Ничего не найдено")
    else:
        print_playlist(result)
    return catalog


def remove_duplicates(catalog):
    check_data(catalog)
    removed = catalog.films.remove_duplicates()
    print(f"Удалено дубликатов: {removed}")
    return catalog


def register_viewer(catalog):
    check_data(catalog)
    name = input("Введите имя зрителя: ").strip()
    if name == "":
        error("Имя не введено")
        return catalog
    genres = input("Любимые жанры через запятую (например, Comedy, Adventure): ")
    catalog.register_viewer(name, parse_genres(genres))
    success(f"Зритель {name} зарегистрирован")
    return catalog


def choose_viewer(catalog):
    if len(catalog.viewers) == 0:
        error("Зрителей пока нет, сначала зарегистрируйте зрителя (пункт 11)")
        return None
    print("Зрители: " + ", ".join(viewer.name for viewer in catalog.viewers))
    name = input("Введите имя зрителя: ").strip()
    viewer = catalog.find_viewer(name)
    if viewer is None:
        error(f"Зритель {name} не найден")
    return viewer


def watch_film(catalog):
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is None:
        return catalog
    film = choose_film(catalog.films, "Введите номер фильма для просмотра")
    if film is not None:
        views = viewer.watch(film)
        success(f"{viewer.name} посмотрел(а) «{film.title}». Всего просмотров: {views}")
    return catalog


def rate_film(catalog):
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is None:
        return catalog
    film = choose_film(catalog.films, "Введите номер фильма для оценки")
    if film is None:
        return catalog
    score = int(input("Ваша оценка (1..10): "))
    rating = viewer.rate(film, score)
    success(f"Оценка принята. Новый рейтинг «{film.title}»: {rating}")
    return catalog


def add_to_viewer_playlist(catalog):
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is None:
        return catalog
    film = choose_film(catalog.films, "Введите номер фильма для плейлиста")
    if film is not None:
        viewer.add_to_playlist(film)
        print(f"«{film.title}» добавлен(а) в плейлист {viewer.name}")
    return catalog


def viewer_profile(catalog):
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is not None:
        header(f"\nЗритель: {viewer.name}")
        print_lines(viewer.profile_lines())
    return catalog


def recommend(catalog):
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is None:
        return catalog
    header(f"Рекомендации для {viewer.name}:")
    films = viewer.recommend(catalog.films)
    if len(films) == 0:
        print("  Подходящих произведений не нашлось")
    for film in films:
        print(f"  {film.title} ({film.genre}), рейтинг {film.rating}")
    return catalog


def statistics(catalog):
    check_data(catalog)
    stats = catalog.statistics(top=3)
    header("Средний рейтинг по жанрам:")
    for genre, rating in stats["by_genre"].items():
        print(f"  {genre}: {rating:.1f}")
    header(f"Топ-{len(stats['top'])} по рейтингу:")
    for i, film in enumerate(stats["top"], start=1):
        print(f"  {i}. {film.title} — {film.rating}")
    header("Просмотры:")
    if stats["most_viewed"] is None:
        print("  Пока никто ничего не смотрел")
    else:
        print(f"  Всего просмотров: {stats['total_views']}")
        print(f"  Самое просматриваемое: {stats['most_viewed'].title} ({stats['most_viewed'].views})")
    print(f"  Зрителей зарегистрировано: {stats['viewers']}")
    return catalog


def test_database(catalog):
    film1 = Film("Inception", "Nolan C.", "Fantasy", 2010, 10, 160000000, "Yes")
    film2 = Film("End of Watch", "Ayer D.", "Action", 2012, 5, 20000000, "No")
    film3 = Film("Barbie", "Gerwig G.", "Comedy", 2023, 7, 145000000, "No")
    film4 = Film("The Grand Budapest Hotel", "Anderson W.", "Criminal", 2014, 10, 100000000, "Yes")
    film5 = Serial("Smeshariki", "Chernov D.", "Comedy", 2008, 3, "Krosh, Ejik", "Serial", 180, 2)
    film6 = Cartoon("Cars", "Ranft J.", "Family", 2006, 10, "Mq.Queen", "Full")
    film7 = Serial("Gravity Falls", "Springer A.", "Detective", 2012, 10, "Dipper, Mabel", "Serial", 41, 2)
    film8 = Cartoon("WALL-E", "Stanton A.", "Adventure", 2008, 10, "WALL-E", "Full")
    film9 = Serial("Rick and Morty", "Roiland J.", "Comedy, Science fiction, Adventure", 2013, 8,
                   "Rick, Morty", "Serial", 62, 7)

    movies = Playlist()
    movies.add_last(film1)
    movies.add_last(film2)
    movies.add_last(film3)
    movies.add_last(film4)
    movies.add_last(film5)
    movies.add_last(film6)
    movies.add_last(film7)
    movies.add_last(film8)
    movies.add_last(film9)

    new_catalog = Catalog(movies)
    new_catalog.register_viewer("Алексей", ["Comedy", "Adventure"])
    new_catalog.register_viewer("Мария", ["Fantasy", "Detective", "Family"])
    print(f"{BLACK_ON_GREEN}Данные успешно загружены{RESET}")
    return new_catalog


def write_error_log(err):
    with open("error_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Ошибка: {err}\n")
        log.write(f"Стек вызовов: {traceback.format_exc()}\n")
        log.write(f"{datetime.now()}\n")
        log.write("-" * 150 + "\n")


ACTIONS = {
    1: get_data,
    2: get_file,
    3: test_database,
    4: writer,
    5: raise_up,
    6: compare,
    7: sort_by_name,
    8: sort_by_rating,
    9: filter_films,
    10: remove_duplicates,
    11: register_viewer,
    12: watch_film,
    13: rate_film,
    14: add_to_viewer_playlist,
    15: viewer_profile,
    16: recommend,
    17: statistics,
}


def main():
    the_first_word()
    catalog = None
    while True:
        try:
            choice = print_menu()
            if choice == 0:
                break
            if choice in ACTIONS:
                catalog = ACTIONS[choice](catalog)
            else:
                error("Введён некорректный номер меню")
        except EOFError:
            break
        except ValueError:
            error("Нужно ввести число")
        except FilmotekaError as e:
            error(e)
        except Exception as e:
            write_error_log(e)
            error("Непредвиденная ошибка, подробности в error_log.txt")
    print("До свидания!")
