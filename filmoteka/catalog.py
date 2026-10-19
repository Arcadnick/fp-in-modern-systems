"""Онлайн-кинотеатр: общий каталог произведений и зарегистрированные зрители."""

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

        genres = {}  # жанр -> [сумма рейтингов, количество]
        for film in self.films:
            for genre in film.genre.split(", "):
                if genre not in genres:
                    genres[genre] = [0, 0]
                genres[genre][0] += film.rating
                genres[genre][1] += 1
        print(f"{CYAN}Средний рейтинг по жанрам:{RESET}")
        for genre in sorted(genres):
            total, count = genres[genre]
            print(f"  {genre}: {total / count:.1f}")

        print(f"{CYAN}Топ-{top} по рейтингу:{RESET}")
        best = sorted(self.films, key=lambda item: item.rating, reverse=True)
        for i in range(min(top, len(best))):
            print(f"  {i + 1}. {best[i].title} — {best[i].rating}")

        most_viewed = self.films.get_first()
        total_views = 0
        for film in self.films:
            total_views += film.views
            if film.views > most_viewed.views:
                most_viewed = film
        print(f"{CYAN}Просмотры:{RESET}")
        if total_views == 0:
            print("  Пока никто ничего не смотрел")
        else:
            print(f"  Всего просмотров: {total_views}")
            print(f"  Самое просматриваемое: {most_viewed.title} ({most_viewed.views})")
        print(f"  Зрителей зарегистрировано: {len(self.viewers)}")
