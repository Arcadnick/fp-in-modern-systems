"""Консольное меню фильмотеки: порт Program.cs.

Единственное место с вводом-выводом. Каждое действие меню получает текущий
каталог аргументом и возвращает каталог, с которым работать дальше: тот же,
если ничего не изменилось, или новый. Старые каталоги не меняются (copy-on-write),
поэтому их можно хранить для отмены действий.
"""

import traceback
from datetime import datetime

from filmoteka.queries import better_of, genre_matches
from filmoteka.records import with_default_extension
from filmoteka.rules import parse_genres
from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.colors import BLACK_ON_GREEN, BLUE, CYAN, GREEN, RED, RESET
from filmoteka.constructors import make_test_catalog
from filmoteka.exceptions import (
    FilmotekaError,
    IdenticalMoviesException,
    NoDataUploadedException,
    NumberFilmException,
    RatingException,
)
from filmoteka.storage import load_playlist, save_playlist


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
    print(f"{UNDO}. Отменить последнее изменение")
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
    try:
        playlist = load_playlist(filename)
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
        save_playlist(catalog.films, filename)
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
            film = films.at(n)
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
            new_catalog, raised = catalog.raise_rating(film)
            success(f"Рейтинг «{film.title}» успешно поднят на одно значение и составляет {raised.rating}")
            return new_catalog
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


def sort_films(catalog, sort):
    """Общая часть пунктов 7–8: отсортировать каталог функцией sort и показать."""
    check_data(catalog)
    new_catalog = sort(catalog)
    print_playlist(new_catalog.films)
    return new_catalog


def sort_by_name(catalog):
    return sort_films(catalog, Catalog.sorted_by_name)


def sort_by_rating(catalog):
    return sort_films(catalog, Catalog.sorted_by_rating)


def filter_films(catalog):
    check_data(catalog)
    print("1. По жанру")
    print("2. По типу (Film, Cartoon, Serial)")
    choice = input("> ").strip()
    if choice == "1":
        genre = input("Введите жанр: ").strip()
        result = catalog.films.filtered(lambda item: genre_matches(item, genre))
    elif choice == "2":
        kind = input("Введите тип: ").strip()
        types = {"film": Film, "cartoon": Cartoon, "serial": Serial}
        if kind.lower() not in types:
            error("Такого типа нет")
            return catalog
        result = catalog.films.filtered(lambda item: type(item) is types[kind.lower()])
    else:
        error("Введён некорректный пункт")
        return catalog
    if len(result) == 0:
        print("Ничего не найдено")
    else:
        print_playlist(result)
    return catalog


def remove_duplicates(catalog):
    check_data(catalog)
    new_catalog = catalog.without_duplicates()
    print(f"Удалено дубликатов: {len(catalog.films) - len(new_catalog.films)}")
    return new_catalog


def register_viewer(catalog):
    check_data(catalog)
    name = input("Введите имя зрителя: ").strip()
    if name == "":
        error("Имя не введено")
        return catalog
    genres = input("Любимые жанры через запятую (например, Comedy, Adventure): ")
    new_catalog = catalog.with_viewer(name, parse_genres(genres))
    success(f"Зритель {name} зарегистрирован")
    return new_catalog


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


def with_viewer(catalog, action):
    """Общая часть пунктов 12–16: выбрать зрителя и вернуть action(viewer) -> каталог."""
    check_data(catalog)
    viewer = choose_viewer(catalog)
    if viewer is None:
        return catalog
    return action(viewer)


def with_viewer_and_film(catalog, prompt, action):
    """Общая часть пунктов 12–14: выбрать зрителя и фильм и вернуть action(viewer, film) -> каталог."""
    def choose_and_act(viewer):
        film = choose_film(catalog.films, prompt)
        if film is None:
            return catalog
        return action(viewer, film)
    return with_viewer(catalog, choose_and_act)


def watch_film(catalog):
    def watch(viewer, film):
        new_catalog, watched = catalog.watch(viewer, film)
        success(f"{viewer.name} посмотрел(а) «{film.title}». Всего просмотров: {watched.views}")
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для просмотра", watch)


def rate_film(catalog):
    def rate(viewer, film):
        score = int(input("Ваша оценка (1..10): "))
        new_catalog, voted = catalog.rate(viewer, film, score)
        success(f"Оценка принята. Новый рейтинг «{film.title}»: {voted.rating}")
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для оценки", rate)


def add_to_viewer_playlist(catalog):
    def add(viewer, film):
        new_catalog = catalog.add_to_playlist(viewer, film)
        print(f"«{film.title}» добавлен(а) в плейлист {viewer.name}")
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для плейлиста", add)


def viewer_profile(catalog):
    def show(viewer):
        header(f"\nЗритель: {viewer.name}")
        print_lines(viewer.profile_lines())
        return catalog
    return with_viewer(catalog, show)


def recommend(catalog):
    def show(viewer):
        header(f"Рекомендации для {viewer.name}:")
        films = viewer.recommend(catalog.films)
        if len(films) == 0:
            print("  Подходящих произведений не нашлось")
        for film in films:
            print(f"  {film.title} ({film.genre}), рейтинг {film.rating}")
        return catalog
    return with_viewer(catalog, show)


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
    new_catalog = make_test_catalog()
    print(f"{BLACK_ON_GREEN}Данные успешно загружены{RESET}")
    return new_catalog


def write_error_log(err):
    with open("error_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Ошибка: {err}\n")
        log.write(f"Стек вызовов: {traceback.format_exc()}\n")
        log.write(f"{datetime.now()}\n")
        log.write("-" * 150 + "\n")


UNDO = 18

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
    history = []  # прошлые версии каталога для отмены
    while True:
        try:
            choice = print_menu()
            if choice == 0:
                break
            if choice == UNDO:
                if len(history) == 0:
                    error("Отменять нечего")
                else:
                    catalog = history.pop()
                    success("Последнее изменение отменено")
            elif choice in ACTIONS:
                new_catalog = ACTIONS[choice](catalog)
                if new_catalog is not catalog:
                    history.append(catalog)
                    catalog = new_catalog
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
