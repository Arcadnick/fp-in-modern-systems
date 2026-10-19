"""Произведения кинематографа: порт Cinematography.cs, Films.cs, Cartoon.cs, Serial.cs."""

from abc import ABC, abstractmethod

from filmoteka.colors import BLUE, GREEN, RESET
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
        if 1894 < value <= 2026:
            self._release = value
        else:
            try:
                self._release = 2026
                raise InvalidPropertyException(
                    f"Введён неверный год ({value}), диапазон ввода 1895..2026 (было присвоено 2026)"
                )
            except InvalidPropertyException as e:
                print(e)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if 0 < value <= 10:
            self._rating = value
        else:
            try:
                self._rating = 0
                raise InvalidPropertyException(
                    f"Введён неверный рейтинг ({value}), диапазон ввода 1..10 (было присвоено 0)"
                )
            except InvalidPropertyException as e:
                print(e)

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

    def print_data(self):
        """Вывод информации о произведении по пунктам."""
        print(f"{BLUE}\nИнформация о произведении:{RESET}")
        print(f"Название: {self.title}")
        print(f"Режиссёр: {self.director}")
        print(f"Жанр: {self.genre}")
        print(f"Год выхода: {self.release}")
        print(f"Рейтинг: {self.rating}")
        print(f"Просмотров: {self.views}")

    def __str__(self):
        return f"Cinematography|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"

    def raise_rating(self):
        """Поднять рейтинг на 1."""
        if self._rating < 10:
            self._rating += 1
            print(f"{GREEN}Рейтинг «{self.title}» успешно поднят на одно значение и составляет {self._rating}{RESET}")
        else:
            raise RatingException(f"Рейтинг «{self.title}» невозможно поднять, он уже максимальный")

    @abstractmethod
    def describe(self):
        """Сказать, что это за произведение (ToDo в оригинале)."""


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
        if value > 0:
            self._budget = value
        else:
            try:
                self._budget = 1
                raise InvalidPropertyException(
                    f"Введён неверный бюджет ({value}), бюджет не может быть <= 0 (было присвоено 1)"
                )
            except InvalidPropertyException as e:
                print(e)

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value):
        if value == "Yes" or value == "No":
            self._effect = value
        else:
            try:
                self._effect = "--"
                raise InvalidPropertyException(
                    f"Введено неверное значение ({value}), возможные — Yes/No (было присвоено --)"
                )
            except InvalidPropertyException as e:
                print(e)

    def print_data(self):
        super().print_data()
        print(f"Бюджет: {self.budget}")
        print(f"Живые спецэффекты: {self.effect}")

    def __str__(self):
        return (f"Film|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.budget}|{self.effect}")

    def describe(self):
        print("Это фильм")


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
        if value == "Short" or value == "Full" or value == "Serial":
            self._kind = value
        else:
            try:
                self._kind = "--"
                raise InvalidPropertyException(
                    f"Введено неверное значение ({value}), возможные варианты — Full, Short, Serial (было присвоено --)"
                )
            except InvalidPropertyException as e:
                print(e)

    def print_data(self):
        super().print_data()
        print(f"Персонажи: {self.character}")
        print(f"Тип: {self.kind}")

    def __str__(self):
        return (f"Cartoon|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.character}|{self.kind}")

    def describe(self):
        print("Это мультфильм")


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
        if value > 0:
            self._series = value
        else:
            try:
                self._series = 0
                raise InvalidPropertyException(
                    f"Введено неверное количество серий ({value}), оно не может быть <= 0 (было присвоено 0)"
                )
            except InvalidPropertyException as e:
                print(e)

    @property
    def seasons(self):
        return self._seasons

    @seasons.setter
    def seasons(self, value):
        if value > 0:
            self._seasons = value
        else:
            try:
                self._seasons = 0
                raise InvalidPropertyException(
                    f"Введено неверное количество сезонов ({value}), оно не может быть <= 0 (было присвоено 0)"
                )
            except InvalidPropertyException as e:
                print(e)

    def print_data(self):
        super().print_data()
        print(f"Серий: {self.series}")
        print(f"Сезонов: {self.seasons}")

    def __str__(self):
        return (f"Serial|{self.title}|{self.director}|{self.genre}|{self.release}|{self.rating}"
                f"|{self.character}|{self.kind}|{self.series}|{self.seasons}")

    def describe(self):
        print("Это мультсериал")
