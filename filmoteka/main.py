"""Консольное меню фильмотеки: порт Program.cs."""

import traceback
from datetime import datetime

from filmoteka.calculations import better_of, genre_matches, item_at, parse_genres, with_default_extension
from filmoteka.catalog import Catalog
from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.colors import BLACK_ON_GREEN, BLUE, CYAN, GREEN, RED, RESET
from filmoteka.exceptions import (
    EmptyPlaylistException,
    IdenticalMoviesException,
    NoDataUploadedException,
    NumberFilmException,
    RatingException,
    ReadingFromFileException,
)
from filmoteka.playlist import Playlist

# Текущий каталог. None — данные ещё не загружены.
catalog = None


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


def check_data():
    if catalog is None or len(catalog.films) == 0:
        raise NoDataUploadedException()


def get_data():
    global catalog
    filename = input("Введите имя файла (или путь к файлу) с расширением: ").strip()
    if filename == "":
        print(f"{RED}Имя файла не введено{RESET}")
        return
    try:
        playlist = Playlist()
        playlist.load_from_file(filename)
        catalog = Catalog(playlist)
    except FileNotFoundError:
        print(f"{RED}Файл {filename} не найден. Введите корректное имя файла или путь.{RESET}")


def get_file():
    check_data()
    filename = input("Введите имя файла, который хотите создать: ").strip()
    if filename == "":
        print(f"{RED}Имя файла не введено{RESET}")
        return
    if with_default_extension(filename) != filename:
        filename = with_default_extension(filename)
        print("Имя было указано без расширения, поэтому файлу присвоено расширение .txt")
    try:
        catalog.films.save_to_file(filename)
        print(f"{GREEN}Данные сохранены в {filename}{RESET}")
    except OSError:
        print(f"{RED}Ошибка при выводе данных в файл.{RESET}")


def writer():
    check_data()
    for film in catalog.films:
        film.print_data()
        film.describe()


def choose_film(prompt):
    """Спросить номер произведения в каталоге. 0 — отказ, вернёт None."""
    catalog.films.print_all()
    while True:
        try:
            n = int(input(f"{prompt} (0 — выход): "))
            if n == 0:
                return None
            film = item_at(catalog.films.get_all(), n)
            if film is not None:
                return film
            raise NumberFilmException()
        except NumberFilmException:
            pass


def raise_up():
    check_data()
    while True:
        film = choose_film("Введите номер фильма, рейтинг которого хотите поднять")
        if film is None:
            return
        try:
            film.raise_rating()
            return
        except RatingException as e:
            print(e)
            print(f"{CYAN}Выберите другой фильм или введите 0 для выхода{RESET}")


def compare():
    check_data()
    first = choose_film("Введите номер первого фильма для сравнения")
    if first is None:
        return
    second = choose_film("Введите номер второго фильма для сравнения")
    if second is None:
        return
    try:
        if first is second:
            raise IdenticalMoviesException()
    except IdenticalMoviesException:
        return
    better = better_of(first, second)
    if better is None:
        print(f"У фильмов одинаковый рейтинг: {first.rating}")
    else:
        worse = second if better is first else first
        print("У фильмов разный рейтинг")
        print(f"«{better.title}» ({better.rating}) лучше, чем «{worse.title}» ({worse.rating})")


def sort_by_name():
    check_data()
    catalog.films.sort_by_name()
    catalog.films.print_all()


def sort_by_rating():
    check_data()
    catalog.films.sort_by_rating()
    catalog.films.print_all()


def filter_films():
    check_data()
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
            print(f"{RED}Такого типа нет{RESET}")
            return
        result = catalog.films.find_all(lambda item: type(item) is types[kind.lower()])
    else:
        print(f"{RED}Введён некорректный пункт{RESET}")
        return
    if result.count == 0:
        print("Ничего не найдено")
    else:
        result.print_all()


def remove_duplicates():
    check_data()
    catalog.films.remove_duplicates()


def register_viewer():
    check_data()
    name = input("Введите имя зрителя: ").strip()
    if name == "":
        print(f"{RED}Имя не введено{RESET}")
        return
    genres = input("Любимые жанры через запятую (например, Comedy, Adventure): ")
    catalog.register_viewer(name, parse_genres(genres))


def choose_viewer():
    if len(catalog.viewers) == 0:
        print(f"{RED}Зрителей пока нет, сначала зарегистрируйте зрителя (пункт 11){RESET}")
        return None
    print("Зрители: " + ", ".join(viewer.name for viewer in catalog.viewers))
    name = input("Введите имя зрителя: ").strip()
    viewer = catalog.find_viewer(name)
    if viewer is None:
        print(f"{RED}Зритель {name} не найден{RESET}")
    return viewer


def watch_film():
    check_data()
    viewer = choose_viewer()
    if viewer is None:
        return
    film = choose_film("Введите номер фильма для просмотра")
    if film is not None:
        viewer.watch(film)


def rate_film():
    check_data()
    viewer = choose_viewer()
    if viewer is None:
        return
    film = choose_film("Введите номер фильма для оценки")
    if film is None:
        return
    score = int(input("Ваша оценка (1..10): "))
    try:
        viewer.rate(film, score)
    except RatingException as e:
        print(e)


def add_to_viewer_playlist():
    check_data()
    viewer = choose_viewer()
    if viewer is None:
        return
    film = choose_film("Введите номер фильма для плейлиста")
    if film is not None:
        viewer.add_to_playlist(film)


def viewer_profile():
    check_data()
    viewer = choose_viewer()
    if viewer is not None:
        viewer.print_profile()


def recommend():
    check_data()
    viewer = choose_viewer()
    if viewer is not None:
        viewer.recommend(catalog.films)


def statistics():
    check_data()
    catalog.print_statistics()


def test_database():
    global catalog
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

    catalog = Catalog(movies)
    catalog.register_viewer("Алексей", ["Comedy", "Adventure"])
    catalog.register_viewer("Мария", ["Fantasy", "Detective", "Family"])
    print(f"{BLACK_ON_GREEN}Данные успешно загружены{RESET}")


def write_error_log(error):
    with open("error_log.txt", "a", encoding="utf-8") as writer_file:
        writer_file.write(f"Ошибка: {error}\n")
        writer_file.write(f"Стек вызовов: {traceback.format_exc()}\n")
        writer_file.write(f"{datetime.now()}\n")
        writer_file.write("-" * 150 + "\n")


def main():
    the_first_word()
    actions = {
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
    while True:
        try:
            choice = print_menu()
            if choice == 0:
                break
            if choice in actions:
                actions[choice]()
            else:
                print(f"{RED}Введён некорректный номер меню{RESET}")
        except EOFError:
            break
        except ValueError:
            print(f"{RED}Нужно ввести число{RESET}")
        except (NoDataUploadedException, ReadingFromFileException):
            pass  # сообщение уже напечатано самим исключением
        except EmptyPlaylistException as e:
            print(e)
        except Exception as e:
            write_error_log(e)
            print(f"{RED}Непредвиденная ошибка, подробности в error_log.txt{RESET}")
    print("До свидания!")
