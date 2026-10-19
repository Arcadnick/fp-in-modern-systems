"""Порт MainException.cs: исключения, которые сами печатают подсказку при создании."""

from filmoteka.colors import RED, RESET


class RatingException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(f"{RED}Минимальное значение рейтинга — 1, максимальное — 10.{RESET}")


class ReadingFromFileException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(f"{RED}В файле записаны некорректные данные.")
        print(f"Пожалуйста, проверьте содержимое файла.{RESET}")


class NumberFilmException(Exception):
    def __init__(self, message=""):
        super().__init__(message)
        print(f"{RED}Фильма с таким номером нет.")
        print(f"Пожалуйста, введите номер из списка.{RESET}")


class NoDataUploadedException(Exception):
    def __init__(self):
        super().__init__("Данные не загружены")
        print(f"{RED}Сначала загрузите данные (пункт 1 или 3 меню).{RESET}")


class IdenticalMoviesException(Exception):
    def __init__(self):
        super().__init__("Выбран один и тот же фильм")
        print(f"{RED}Нет смысла сравнивать фильм с самим собой. Выберите два разных фильма.{RESET}")


class InvalidPropertyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(f"{RED}Введено неверное значение свойства{RESET}")


class EmptyPlaylistException(Exception):
    """Аналог InvalidOperationException("The container is empty.") из C#."""

    def __init__(self):
        super().__init__("Плейлист пуст.")
