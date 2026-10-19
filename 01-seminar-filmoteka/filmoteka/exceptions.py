"""Исключения предметной области.

Сами ничего не печатают: текст ошибки показывает пользователю меню.
"""


class FilmotekaError(Exception):
    """Ошибка, текст которой меню показывает пользователю."""


class RatingException(FilmotekaError):
    pass


class ReadingFromFileException(FilmotekaError):
    pass


class NumberFilmException(FilmotekaError):
    def __init__(self):
        super().__init__("Фильма с таким номером нет. Введите номер из списка.")


class NoDataUploadedException(FilmotekaError):
    def __init__(self):
        super().__init__("Сначала загрузите данные (пункт 1 или 3 меню).")


class IdenticalMoviesException(FilmotekaError):
    def __init__(self):
        super().__init__("Нет смысла сравнивать фильм с самим собой. Выберите два разных фильма.")


class InvalidPropertyException(FilmotekaError):
    pass


class EmptyPlaylistException(FilmotekaError):
    """Аналог InvalidOperationException("The container is empty.") из C#."""

    def __init__(self):
        super().__init__("Плейлист пуст.")


class ViewerException(FilmotekaError):
    pass
