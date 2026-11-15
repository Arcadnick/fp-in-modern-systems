"""Правила предметной области: допустимые значения и расчёт рейтинга.

На них опираются сами классы произведений, поэтому модуль не знает о классах.
"""

from filmoteka.generic import average, split_list

MIN_YEAR = 1895
MAX_YEAR = 2026
MIN_RATING = 1
MAX_RATING = 10


def is_valid_year(value):
    return MIN_YEAR <= value <= MAX_YEAR


def is_valid_rating(value):
    return MIN_RATING <= value <= MAX_RATING


def can_raise_rating(rating):
    return rating < MAX_RATING


def rating_from_votes(votes):
    """Рейтинг произведения — округлённое среднее всех оценок."""
    return round(average(votes))


def split_genres(genre):
    """Жанры произведения: «Comedy, Adventure» -> ["Comedy", "Adventure"]."""
    return genre.split(", ")


def parse_genres(text):
    """Жанры, введённые зрителем: «Comedy, Adventure » -> ["Comedy", "Adventure"]."""
    return split_list(text)
