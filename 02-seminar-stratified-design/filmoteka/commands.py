"""Команды меню: порт пунктов Program.cs.

Каждая команда получает текущий каталог и возвращает каталог, с которым
работать дальше: тот же, если ничего не изменилось, или новый (copy-on-write).
Команда только спрашивает через диалоги, вызывает каталог и показывает
результат: текст берётся из views, печатает консоль.
"""

from filmoteka import console, dialogs, views
from filmoteka.catalog import Catalog
from filmoteka.constructors import make_test_catalog
from filmoteka.exceptions import RatingException
from filmoteka.storage import load_catalog, save_catalog


def load_from_file(catalog):
    filename = dialogs.ask_filename()
    if filename is None:
        return catalog
    try:
        new_catalog = load_catalog(filename)
    except FileNotFoundError:
        console.error(f"Файл {filename} не найден. Введите корректное имя файла или путь.")
        return catalog
    console.notice("Данные успешно загружены")
    return new_catalog


def save_to_file(catalog):
    catalog.check_not_empty()
    filename = dialogs.ask_new_filename()
    if filename is None:
        return catalog
    try:
        save_catalog(catalog, filename)
        console.success(f"Данные сохранены в {filename}")
    except OSError:
        console.error("Ошибка при выводе данных в файл.")
    return catalog


def load_test_data(catalog):
    new_catalog = make_test_catalog()
    console.notice("Данные успешно загружены")
    return new_catalog


def show_all(catalog):
    catalog.check_not_empty()
    for film in catalog.all_films():
        console.card_title("\nИнформация о произведении:")
        console.show_lines(views.film_details(film))
    return catalog


def raise_rating(catalog):
    catalog.check_not_empty()
    while True:
        film = dialogs.choose_film(catalog, "Введите номер фильма, рейтинг которого хотите поднять")
        if film is None:
            return catalog
        try:
            new_catalog, raised = catalog.raise_rating(film)
            console.success(views.raised_message(raised))
            return new_catalog
        except RatingException as e:
            console.error(e)
            console.header("Выберите другой фильм или введите 0 для выхода")


def compare(catalog):
    catalog.check_not_empty()
    first = dialogs.choose_film(catalog, "Введите номер первого фильма для сравнения")
    if first is None:
        return catalog
    second = dialogs.choose_film(catalog, "Введите номер второго фильма для сравнения")
    if second is None:
        return catalog
    console.show_lines(views.comparison_lines(catalog.compare(first, second)))
    return catalog


def sort_films(catalog, sort):
    """Общая часть пунктов 7–8: отсортировать каталог функцией sort и показать."""
    catalog.check_not_empty()
    new_catalog = sort(catalog)
    dialogs.show_films(new_catalog.all_films())
    return new_catalog


def sort_by_name(catalog):
    return sort_films(catalog, Catalog.sorted_by_name)


def sort_by_rating(catalog):
    return sort_films(catalog, Catalog.sorted_by_rating)


def filter_films(catalog):
    catalog.check_not_empty()
    choice, query = dialogs.ask_filter()
    if choice == "1":
        result = catalog.films_of_genre(query)
    elif choice == "2":
        result = catalog.films_of_kind(query)
        if result is None:
            console.error("Такого типа нет")
            return catalog
    else:
        console.error("Введён некорректный пункт")
        return catalog
    if len(result) == 0:
        console.show("Ничего не найдено")
    else:
        dialogs.show_films(result)
    return catalog


def remove_duplicates(catalog):
    catalog.check_not_empty()
    new_catalog, removed = catalog.without_duplicates()
    console.show(views.duplicates_message(removed))
    return new_catalog


def register_viewer(catalog):
    catalog.check_not_empty()
    answer = dialogs.ask_new_viewer()
    if answer is None:
        return catalog
    name, genres = answer
    new_catalog = catalog.with_viewer(name, genres)
    console.success(views.registered_message(name))
    return new_catalog


def with_viewer(catalog, action):
    """Общая часть пунктов 12–16: выбрать зрителя и вернуть action(viewer) -> каталог."""
    catalog.check_not_empty()
    viewer = dialogs.choose_viewer(catalog)
    if viewer is None:
        return catalog
    return action(viewer)


def with_viewer_and_film(catalog, prompt, action):
    """Общая часть пунктов 12–14: выбрать зрителя и фильм и вернуть action(viewer, film) -> каталог."""
    def choose_and_act(viewer):
        film = dialogs.choose_film(catalog, prompt)
        if film is None:
            return catalog
        return action(viewer, film)
    return with_viewer(catalog, choose_and_act)


def watch_film(catalog):
    def watch(viewer, film):
        new_catalog, watched = catalog.watch(viewer, film)
        console.success(views.watched_message(viewer, watched))
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для просмотра", watch)


def rate_film(catalog):
    def rate(viewer, film):
        new_catalog, voted = catalog.rate(viewer, film, dialogs.ask_score())
        console.success(views.rated_message(voted))
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для оценки", rate)


def add_to_viewer_playlist(catalog):
    def add(viewer, film):
        new_catalog = catalog.add_to_playlist(viewer, film)
        console.show(views.added_message(viewer, film))
        return new_catalog
    return with_viewer_and_film(catalog, "Введите номер фильма для плейлиста", add)


def viewer_profile(catalog):
    def show(viewer):
        console.show_section(views.profile_section(viewer))
        return catalog
    return with_viewer(catalog, show)


def recommend(catalog):
    def show(viewer):
        console.show_section(views.recommendations_section(viewer, catalog.recommendations_for(viewer)))
        return catalog
    return with_viewer(catalog, show)


def statistics(catalog):
    catalog.check_not_empty()
    for section in views.statistics_sections(catalog.statistics(top=3)):
        console.show_section(section)
    return catalog


# Номер пункта меню -> команда
COMMANDS = {
    1: load_from_file,
    2: save_to_file,
    3: load_test_data,
    4: show_all,
    5: raise_rating,
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
