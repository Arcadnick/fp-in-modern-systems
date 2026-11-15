"""Действия с файлами: чтение и запись плейлиста."""

from filmoteka.records import playlist_to_lines
from filmoteka.constructors import parse_playlist


def load_playlist(filename):
    with open(filename, encoding="utf-8") as file:
        lines = file.read().splitlines()
    return parse_playlist(lines)


def save_playlist(playlist, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(playlist_to_lines(playlist.get_all())) + "\n")
