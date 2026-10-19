"""Зритель онлайн-кинотеатра: смотрит, оценивает и собирает свой плейлист."""

from filmoteka.calculations import (
    MAX_RATING,
    MIN_RATING,
    contains_same,
    is_valid_rating,
    rating_from_votes,
    recommendations,
)
from filmoteka.exceptions import RatingException, ViewerException
from filmoteka.playlist import Playlist


class Viewer:
    def __init__(self, name, favorite_genres=None):
        self.name = name
        self.favorite_genres = favorite_genres or []
        self.history = []  # просмотренные произведения по порядку
        self.ratings = {}  # название произведения -> оценка зрителя
        self.playlist = Playlist()

    def has_watched(self, film):
        return contains_same(self.history, film)

    def watch(self, film):
        """Посмотреть произведение: запись в историю и +1 просмотр. Вернуть число просмотров."""
        self.history.append(film)
        film.views += 1
        return film.views

    def rate(self, film, score):
        """Поставить оценку и пересчитать рейтинг произведения. Вернуть новый рейтинг."""
        if not self.has_watched(film):
            raise RatingException(f"Нельзя оценить «{film.title}», пока {self.name} его не посмотрел(а)")
        if not is_valid_rating(score):
            raise RatingException(f"Оценка должна быть от {MIN_RATING} до {MAX_RATING}")
        if film.title in self.ratings:
            raise RatingException(f"{self.name} уже оценивал(а) «{film.title}» на {self.ratings[film.title]}")
        self.ratings[film.title] = score
        film.votes.append(score)
        film.rating = rating_from_votes(film.votes)
        return film.rating

    def add_to_playlist(self, film):
        if self.playlist.contains(film):
            raise ViewerException(f"«{film.title}» уже есть в плейлисте {self.name}")
        self.playlist.add_last(film)

    def recommend(self, catalog_films, count=3):
        """Непросмотренные произведения любимых жанров, лучшие по рейтингу."""
        return recommendations(catalog_films, self.favorite_genres, self.history, count)

    def profile_lines(self):
        lines = [
            f"Любимые жанры: {', '.join(self.favorite_genres) or '—'}",
            f"Просмотрено: {len(self.history)}",
        ]
        for film in self.history:
            lines.append(f"  {film.title}, оценка: {self.ratings.get(film.title, '—')}")
        lines.append(f"В плейлисте: {self.playlist.count}")
        for film in self.playlist:
            lines.append(f"  {film.title}")
        return lines
