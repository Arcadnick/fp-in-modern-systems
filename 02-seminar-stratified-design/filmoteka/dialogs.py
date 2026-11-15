"""Диалоги с пользователем: выбрать, спросить, сообщить.

Собраны из консоли и представления. Ничего не меняют в каталоге — только
спрашивают и показывают; что делать с ответом, решают команды меню.
"""

from filmoteka import console, views
from filmoteka.exceptions import FilmotekaError, NumberFilmException
from filmoteka.history import can_undo, undone
from filmoteka.records import with_default_extension
from filmoteka.rules import parse_genres
from filmoteka.storage import write_error_log


# --- Цикл меню ---

def greet():
    console.banner(views.TITLE)


def goodbye():
    console.show("До свидания!")


def ask_menu_choice(undo):
    console.show()
    console.show_lines(views.menu_lines(undo))
    return console.ask_number("> ")


def wrong_menu_item():
    console.error("Введён некорректный номер меню")


def undo(catalog, history):
    """(каталог, история) после отмены последнего изменения."""
    if not can_undo(history):
        console.error("Отменять нечего")
        return catalog, history
    console.success("Последнее изменение отменено")
    return undone(history)


def report_error(err):
    """Показать ошибку, прервавшую пункт меню. Вызывается внутри except."""
    if isinstance(err, ValueError):
        console.error("Нужно ввести число")
    elif isinstance(err, FilmotekaError):
        console.error(err)
    else:
        write_error_log(err)
        console.error("Непредвиденная ошибка, подробности в error_log.txt")


# --- Выбор произведения и зрителя ---

def show_films(films):
    console.show_lines(views.numbered(films))


def choose_film(catalog, prompt):
    """Спросить номер произведения. 0 — отказ, вернёт None."""
    show_films(catalog.all_films())
    while True:
        try:
            n = console.ask_number(f"{prompt} (0 — выход): ")
            if n == 0:
                return None
            film = catalog.film_at(n)
            if film is not None:
                return film
            raise NumberFilmException()
        except NumberFilmException as e:
            console.error(e)


def choose_viewer(catalog):
    """Спросить имя зрителя. Нет такого зрителя — сообщить и вернуть None."""
    if not catalog.has_viewers():
        console.error("Зрителей пока нет, сначала зарегистрируйте зрителя (пункт 11)")
        return None
    console.show(views.viewers_line(catalog.viewer_names()))
    name = console.ask_text("Введите имя зрителя: ")
    viewer = catalog.find_viewer(name)
    if viewer is None:
        console.error(f"Зритель {name} не найден")
    return viewer


# --- Вопросы ---

def ask_filename():
    """Имя существующего файла или None, если ничего не введено."""
    filename = console.ask_text("Введите имя файла (или путь к файлу) с расширением: ")
    if filename == "":
        console.error("Имя файла не введено")
        return None
    return filename


def ask_new_filename():
    """Имя нового файла (без расширения — с .txt) или None, если ничего не введено."""
    filename = console.ask_text("Введите имя файла, который хотите создать: ")
    if filename == "":
        console.error("Имя файла не введено")
        return None
    if with_default_extension(filename) != filename:
        console.show("Имя было указано без расширения, поэтому файлу присвоено расширение .txt")
    return with_default_extension(filename)


def ask_new_viewer():
    """(имя, любимые жанры) нового зрителя или None, если имя не введено."""
    name = console.ask_text("Введите имя зрителя: ")
    if name == "":
        console.error("Имя не введено")
        return None
    genres = console.ask_text("Любимые жанры через запятую (например, Comedy, Adventure): ")
    return name, parse_genres(genres)


def ask_score():
    return console.ask_number("Ваша оценка (1..10): ")


def ask_filter():
    """("1", жанр) или ("2", тип) — что ввёл пользователь; другой пункт — (пункт, None)."""
    console.show("1. По жанру")
    console.show("2. По типу (Film, Cartoon, Serial)")
    choice = console.ask_text("> ")
    if choice == "1":
        return choice, console.ask_text("Введите жанр: ")
    if choice == "2":
        return choice, console.ask_text("Введите тип: ")
    return choice, None
