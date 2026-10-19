"""Произведения кинематографа: порт Cinematography.cs, Films.cs, Cartoon.cs, Serial.cs."""

from abc import ABC, abstractmethod

from filmoteka.calculations import (
    MAX_RATING,
    MAX_YEAR,
    MIN_RATING,
    MIN_YEAR,
    can_raise_rating,
    is_positive,
    is_valid_rating,
    is_valid_year,
)
from filmoteka.exceptions import InvalidPropertyException, RatingException


class Cinematography(ABC):
    """Произведение кинематографа.

    Сортировка (<) — по названию, при одинаковом названии — по году выхода.
    """

    def __init__(self, title, director, genre="unknown", release=1895, rating=1):
        self.title = title
        self.director = director
        self.genre = genre  # Ужасы, Фэнтези, Приключения, Триллер, Комедия и т.д.
        self.release = release
        self.rating = rating  # 1..10
        self.views = 0
        self.votes = [self.rating]  # оценка критиков + оценки зрителей

    @property
    def release(self):
        return self._release

    @release.setter
    def release(self, value):
        if not is_valid_year(value):
            raise InvalidPropertyException(f"Неверный год ({value}), допустимо {MIN_YEAR}..{MAX_YEAR}")
        self._release = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not is_valid_rating(value):
            raise InvalidPropertyException(f"Неверный рейтинг ({value}), допустимо {MIN_RATING}..{MAX_RATING}")
        self._rating = value

    def __lt__(self, other):
        if self.title == other.title:
            return self.release < other.release
        return self.title < other.title

    def __eq__(self, other):
        # Как в оригинале: два произведения «равны», если у них одинаковый рейтинг
        if isinstance(other, Cinematography):
            return self.rating == other.rating
        return False

    __hash__ = object.__hash__

    def details(self):
        """Информация о произведении построчно."""
        return [
            f"Название: {self.title}",
            f"Режиссёр: {self.director}",
            f"Жанр: {self.genre}",
            f"Год выхода: {self.release}",
            f"Рейтинг: {self.rating}",
            f"Просмотров: {self.views}",
        ]

    def __str__(self):
        return f"Cinematography|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"

    def raise_rating(self):
        """Поднять рейтинг на 1 и вернуть новый рейтинг."""
        if not can_raise_rating(self._rating):
            raise RatingException(f"Рейтинг «{self.title}» уже максимальный, поднять его нельзя")
        self._rating += 1
        return self._rating

    @abstractmethod
    def describe(self):
        """Что это за произведение (ToDo в оригинале)."""


class Film(Cinematography):
    def __init__(self, title, director, genre, release, rating, budget, effect):
        super().__init__(title, director, genre, release, rating)
        self.budget = budget
        self.effect = effect  # снимались ли спецэффекты вживую: Yes/No

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if not is_positive(value):
            raise InvalidPropertyException(f"Неверный бюджет ({value}), бюджет должен быть больше 0")
        self._budget = value

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value):
        if value not in ("Yes", "No"):
            raise InvalidPropertyException(f"Неверное значение ({value}), возможные — Yes/No")
        self._effect = value

    def details(self):
        return super().details() + [
            f"Бюджет: {self.budget}",
            f"Живые спецэффекты: {self.effect}",
        ]

    def __str__(self):
        return (f"Film|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.budget}|{self.effect}")

    def describe(self):
        return "Это фильм"


class Cartoon(Cinematography):
    def __init__(self, title, director, genre, release, rating, character, kind):
        super().__init__(title, director, genre, release, rating)
        self.character = character
        self.kind = kind  # короткометражный, полнометражный или сериал

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        if value not in ("Short", "Full", "Serial"):
            raise InvalidPropertyException(f"Неверное значение ({value}), возможные варианты — Full, Short, Serial")
        self._kind = value

    def details(self):
        return super().details() + [
            f"Персонажи: {self.character}",
            f"Тип: {self.kind}",
        ]

    def __str__(self):
        return (f"Cartoon|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.character}|{self.kind}")

    def describe(self):
        return "Это мультфильм"


class Serial(Cartoon):
    def __init__(self, title, director, genre, release, rating, character, kind, series, seasons):
        super().__init__(title, director, genre, release, rating, character, kind)
        self.series = series
        self.seasons = seasons

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, value):
        if not is_positive(value):
            raise InvalidPropertyException(f"Неверное количество серий ({value}), оно должно быть больше 0")
        self._series = value

    @property
    def seasons(self):
        return self._seasons

    @seasons.setter
    def seasons(self, value):
        if not is_positive(value):
            raise InvalidPropertyException(f"Неверное количество сезонов ({value}), оно должно быть больше 0")
        self._seasons = value

    def details(self):
        return super().details() + [
            f"Серий: {self.series}",
            f"Сезонов: {self.seasons}",
        ]

    def __str__(self):
        return (f"Serial|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.character}|{self.kind}|{self.series}|{self.seasons}")

    def describe(self):
        return "Это мультсериал"
