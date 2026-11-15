"""Порт Playlist.cs: список произведений.

Плейлист неизменяемый: операции возвращают новый плейлист (copy-on-write).
"""

from filmoteka.calculations import contains_same, replaced, sorted_by_name, sorted_by_rating, unique_by_line
from filmoteka.exceptions import EmptyPlaylistException


class Playlist:
    def __init__(self, items=()):
        self.cinema = tuple(items)

    def __iter__(self):
        return iter(self.cinema)

    def __len__(self):
        return len(self.cinema)

    @property
    def count(self):
        return len(self.cinema)

    def find_all(self, filters):
        """Новый плейлист, отфильтрованный по условию."""
        return Playlist(item for item in self.cinema if filters(item))

    def numbered_lines(self):
        """Плейлист построчно с номерами."""
        return [f"{i}. {item}" for i, item in enumerate(self.cinema, start=1)]

    def add_last(self, item):
        """Новый плейлист с произведением в конце."""
        return Playlist(self.cinema + (item,))

    def add_first(self, item):
        """Новый плейлист с произведением в начале."""
        return Playlist((item,) + self.cinema)

    def check_not_empty(self):
        if len(self.cinema) == 0:
            raise EmptyPlaylistException()

    def sort_with(self, sorter):
        """Новый плейлист, отсортированный функцией sorter(список) -> отсортированный список."""
        self.check_not_empty()
        return Playlist(sorter(self.cinema))

    def sort_by_name(self):
        return self.sort_with(sorted_by_name)

    def sort_by_rating(self):
        return self.sort_with(sorted_by_rating)

    def remove(self, item):
        return Playlist(element for element in self.cinema if element is not item)

    def replace(self, old, new):
        """Новый плейлист, в котором произведение old заменено на new."""
        return Playlist(replaced(self.cinema, old, new))

    def contains(self, item):
        return contains_same(self.cinema, item)

    def clear(self):
        return Playlist()

    def get_all(self):
        return self.cinema

    def get_first(self):
        self.check_not_empty()
        return self.cinema[0]

    def get_last(self):
        self.check_not_empty()
        return self.cinema[-1]

    def remove_duplicates(self):
        """Новый плейлист без произведений, у которых совпадают все поля."""
        return Playlist(unique_by_line(self.cinema))

    def to_lines(self):
        return [str(item) for item in self.cinema]
