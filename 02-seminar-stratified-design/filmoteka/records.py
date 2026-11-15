"""Формат файла с плейлистом: первая строка — количество, затем по произведению в строке."""


def playlist_to_lines(items):
    """Произведения -> строки файла."""
    return [str(len(items))] + [str(item) for item in items]


def with_default_extension(filename):
    return filename if "." in filename else filename + ".txt"
