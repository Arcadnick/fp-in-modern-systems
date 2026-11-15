"""Онлайн-кинотеатр: общий каталог произведений и зарегистрированные зрители.

Каталог неизменяемый: каждая операция возвращает новый каталог (copy-on-write),
а старый остаётся прежним — поэтому его можно хранить для отмены действий.
"""

from filmoteka.generic import copy_with, find_first, replaced, same_text
from filmoteka.queries import average_rating_by_genre, most_viewed, top_by_rating, total_views
from filmoteka.exceptions import EmptyPlaylistException, ViewerException
from filmoteka.playlist import Playlist
from filmoteka.viewer import Viewer


class Catalog:
    def __init__(self, films=None, viewers=()):
        self.films = films if films is not None else Playlist()
        self.viewers = tuple(viewers)

    def find_viewer(self, name):
        return find_first(self.viewers, lambda viewer: same_text(viewer.name, name))

    def find_film(self, title):
        return find_first(self.films, lambda film: same_text(film.title, title))

    # --- Копии с изменениями ---

    def with_films(self, films):
        return copy_with(self, films=films)

    def replace_film(self, old, new):
        return self.with_films(self.films.replace(old, new))

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
        return self.with_films(self.films.sort_by_name())

    def sorted_by_rating(self):
        return self.with_films(self.films.sort_by_rating())

    def without_duplicates(self):
        return self.with_films(self.films.remove_duplicates())

    # --- Вычисления над каталогом ---

    def statistics(self, top=3):
        """Средний рейтинг по жанрам, топ по рейтингу и просмотры."""
        if len(self.films) == 0:
            raise EmptyPlaylistException()
        return {
            "by_genre": average_rating_by_genre(self.films),
            "top": top_by_rating(self.films, top),
            "most_viewed": most_viewed(self.films),
            "total_views": total_views(self.films),
            "viewers": len(self.viewers),
        }
