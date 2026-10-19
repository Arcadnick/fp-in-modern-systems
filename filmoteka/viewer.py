"""Зритель онлайн-кинотеатра: смотрит, оценивает и собирает свой плейлист."""

from filmoteka.colors import CYAN, GREEN, RESET
from filmoteka.exceptions import RatingException
from filmoteka.playlist import Playlist


class Viewer:
    def __init__(self, name, favorite_genres=None):
        self.name = name
        self.favorite_genres = favorite_genres or []
        self.history = []  # просмотренные произведения по порядку
        self.ratings = {}  # название произведения -> оценка зрителя
        self.playlist = Playlist()

    def has_watched(self, film):
        for item in self.history:
            if item is film:
                return True
        return False

    def watch(self, film):
        """Посмотреть произведение: запись в историю и +1 просмотр у произведения."""
        self.history.append(film)
        film.views += 1
        print(f"{GREEN}{self.name} посмотрел(а) «{film.title}». Всего просмотров: {film.views}{RESET}")

    def rate(self, film, score):
        """Поставить оценку и пересчитать рейтинг произведения как среднее всех оценок."""
        if not self.has_watched(film):
            print(f"Нельзя оценить «{film.title}», пока {self.name} его не посмотрел(а)")
            return False
        if score < 1 or score > 10:
            raise RatingException(f"Неверная оценка {score}")
        if film.title in self.ratings:
            print(f"{self.name} уже оценивал(а) «{film.title}» на {self.ratings[film.title]}")
            return False
        self.ratings[film.title] = score
        film.votes.append(score)
        film.rating = round(sum(film.votes) / len(film.votes))
        print(f"{GREEN}Оценка принята. Новый рейтинг «{film.title}»: {film.rating}{RESET}")
        return True

    def add_to_playlist(self, film):
        if self.playlist.contains(film):
            print(f"«{film.title}» уже есть в плейлисте {self.name}")
            return
        self.playlist.add_last(film)
        print(f"«{film.title}» добавлен(а) в плейлист {self.name}")

    def recommend(self, catalog_films, count=3):
        """Подобрать непросмотренные произведения любимых жанров, лучшие по рейтингу."""
        result = []
        for film in catalog_films:
            if self.has_watched(film):
                continue
            for genre in film.genre.split(", "):
                if genre in self.favorite_genres:
                    result.append(film)
                    break
        result.sort(key=lambda item: item.rating, reverse=True)
        result = result[:count]
        print(f"{CYAN}Рекомендации для {self.name}:{RESET}")
        if len(result) == 0:
            print("  Подходящих произведений не нашлось")
        for film in result:
            print(f"  {film.title} ({film.genre}), рейтинг {film.rating}")
        return result

    def print_profile(self):
        print(f"{CYAN}\nЗритель: {self.name}{RESET}")
        print(f"Любимые жанры: {', '.join(self.favorite_genres) or '—'}")
        print(f"Просмотрено: {len(self.history)}")
        for film in self.history:
            score = self.ratings.get(film.title, "—")
            print(f"  {film.title}, оценка: {score}")
        print(f"В плейлисте: {self.playlist.count}")
        for film in self.playlist:
            print(f"  {film.title}")
