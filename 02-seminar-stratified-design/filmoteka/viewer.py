"""Зритель онлайн-кинотеатра: смотрит, оценивает и собирает свой плейлист.

Зритель неизменяемый: операции возвращают изменённую копию (copy-on-write).
Произведения он хранит по названиям, поэтому новые копии произведений
не делают его данные устаревшими.
"""

from filmoteka.generic import copy_with
from filmoteka.rules import MAX_RATING, MIN_RATING, is_valid_rating
from filmoteka.exceptions import RatingException, ViewerException


class Viewer:
    def __init__(self, name, favorite_genres=()):
        self.name = name
        self.favorite_genres = tuple(favorite_genres)
        self.history = ()  # названия просмотренных произведений по порядку
        self.ratings = {}  # название произведения -> оценка; при оценке создаётся новый словарь
        self.playlist = ()  # названия произведений в личном плейлисте

    def has_watched(self, title):
        return title in self.history

    def watched(self, title):
        """Копия с произведением в истории просмотров."""
        return copy_with(self, history=self.history + (title,))

    def rated(self, title, score):
        """Копия с оценкой произведения."""
        if not self.has_watched(title):
            raise RatingException(f"Нельзя оценить «{title}», пока {self.name} его не посмотрел(а)")
        if not is_valid_rating(score):
            raise RatingException(f"Оценка должна быть от {MIN_RATING} до {MAX_RATING}")
        if title in self.ratings:
            raise RatingException(f"{self.name} уже оценивал(а) «{title}» на {self.ratings[title]}")
        return copy_with(self, ratings={**self.ratings, title: score})

    def with_in_playlist(self, title):
        """Копия с произведением в личном плейлисте."""
        if title in self.playlist:
            raise ViewerException(f"«{title}» уже есть в плейлисте {self.name}")
        return copy_with(self, playlist=self.playlist + (title,))
