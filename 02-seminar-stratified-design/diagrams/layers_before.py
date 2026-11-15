"""Слои исходного состояния (код после семинара 1, коммит «Семинар 2: исходное состояние»).

Слои перечислены сверху вниз. Узел попадает в первый слой, где его имя указано
явно, а если явно не указано — в первый слой с подходящим шаблоном.
"""

TITLE = "Граф вызовов: исходное состояние"

LAYERS = [
    ("Цикл меню", ["main.main"]),
    ("Команды меню и их общие части", [
        "main.get_data", "main.get_file", "main.test_database", "main.writer", "main.raise_up",
        "main.compare", "main.sort_by_name", "main.sort_by_rating", "main.sort_films",
        "main.filter_films", "main.remove_duplicates", "main.register_viewer", "main.watch_film",
        "main.rate_film", "main.add_to_viewer_playlist", "main.viewer_profile", "main.recommend",
        "main.statistics", "main.with_viewer", "main.with_viewer_and_film", "main.choose_film",
        "main.choose_viewer", "main.check_data",
    ]),
    ("Консоль и файлы", ["main.*", "storage.*"]),
    ("Конструкторы", ["constructors.*"]),
    ("Каталог", ["Catalog.*"]),
    ("Зритель и плейлист", ["Viewer.*", "Playlist.*"]),
    # Класс Cinematography размазан по двум слоям: копии with_* опираются на
    # calculations.py, а calculations.py сам вызывает __str__ и __lt__ произведений.
    ("Операции над произведениями", ["*.__init__", "*=", "Cinematography.with_*", "cinematography.*"]),
    ("Вычисления (calculations.py)", ["calculations.*"]),
    ("Представление произведений", ["*.__str__", "*.__lt__", "*.__eq__", "*.details", "*.describe"]),
    ("Данные", ["*: поля", "*Exception", "FilmotekaError"]),
]

# Слои, которые должны работать через нижние слои, а не с данными и языком напрямую
TOP_LAYERS = ["Цикл меню", "Команды меню и их общие части"]

# Барьер абстракций: кто владеет данными каталога и плейлиста и что считается их внутренностями
BARRIER = (["Catalog.*", "Playlist.*"], ["Catalog: поля", "Playlist: поля", "Playlist.*"])

# Неявные вызовы: в синтаксисе их не видно, но код от них зависит
IMPLICIT_CALLS = [
    # str(film) и f"{film}" вызывают __str__ — строку формата файла
    ("calculations.unique_by_line", "Cinematography.__str__"),
    ("calculations.playlist_to_lines", "Cinematography.__str__"),
    ("Playlist.to_lines", "Cinematography.__str__"),
    ("Playlist.numbered_lines", "Cinematography.__str__"),
    # sorted(films) сравнивает произведения через __lt__
    ("calculations.sorted_by_name", "Cinematography.__lt__"),
    # len(playlist) и for по плейлисту
    ("main.check_data", "Playlist.__len__"),
    ("main.remove_duplicates", "Playlist.__len__"),
    ("Catalog.statistics", "Playlist.__len__"),
    ("main.writer", "Playlist.__iter__"),
    ("main.recommend", "Playlist.__iter__"),
    ("Catalog.find_film", "Playlist.__iter__"),
    ("Catalog.statistics", "Playlist.__iter__"),
]
