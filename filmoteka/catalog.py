"""Онлайн-кинотеатр: общий каталог произведений и зарегистрированные зрители."""

from filmoteka.calculations import (
    average_rating_by_genre,
    find_first,
    most_viewed,
    same_text,
    top_by_rating,
    total_views,
)
from filmoteka.exceptions import EmptyPlaylistException, ViewerException
from filmoteka.playlist import Playlist
from filmoteka.viewer import Viewer


class Catalog:
    def __init__(self, films=None):
        self.films = films if films is not None else Playlist()
        self.viewers = []

    def register_viewer(self, name, favorite_genres):
        if self.find_viewer(name) is not None:
            raise ViewerException(f"Зритель {name} уже зарегистрирован")
        viewer = Viewer(name, favorite_genres)
        self.viewers.append(viewer)
        return viewer

    def find_viewer(self, name):
        return find_first(self.viewers, lambda viewer: same_text(viewer.name, name))

    def find_film(self, title):
        return find_first(self.films, lambda film: same_text(film.title, title))

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
