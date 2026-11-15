"""Порт Playlist.cs: список произведений.

Плейлист неизменяемый: операции возвращают новый плейлист (copy-on-write).
Интерфейс минимальный: всё остальное каталог выражает через эти методы
и общие операции из generic.py.
"""

from filmoteka.exceptions import EmptyPlaylistException
from filmoteka.generic import item_at, replaced, unique_by


class Playlist:
    def __init__(self, items=()):
        self.cinema = tuple(items)

    def __iter__(self):
        return iter(self.cinema)

    def __len__(self):
        return len(self.cinema)

    def at(self, number):
        """Произведение по номеру с 1 или None."""
        return item_at(self.cinema, number)

    def filtered(self, predicate):
        return Playlist(item for item in self.cinema if predicate(item))

    def sorted_with(self, sorter):
        """Новый плейлист, отсортированный функцией sorter(список) -> отсортированный список."""
        if len(self.cinema) == 0:
            raise EmptyPlaylistException()
        return Playlist(sorter(self.cinema))

    def replaced(self, old, new):
        """Новый плейлист, в котором произведение old заменено на new."""
        return Playlist(replaced(self.cinema, old, new))

    def unique_by(self, key):
        """Новый плейлист без повторов key(произведение)."""
        return Playlist(unique_by(self.cinema, key))

    def numbered_lines(self):
        """Плейлист построчно с номерами."""
        return [f"{i}. {item}" for i, item in enumerate(self.cinema, start=1)]
