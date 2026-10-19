"""Порт Playlist.cs: список произведений."""

from filmoteka.calculations import contains_same, sorted_by_name, sorted_by_rating, unique_by_line
from filmoteka.exceptions import EmptyPlaylistException


class Playlist:
    def __init__(self, items=None):
        self.cinema = list(items) if items else []

    def __iter__(self):
        return iter(self.cinema)

    def __len__(self):
        return len(self.cinema)

    @property
    def count(self):
        return len(self.cinema)

    def find_all(self, filters):
        """Выдать новый плейлист, отфильтрованный по условию."""
        new_playlist = Playlist()
        for item in self.cinema:
            if filters(item):
                new_playlist.add_last(item)
        return new_playlist

    def numbered_lines(self):
        """Плейлист построчно с номерами."""
        return [f"{i}. {item}" for i, item in enumerate(self.cinema, start=1)]

    def add_last(self, item):
        """Добавить произведение в конец плейлиста."""
        self.cinema.append(item)

    def add_first(self, item):
        """Добавить произведение в начало плейлиста."""
        self.cinema.insert(0, item)

    def check_not_empty(self):
        if len(self.cinema) == 0:
            raise EmptyPlaylistException()

    def sort_with(self, sorter):
        """Отсортировать плейлист функцией sorter(список) -> отсортированный список."""
        self.check_not_empty()
        self.cinema = sorter(self.cinema)

    def sort_by_name(self):
        self.sort_with(sorted_by_name)

    def sort_by_rating(self):
        self.sort_with(sorted_by_rating)

    def remove(self, item):
        for i in range(len(self.cinema)):
            if self.cinema[i] is item:
                del self.cinema[i]
                return

    def contains(self, item):
        return contains_same(self.cinema, item)

    def clear(self):
        self.cinema.clear()

    def get_all(self):
        return self.cinema

    def get_first(self):
        self.check_not_empty()
        return self.cinema[0]

    def get_last(self):
        self.check_not_empty()
        return self.cinema[-1]

    def remove_duplicates(self):
        """Удалить произведения, у которых совпадают все поля. Вернуть, сколько удалено."""
        unique = unique_by_line(self.cinema)
        removed = len(self.cinema) - len(unique)
        self.cinema = unique
        return removed

    def to_lines(self):
        return [str(item) for item in self.cinema]
