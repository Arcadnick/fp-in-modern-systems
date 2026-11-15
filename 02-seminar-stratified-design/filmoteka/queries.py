"""Запросы к спискам произведений: сортировка, подбор, сравнение и статистика."""

from filmoteka.generic import average, group_by, sorted_by, unique_by
from filmoteka.rules import split_genres


def by_rating(item):
    return item.rating


def sorted_by_name(items):
    return sorted(items)


def sorted_by_rating(items):
    return sorted_by(items, by_rating)


def top_by_rating(items, count):
    return sorted_by(items, by_rating, reverse=True)[:count]


def unique_by_line(items):
    """Убрать произведения, у которых совпадают все поля; порядок сохраняется."""
    return unique_by(items, str)


def better_of(first, second):
    """Произведение с бо́льшим рейтингом или None, если рейтинги равны."""
    if first.rating == second.rating:
        return None
    return first if first.rating > second.rating else second


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
