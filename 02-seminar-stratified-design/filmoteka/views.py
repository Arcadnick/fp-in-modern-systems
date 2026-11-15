"""Представление: текст для экрана.

Чистые функции: получают объекты предметной области и возвращают строки.
Сами ничего не печатают — печатает консоль. Раздел — пара (заголовок, строки):
заголовок консоль выделяет цветом.
"""

from filmoteka.cinematography import Cartoon, Film, Serial
from filmoteka.records import to_record


# --- Произведения ---

def common_details(film):
    return [
        f"Название: {film.title}",
        f"Режиссёр: {film.director}",
        f"Жанр: {film.genre}",
        f"Год выхода: {film.release}",
        f"Рейтинг: {film.rating}",
        f"Просмотров: {film.views}",
    ]


def film_extra(film):
    return [f"Бюджет: {film.budget}", f"Живые спецэффекты: {film.effect}"]


def cartoon_extra(cartoon):
    return [f"Персонажи: {cartoon.character}", f"Тип: {cartoon.kind}"]


def serial_extra(serial):
    return cartoon_extra(serial) + [f"Серий: {serial.series}", f"Сезонов: {serial.seasons}"]


# Тип произведения -> (дополнительные строки, что это такое)
KIND_VIEWS = {
    Film: (film_extra, "Это фильм"),
    Cartoon: (cartoon_extra, "Это мультфильм"),
    Serial: (serial_extra, "Это мультсериал"),
}


def film_details(film):
    """Карточка произведения построчно."""
    extra, description = KIND_VIEWS[type(film)]
    return common_details(film) + extra(film) + [description]


def numbered(films):
    """Список произведений с номерами с 1."""
    return ["Список произведений:"] + [f"{i}. {to_record(film)}" for i, film in enumerate(films, start=1)]


def comparison_lines(result):
    if result.equal:
        return [f"У фильмов одинаковый рейтинг: {result.better.rating}"]
    return [
        "У фильмов разный рейтинг",
        f"«{result.better.title}» ({result.better.rating}) лучше, "
        f"чем «{result.worse.title}» ({result.worse.rating})",
    ]


# --- Сообщения о результате действия ---

def raised_message(film):
    return f"Рейтинг «{film.title}» успешно поднят на одно значение и составляет {film.rating}"


def watched_message(viewer, film):
    return f"{viewer.name} посмотрел(а) «{film.title}». Всего просмотров: {film.views}"


def rated_message(film):
    return f"Оценка принята. Новый рейтинг «{film.title}»: {film.rating}"


def added_message(viewer, film):
    return f"«{film.title}» добавлен(а) в плейлист {viewer.name}"


def registered_message(name):
    return f"Зритель {name} зарегистрирован"


def duplicates_message(removed):
    return f"Удалено дубликатов: {removed}"


# --- Зрители ---

def viewers_line(names):
    return "Зрители: " + ", ".join(names)


def profile_section(viewer):
    lines = [
        f"Любимые жанры: {', '.join(viewer.favorite_genres) or '—'}",
        f"Просмотрено: {len(viewer.history)}",
    ]
    for title in viewer.history:
        lines.append(f"  {title}, оценка: {viewer.ratings.get(title, '—')}")
    lines.append(f"В плейлисте: {len(viewer.playlist)}")
    for title in viewer.playlist:
        lines.append(f"  {title}")
    return f"\nЗритель: {viewer.name}", lines


def recommendations_section(viewer, films):
    lines = [f"  {film.title} ({film.genre}), рейтинг {film.rating}" for film in films]
    return f"Рекомендации для {viewer.name}:", lines or ["  Подходящих произведений не нашлось"]


# --- Статистика ---

def statistics_sections(stats):
    if stats.most_viewed is None:
        views = ["  Пока никто ничего не смотрел"]
    else:
        views = [
            f"  Всего просмотров: {stats.total_views}",
            f"  Самое просматриваемое: {stats.most_viewed.title} ({stats.most_viewed.views})",
        ]
    return [
        ("Средний рейтинг по жанрам:", [f"  {genre}: {rating:.1f}" for genre, rating in stats.by_genre.items()]),
        (f"Топ-{len(stats.top)} по рейтингу:",
         [f"  {i}. {film.title} — {film.rating}" for i, film in enumerate(stats.top, start=1)]),
        ("Просмотры:", views + [f"  Зрителей зарегистрировано: {stats.viewers}"]),
    ]
