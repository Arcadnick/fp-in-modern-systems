"""Запросы к спискам произведений: сортировка, подбор, сравнение и статистика."""

from typing import NamedTuple

from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.exceptions import IdenticalMoviesException
from filmoteka.generic import average, group_by, sorted_by
from filmoteka.rules import split_genres

# Тип произведения, как его вводит пользователь -> класс
KINDS = {"film": Film, "cartoon": Cartoon, "serial": Serial}


class Comparison(NamedTuple):
    """Итог сравнения двух произведений; при равных рейтингах better и worse — в порядке выбора."""
    better: object
    worse: object
    equal: bool


class Statistics(NamedTuple):
    by_genre: dict      # жанр -> средний рейтинг, жанры по алфавиту
    top: list           # лучшие по рейтингу
    most_viewed: object  # самое просматриваемое или None
    total_views: int
    viewers: int


def by_rating(item):
    return item.rating


def by_title_and_year(item):
    """Порядок «по названию»: при одинаковом названии — по году выхода."""
    return item.title, item.release


def identity(film):
    """Ключ для поиска дубликатов: тип и все поля из FIELDS."""
    return (type(film).__name__,) + tuple(getattr(film, name) for name in film.FIELDS)


def sorted_by_name(items):
    return sorted_by(items, by_title_and_year)


def sorted_by_rating(items):
    return sorted_by(items, by_rating)


def top_by_rating(items, count):
    return sorted_by(items, by_rating, reverse=True)[:count]


def better_of(first, second):
    """Произведение с бо́льшим рейтингом или None, если рейтинги равны."""
    if first.rating == second.rating:
        return None
    return first if first.rating > second.rating else second


def compare_films(first, second):
    if first is second:
        raise IdenticalMoviesException()
    better = better_of(first, second)
    if better is None:
        return Comparison(first, second, equal=True)
    return Comparison(better, second if better is first else first, equal=False)


def is_kind(film, kind):
    """Точный тип произведения: мультсериал — не мультфильм."""
    return type(film) is KINDS[kind.lower()]


def is_known_kind(kind):
    return kind.lower() in KINDS


# --- Жанры и рекомендации ---

def has_favorite_genre(film, favorite_genres):
    return any(genre in favorite_genres for genre in split_genres(film.genre))


def genre_matches(film, query):
    return query.lower() in film.genre.lower()


def recommendations(films, favorite_genres, watched_titles, count):
    """Непросмотренные произведения любимых жанров, лучшие по рейтингу."""
    candidates = [film for film in films
                  if film.title not in watched_titles and has_favorite_genre(film, favorite_genres)]
    return top_by_rating(candidates, count)


# --- Статистика каталога ---

def average_rating_by_genre(films):
    """{жанр: средний рейтинг}, жанры по алфавиту."""
    groups = group_by(films, lambda film: split_genres(film.genre))
    return {genre: average([film.rating for film in groups[genre]]) for genre in sorted(groups)}


def total_views(films):
    return sum(film.views for film in films)


def most_viewed(films):
    """Самое просматриваемое произведение или None, если просмотров не было."""
    if total_views(films) == 0:
        return None
    return sorted_by(films, lambda film: film.views, reverse=True)[0]


def statistics(films, viewers, top):
    """Средний рейтинг по жанрам, топ по рейтингу и просмотры."""
    return Statistics(
        by_genre=average_rating_by_genre(films),
        top=top_by_rating(films, top),
        most_viewed=most_viewed(films),
        total_views=total_views(films),
        viewers=viewers,
    )
