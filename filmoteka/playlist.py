"""Порт Playlist.cs: список произведений."""

from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.colors import BLACK_ON_GREEN, RESET
from filmoteka.exceptions import EmptyPlaylistException, ReadingFromFileException


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

    def print_all(self):
        """Вывести весь плейлист с номерами."""
        print("Список произведений:")
        for i, item in enumerate(self.cinema, start=1):
            print(f"{i}. {item}")

    def add_last(self, item):
        """Добавить произведение в конец плейлиста."""
        self.cinema.append(item)

    def add_first(self, item):
        """Добавить произведение в начало плейлиста."""
        self.cinema.insert(0, item)

    def sort_by_name(self):
        if len(self.cinema) > 0:
            self.cinema.sort()
        else:
            raise EmptyPlaylistException()

    def sort_by_rating(self):
        if len(self.cinema) > 0:
            self.cinema.sort(key=lambda item: item.rating)
        else:
            raise EmptyPlaylistException()

    def remove(self, item):
        for i in range(len(self.cinema)):
            if self.cinema[i] is item:
                del self.cinema[i]
                return

    def contains(self, item):
        for element in self.cinema:
            if element is item:
                return True
        return False

    def clear(self):
        self.cinema.clear()

    def get_all(self):
        return self.cinema

    def get_first(self):
        if len(self.cinema) > 0:
            return self.cinema[0]
        raise EmptyPlaylistException()

    def get_last(self):
        if len(self.cinema) > 0:
            return self.cinema[-1]
        raise EmptyPlaylistException()

    def remove_duplicates(self):
        """Удалить произведения, у которых совпадают все поля."""
        seen = set()
        unique = []
        for item in self.cinema:
            line = str(item)
            if line not in seen:
                seen.add(line)
                unique.append(item)
        removed = len(self.cinema) - len(unique)
        self.cinema = unique
        print(f"Удалено дубликатов: {removed}")

    def load_from_file(self, filename):
        """Дописать в плейлист произведения из файла.

        Формат: в первой строке количество записей, дальше по записи в строке,
        поля через «|», первое поле — тип (Film, Cartoon, Serial).
        """
        with open(filename, encoding="utf-8") as file:
            try:
                n = int(file.readline())
                for _ in range(n):
                    parts = file.readline().strip().split("|")
                    if parts[0] == "Film":
                        self.cinema.append(Film(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]),
                                                int(parts[6]), parts[7]))
                    if parts[0] == "Cartoon":
                        self.cinema.append(Cartoon(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]),
                                                   parts[6], parts[7]))
                    if parts[0] == "Serial":
                        self.cinema.append(Serial(parts[1], parts[2], parts[3], int(parts[4]), int(parts[5]),
                                                  parts[6], parts[7], int(parts[8]), int(parts[9])))
            except (ValueError, IndexError) as e:
                raise ReadingFromFileException(str(e))
        print(f"{BLACK_ON_GREEN}Данные успешно загружены{RESET}")

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"{len(self.cinema)}\n")
            for item in self.cinema:
                file.write(f"{item}\n")

    def to_lines(self):
        result = []
        for item in self.cinema:
            result.append(str(item))
        return result
