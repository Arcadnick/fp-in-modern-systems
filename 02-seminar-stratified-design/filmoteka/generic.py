"""Общие операции: ничего не знают о фильмах и зрителях.

Чистые функции над объектами, списками и строками. Их можно перенести
в любой другой проект без изменений.
"""

import copy


# --- Copy-on-write ---

def copy_with(obj, **changes):
    """Поверхностная копия obj с изменёнными полями. Сам obj не меняется."""
    result = copy.copy(obj)
    for name, value in changes.items():
        setattr(result, name, value)
    return result


# --- Проверки ---

def is_positive(value):
    return value > 0


def one_of(options):
    """Построить проверку «значение входит в options»."""
    return lambda value: value in options


# --- Списки ---

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


def replaced(items, old, new):
    """Кортеж items, в котором объект old (по ссылке) заменён на new."""
    return tuple(new if item is old else item for item in items)


def unique_by(items, key):
    """Убрать элементы с повторяющимся key(элемент); порядок сохраняется."""
    seen = set()
    unique = []
    for item in items:
        value = key(item)
        if value not in seen:
            seen.add(value)
            unique.append(item)
    return unique


def item_at(items, number):
    """Элемент по номеру с 1 или None, если такого номера нет."""
    if 0 < number <= len(items):
        return items[number - 1]
    return None


def average(values):
    return sum(values) / len(values)


# --- Строки ---

def same_text(first, second):
    return first.lower() == second.lower()


def split_list(text):
    """«a, b , ,c» -> ["a", "b", "c"]."""
    return [part.strip() for part in text.split(",") if part.strip() != ""]
