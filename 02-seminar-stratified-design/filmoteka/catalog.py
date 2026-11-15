"""Онлайн-кинотеатр: общий каталог произведений и зарегистрированные зрители.

Каталог неизменяемый: каждая операция возвращает новый каталог (copy-on-write),
а старый остаётся прежним — поэтому его можно хранить для отмены действий.

Каталог — барьер абстракций: код выше него не знает, что произведения лежат
в Playlist, а зрители — в кортеже, и работает только через методы каталога.
"""

from filmoteka.generic import copy_with, find_first, replaced, same_text
from filmoteka.queries import (
    genre_matches,
    is_kind,
    is_known_kind,
    recommendations,
    sorted_by_name,
    sorted_by_rating,
    statistics,
)
from filmoteka.exceptions import EmptyPlaylistException, NoDataUploadedException, ViewerException
from filmoteka.playlist import Playlist
from filmoteka.viewer import Viewer


class Catalog:
    def __init__(self, films=None, viewers=()):
        self.films = films if films is not None else Playlist()
        self.viewers = tuple(viewers)

    # --- Чтение ---

    def is_empty(self):
        return len(self.films) == 0

    def check_not_empty(self):
        if self.is_empty():
            raise NoDataUploadedException()

    def film_count(self):
        return len(self.films)

    def all_films(self):
        return tuple(self.films)

    def film_at(self, number):
        """Произведение по номеру в списке (с 1) или None."""
        return self.films.at(number)

    def films_where(self, predicate):
        return tuple(self.films.filtered(predicate))

    def films_of_genre(self, genre):
        return self.films_where(lambda film: genre_matches(film, genre))

    def films_of_kind(self, kind):
        """Произведения типа kind (Film, Cartoon, Serial) или None, если такого типа нет."""
        if not is_known_kind(kind):
            return None
        return self.films_where(lambda film: is_kind(film, kind))

    def has_viewers(self):
        return len(self.viewers) > 0

    def viewer_names(self):
        return tuple(viewer.name for viewer in self.viewers)

    def find_viewer(self, name):
        return find_first(self.viewers, lambda viewer: same_text(viewer.name, name))

    # --- Копии с изменениями ---

    def with_films(self, films):
        return copy_with(self, films=films)

    def replace_film(self, old, new):
        return self.with_films(self.films.replaced(old, new))

    def replace_viewer(self, old, new):
        return copy_with(self, viewers=replaced(self.viewers, old, new))

    def with_viewer(self, name, favorite_genres):
        """Новый каталог с зарегистрированным зрителем."""
        if self.find_viewer(name) is not None:
            raise ViewerException(f"Зритель {name} уже зарегистрирован")
        return copy_with(self, viewers=self.viewers + (Viewer(name, favorite_genres),))

    def raise_rating(self, film):
        """(новый каталог, произведение с поднятым рейтингом)."""
        raised = film.with_raised_rating()
        return self.replace_film(film, raised), raised

    def watch(self, viewer, film):
        """(новый каталог, произведение с учтённым просмотром)."""
        watched = film.with_view()
        new_catalog = self.replace_film(film, watched).replace_viewer(viewer, viewer.watched(film.title))
        return new_catalog, watched

    def rate(self, viewer, film, score):
        """(новый каталог, произведение с пересчитанным рейтингом)."""
        rated_viewer = viewer.rated(film.title, score)
        voted = film.with_vote(score)
        return self.replace_film(film, voted).replace_viewer(viewer, rated_viewer), voted

    def add_to_playlist(self, viewer, film):
        return self.replace_viewer(viewer, viewer.with_in_playlist(film.title))

    def sorted_by_name(self):
        return self.with_films(self.films.sorted_with(sorted_by_name))

    def sorted_by_rating(self):
        return self.with_films(self.films.sorted_with(sorted_by_rating))

    def without_duplicates(self):
        """(новый каталог, сколько произведений удалено)."""
        # дубликаты — произведения, у которых совпадают все поля, то есть строка файла
        new_catalog = self.with_films(self.films.unique_by(str))
        return new_catalog, self.film_count() - new_catalog.film_count()

    # --- Вычисления над каталогом ---

    def recommendations_for(self, viewer, count=3):
        """Непросмотренные зрителем произведения его любимых жанров, лучшие по рейтингу."""
        return recommendations(self.films, viewer.favorite_genres, viewer.history, count)

    def statistics(self, top=3):
        """Средний рейтинг по жанрам, топ по рейтингу и просмотры."""
        if self.is_empty():
            raise EmptyPlaylistException()
        return statistics(self.films, len(self.viewers), top)
