"""Онлайн-кинотеатр: общий каталог произведений и зарегистрированные зрители."""

from filmoteka.calculations import average_rating_by_genre, most_viewed, top_by_rating, total_views
from filmoteka.colors import CYAN, GREEN, RESET
from filmoteka.exceptions import EmptyPlaylistException
from filmoteka.playlist import Playlist
from filmoteka.viewer import Viewer


class Catalog:
    def __init__(self, films=None):
        self.films = films if films is not None else Playlist()
        self.viewers = []

    def register_viewer(self, name, favorite_genres):
        if self.find_viewer(name) is not None:
            print(f"Зритель {name} уже зарегистрирован")
            return None
        viewer = Viewer(name, favorite_genres)
        self.viewers.append(viewer)
        print(f"{GREEN}Зритель {name} зарегистрирован{RESET}")
        return viewer

    def find_viewer(self, name):
        for viewer in self.viewers:
            if viewer.name.lower() == name.lower():
                return viewer
        return None

    def find_film(self, title):
        for film in self.films:
            if film.title.lower() == title.lower():
                return film
        return None

    def print_statistics(self, top=3):
        """Средний рейтинг по жанрам, топ по рейтингу и самое просматриваемое."""
        if len(self.films) == 0:
            raise EmptyPlaylistException()

        print(f"{CYAN}Средний рейтинг по жанрам:{RESET}")
        for genre, rating in average_rating_by_genre(self.films).items():
            print(f"  {genre}: {rating:.1f}")

        print(f"{CYAN}Топ-{top} по рейтингу:{RESET}")
        for i, film in enumerate(top_by_rating(self.films, top), start=1):
            print(f"  {i}. {film.title} — {film.rating}")

        print(f"{CYAN}Просмотры:{RESET}")
        leader = most_viewed(self.films)
        if leader is None:
            print("  Пока никто ничего не смотрел")
        else:
            print(f"  Всего просмотров: {total_views(self.films)}")
            print(f"  Самое просматриваемое: {leader.title} ({leader.views})")
        print(f"  Зрителей зарегистрировано: {len(self.viewers)}")
