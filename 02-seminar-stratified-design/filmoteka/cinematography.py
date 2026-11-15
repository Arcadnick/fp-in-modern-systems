"""Произведения кинематографа: порт Cinematography.cs, Films.cs, Cartoon.cs, Serial.cs."""

from filmoteka.exceptions import InvalidPropertyException, RatingException
from filmoteka.generic import copy_with, is_positive, one_of
from filmoteka.rules import (
    MAX_RATING,
    MAX_YEAR,
    MIN_RATING,
    MIN_YEAR,
    can_raise_rating,
    is_valid_rating,
    is_valid_year,
    rating_from_votes,
)

EFFECTS = ("Yes", "No")
CARTOON_KINDS = ("Short", "Full", "Serial")


def checked(value, is_valid, message):
    """Вернуть value, если is_valid(value), иначе бросить InvalidPropertyException(message)."""
    if not is_valid(value):
        raise InvalidPropertyException(message)
    return value


class Cinematography:
    """Произведение кинематографа.

    После создания не меняется: операции возвращают изменённую копию (copy-on-write).
    FIELDS — поля, которые описывают произведение (без просмотров и оценок), по порядку.
    """

    FIELDS = ("title", "director", "genre", "release", "rating")

    def __init__(self, title, director, genre="unknown", release=1895, rating=1):
        self.title = title
        self.director = director
        self.genre = genre  # Ужасы, Фэнтези, Приключения, Триллер, Комедия и т.д.
        self.release = release
        self.rating = rating  # 1..10
        self.views = 0
        self.votes = (self.rating,)  # оценка критиков + оценки зрителей

    @property
    def release(self):
        return self._release

    @release.setter
    def release(self, value):
        self._release = checked(value, is_valid_year, f"Неверный год ({value}), допустимо {MIN_YEAR}..{MAX_YEAR}")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = checked(value, is_valid_rating,
                               f"Неверный рейтинг ({value}), допустимо {MIN_RATING}..{MAX_RATING}")

    def can_raise_rating(self):
        return can_raise_rating(self.rating)

    def with_raised_rating(self):
        """Копия с рейтингом на 1 больше."""
        if not self.can_raise_rating():
            raise RatingException(f"Рейтинг «{self.title}» уже максимальный, поднять его нельзя")
        return copy_with(self, rating=self.rating + 1)

    def with_view(self):
        """Копия с ещё одним просмотром."""
        return copy_with(self, views=self.views + 1)

    def with_vote(self, score):
        """Копия с новой оценкой зрителя и пересчитанным рейтингом."""
        votes = self.votes + (score,)
        return copy_with(self, votes=votes, rating=rating_from_votes(votes))


class Film(Cinematography):
    FIELDS = Cinematography.FIELDS + ("budget", "effect")

    def __init__(self, title, director, genre, release, rating, budget, effect):
        super().__init__(title, director, genre, release, rating)
        self.budget = budget
        self.effect = effect  # снимались ли спецэффекты вживую: Yes/No

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget = checked(value, is_positive, f"Неверный бюджет ({value}), бюджет должен быть больше 0")

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value):
        self._effect = checked(value, one_of(EFFECTS), f"Неверное значение ({value}), возможные — Yes/No")


class Cartoon(Cinematography):
    FIELDS = Cinematography.FIELDS + ("character", "kind")

    def __init__(self, title, director, genre, release, rating, character, kind):
        super().__init__(title, director, genre, release, rating)
        self.character = character
        self.kind = kind  # короткометражный, полнометражный или сериал

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = checked(value, one_of(CARTOON_KINDS),
                             f"Неверное значение ({value}), возможные варианты — Full, Short, Serial")


class Serial(Cartoon):
    FIELDS = Cartoon.FIELDS + ("series", "seasons")

    def __init__(self, title, director, genre, release, rating, character, kind, series, seasons):
        super().__init__(title, director, genre, release, rating, character, kind)
        self.series = series
        self.seasons = seasons

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, value):
        self._series = checked(value, is_positive, f"Неверное количество серий ({value}), оно должно быть больше 0")

    @property
    def seasons(self):
        return self._seasons

    @seasons.setter
    def seasons(self, value):
        self._seasons = checked(value, is_positive,
                                f"Неверное количество сезонов ({value}), оно должно быть больше 0")
