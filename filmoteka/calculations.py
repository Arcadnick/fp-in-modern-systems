"""Вычисления: чистые функции.

Результат зависит только от аргументов, ничего не печатают и ничего не меняют.
"""

MIN_YEAR = 1895
MAX_YEAR = 2026
MIN_RATING = 1
MAX_RATING = 10


# --- Проверки значений свойств ---

def is_valid_year(value):
    return MIN_YEAR <= value <= MAX_YEAR


def is_valid_rating(value):
    return MIN_RATING <= value <= MAX_RATING


def is_positive(value):
    return value > 0


def one_of(options):
    """Построить проверку «значение входит в options»."""
    return lambda value: value in options


def can_raise_rating(rating):
    return rating < MAX_RATING


# --- Рейтинг и оценки ---

def average(values):
    return sum(values) / len(values)


def rating_from_votes(votes):
    """Рейтинг произведения — округлённое среднее всех оценок."""
    return round(average(votes))


def better_of(first, second):
    """Произведение с бо́льшим рейтингом или None, если рейтинги равны."""
    if first.rating == second.rating:
        return None
    return first if first.rating > second.rating else second


# --- Жанры ---

def split_genres(genre):
    return genre.split(", ")


def parse_genres(text):
    """«Comedy, Adventure » -> ["Comedy", "Adventure"]."""
    return [genre.strip() for genre in text.split(",") if genre.strip() != ""]


def has_favorite_genre(film, favorite_genres):
    return any(genre in favorite_genres for genre in split_genres(film.genre))


def genre_matches(film, query):
    return query.lower() in film.genre.lower()


# --- Обобщённые операции над списками ---

def find_first(items, predicate):
    """Первый элемент, для которого predicate истинен, или None."""
    for item in items:
        if predicate(item):
            return item
    return None


def sorted_by(items, key, reverse=False):
    return sorted(items, key=key, reverse=reverse)


def group_by(items, keys_of):
    """{ключ: [элементы]}; keys_of(item) возвращает все ключи элемента."""
    groups = {}
    for item in items:
        for key in keys_of(item):
            groups.setdefault(key, []).append(item)
    return groups


def same_text(first, second):
    return first.lower() == second.lower()


# --- Списки произведений ---

def by_rating(item):
    return item.rating


def contains_same(items, item):
    """Есть ли в списке именно этот объект (сравнение по ссылке, а не по ==)."""
    return any(element is item for element in items)


def sorted_by_name(items):
    return sorted(items)


def sorted_by_rating(items):
    return sorted_by(items, by_rating)


def top_by_rating(items, count):
    return sorted_by(items, by_rating, reverse=True)[:count]


def unique_by_line(items):
    """Убрать произведения, у которых совпадают все поля; порядок сохраняется."""
    seen = set()
    unique = []
    for item in items:
        line = str(item)
        if line not in seen:
            seen.add(line)
            unique.append(item)
    return unique


def item_at(items, number):
    """Элемент по номеру с 1 или None, если такого номера нет."""
    if 0 < number <= len(items):
        return items[number - 1]
    return None


def recommendations(films, favorite_genres, watched, count):
    """Непросмотренные произведения любимых жанров, лучшие по рейтингу."""
    candidates = [film for film in films
                  if not contains_same(watched, film) and has_favorite_genre(film, favorite_genres)]
    return top_by_rating(candidates, count)


# --- Статистика каталога ---

def average_rating_by_genre(films):
    """{жанр: средний рейтинг}, жанры по алфавиту."""
    groups = group_by(films, lambda film: split_genres(film.genre))
    return {genre: average([film.rating for film in groups[genre]]) for genre in sorted(groups)}


def total_views(films):
    return sum(film.views for film in films)


def most_viewed(films):
    """Самое просматриваемое произведение или None, если просмотров не было."""
    if total_views(films) == 0:
        return None
    return sorted_by(films, lambda film: film.views, reverse=True)[0]


# --- Файлы ---

def playlist_to_lines(items):
    """Произведения -> строки файла: количество, затем по произведению в строке."""
    return [str(len(items))] + [str(item) for item in items]


def with_default_extension(filename):
    return filename if "." in filename else filename + ".txt"
