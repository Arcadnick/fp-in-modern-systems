# Метрики графа: Граф вызовов: исходное состояние

Файл создан скриптом `callgraph.py`. Длина стрелки — на сколько подуровней она опускается.

| Показатель | Значение |
|---|---|
| Слоёв с назначением (вместе с «Язык Python») | 11 |
| Подуровней | 29 |
| Функций и методов | 143 |
| — из них действие | 33 |
| — из них вычисление | 110 |
| Стрелок | 486 |
| Самая длинная стрелка между функциями, слоёв | 7 |
| Стрелок между функциями через 3 слоя и больше | 49 |
| Самая длинная стрелка вообще, подуровней | 28 |
| Функций, напрямую использующих конструкции языка | 69 |
| Функций верхних слоёв, напрямую зависящих от данных и языка | 21 |
| Обращений к внутренностям каталога и плейлиста извне | 22 |

## Слои сверху вниз

**Цикл меню** (подуровень 28, узлов: 1): `main.main`

**Команды меню и их общие части** (подуровни 24–27, узлов: 23): `main.add_to_viewer_playlist`, `main.rate_film`, `main.watch_film`, `main.recommend`, `main.sort_by_name`, `main.sort_by_rating`, `main.viewer_profile`, `main.with_viewer_and_film`, `main.compare`, `main.filter_films`, `main.get_file`, `main.raise_up`, `main.register_viewer`, `main.remove_duplicates`, `main.sort_films`, `main.statistics`, `main.with_viewer`, `main.writer`, `main.check_data`, `main.choose_film`, `main.choose_viewer`, `main.get_data`, `main.test_database`

**Консоль и файлы** (подуровни 22–23, узлов: 10): `main.print_playlist`, `main.error`, `main.header`, `main.print_lines`, `main.print_menu`, `main.success`, `main.the_first_word`, `main.write_error_log`, `storage.load_playlist`, `storage.save_playlist`

**Конструкторы** (подуровни 19–21, узлов: 7): `constructors.parse_playlist`, `constructors.make_test_catalog`, `constructors.parse_cinematography`, `constructors.make_cartoon`, `constructors.make_film`, `constructors.make_serial`, `constructors.make_test_films`

**Каталог** (подуровни 16–18, узлов: 15): `Catalog.raise_rating`, `Catalog.rate`, `Catalog.watch`, `Catalog.add_to_playlist`, `Catalog.replace_film`, `Catalog.sorted_by_name`, `Catalog.sorted_by_rating`, `Catalog.with_viewer`, `Catalog.without_duplicates`, `Catalog.__init__`, `Catalog.find_film`, `Catalog.find_viewer`, `Catalog.replace_viewer`, `Catalog.statistics`, `Catalog.with_films`

**Зритель и плейлист** (подуровни 13–15, узлов: 27): `Playlist.sort_by_name`, `Playlist.sort_by_rating`, `Playlist.add_first`, `Playlist.add_last`, `Playlist.clear`, `Playlist.find_all`, `Playlist.get_first`, `Playlist.get_last`, `Playlist.remove`, `Playlist.remove_duplicates`, `Playlist.replace`, `Playlist.sort_with`, `Viewer.rated`, `Playlist.__init__`, `Playlist.__iter__`, `Playlist.__len__`, `Playlist.check_not_empty`, `Playlist.contains`, `Playlist.get_all`, `Playlist.numbered_lines`, `Playlist.to_lines`, `Viewer.__init__`, `Viewer.has_watched`, `Viewer.profile_lines`, `Viewer.recommend`, `Viewer.watched`, `Viewer.with_in_playlist`

**Операции над произведениями** (подуровни 8–12, узлов: 15): `Serial.__init__`, `Cartoon.__init__`, `Film.__init__`, `Cinematography.__init__`, `Cartoon.kind=`, `Cinematography.rating=`, `Cinematography.release=`, `Film.budget=`, `Film.effect=`, `Serial.seasons=`, `Serial.series=`, `Cinematography.with_raised_rating`, `Cinematography.with_view`, `Cinematography.with_vote`, `cinematography.checked`

**Вычисления (calculations.py)** (подуровни 5–7, узлов: 31): `calculations.recommendations`, `calculations.average_rating_by_genre`, `calculations.has_favorite_genre`, `calculations.most_viewed`, `calculations.rating_from_votes`, `calculations.sorted_by_rating`, `calculations.top_by_rating`, `calculations.average`, `calculations.better_of`, `calculations.by_rating`, `calculations.can_raise_rating`, `calculations.contains_same`, `calculations.copy_with`, `calculations.find_first`, `calculations.genre_matches`, `calculations.group_by`, `calculations.is_positive`, `calculations.is_valid_rating`, `calculations.is_valid_year`, `calculations.item_at`, `calculations.one_of`, `calculations.parse_genres`, `calculations.playlist_to_lines`, `calculations.replaced`, `calculations.same_text`, `calculations.sorted_by`, `calculations.sorted_by_name`, `calculations.split_genres`, `calculations.total_views`, `calculations.unique_by_line`, `calculations.with_default_extension`

**Представление произведений** (подуровни 2–4, узлов: 14): `Serial.details`, `Cartoon.details`, `Film.details`, `Cartoon.__str__`, `Cartoon.describe`, `Cinematography.__eq__`, `Cinematography.__lt__`, `Cinematography.__str__`, `Cinematography.describe`, `Cinematography.details`, `Film.__str__`, `Film.describe`, `Serial.__str__`, `Serial.describe`

**Данные** (подуровень 1, узлов: 16): `Cartoon: поля`, `Catalog: поля`, `Cinematography: поля`, `EmptyPlaylistException`, `Film: поля`, `FilmotekaError`, `IdenticalMoviesException`, `InvalidPropertyException`, `NoDataUploadedException`, `NumberFilmException`, `Playlist: поля`, `RatingException`, `ReadingFromFileException`, `Serial: поля`, `Viewer: поля`, `ViewerException`

**Язык Python** (подуровень 0, узлов: 36): `any()`, `copy.copy`, `datetime.now`, `dict.get`, `dict.items`, `dict.setdefault`, `enumerate()`, `file.read`, `file.write`, `for`, `input()`, `int()`, `isinstance()`, `iter()`, `len()`, `list.append`, `list.pop`, `open()`, `print()`, `round()`, `set()`, `set.add`, `setattr()`, `sorted()`, `str()`, `str.join`, `str.lower`, `str.split`, `str.splitlines`, `str.strip`, `sum()`, `traceback.format_exc`, `tuple()`, `type()`, `индекс [ ]`, `срез [:]`

## Стрелки между функциями через 3 слоя и больше

- `main.writer` (Команды меню и их общие части) → `Cinematography.describe` (Представление произведений), слоёв: 7
- `main.writer` (Команды меню и их общие части) → `Cinematography.details` (Представление произведений), слоёв: 7
- `main.choose_film` (Команды меню и их общие части) → `calculations.item_at` (Вычисления (calculations.py)), слоёв: 6
- `main.compare` (Команды меню и их общие части) → `calculations.better_of` (Вычисления (calculations.py)), слоёв: 6
- `main.filter_films` (Команды меню и их общие части) → `calculations.genre_matches` (Вычисления (calculations.py)), слоёв: 6
- `main.get_file` (Команды меню и их общие части) → `calculations.with_default_extension` (Вычисления (calculations.py)), слоёв: 6
- `main.register_viewer` (Команды меню и их общие части) → `calculations.parse_genres` (Вычисления (calculations.py)), слоёв: 6
- `storage.save_playlist` (Консоль и файлы) → `calculations.playlist_to_lines` (Вычисления (calculations.py)), слоёв: 5
- `main.check_data` (Команды меню и их общие части) → `Playlist.__len__` (Зритель и плейлист), слоёв: 4
- `main.choose_film` (Команды меню и их общие части) → `Playlist.get_all` (Зритель и плейлист), слоёв: 4
- `main.filter_films` (Команды меню и их общие части) → `Playlist.find_all` (Зритель и плейлист), слоёв: 4
- `main.recommend` (Команды меню и их общие части) → `Playlist.__iter__` (Зритель и плейлист), слоёв: 4
- `main.recommend` (Команды меню и их общие части) → `Viewer.recommend` (Зритель и плейлист), слоёв: 4
- `main.remove_duplicates` (Команды меню и их общие части) → `Playlist.__len__` (Зритель и плейлист), слоёв: 4
- `main.viewer_profile` (Команды меню и их общие части) → `Viewer.profile_lines` (Зритель и плейлист), слоёв: 4
- `main.writer` (Команды меню и их общие части) → `Playlist.__iter__` (Зритель и плейлист), слоёв: 4
- `Catalog.find_film` (Каталог) → `calculations.find_first` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.find_film` (Каталог) → `calculations.same_text` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.find_viewer` (Каталог) → `calculations.find_first` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.find_viewer` (Каталог) → `calculations.same_text` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.replace_viewer` (Каталог) → `calculations.copy_with` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.replace_viewer` (Каталог) → `calculations.replaced` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.statistics` (Каталог) → `calculations.average_rating_by_genre` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.statistics` (Каталог) → `calculations.most_viewed` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.statistics` (Каталог) → `calculations.top_by_rating` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.statistics` (Каталог) → `calculations.total_views` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.with_films` (Каталог) → `calculations.copy_with` (Вычисления (calculations.py)), слоёв: 3
- `Catalog.with_viewer` (Каталог) → `calculations.copy_with` (Вычисления (calculations.py)), слоёв: 3
- `Playlist.numbered_lines` (Зритель и плейлист) → `Cinematography.__str__` (Представление произведений), слоёв: 3
- `Playlist.to_lines` (Зритель и плейлист) → `Cinematography.__str__` (Представление произведений), слоёв: 3
- `constructors.make_cartoon` (Конструкторы) → `Cartoon.__init__` (Операции над произведениями), слоёв: 3
- `constructors.make_film` (Конструкторы) → `Film.__init__` (Операции над произведениями), слоёв: 3
- `constructors.make_serial` (Конструкторы) → `Serial.__init__` (Операции над произведениями), слоёв: 3
- `constructors.make_test_films` (Конструкторы) → `Cartoon.__init__` (Операции над произведениями), слоёв: 3
- `constructors.make_test_films` (Конструкторы) → `Film.__init__` (Операции над произведениями), слоёв: 3
- `constructors.make_test_films` (Конструкторы) → `Serial.__init__` (Операции над произведениями), слоёв: 3
- `main.add_to_viewer_playlist` (Команды меню и их общие части) → `Catalog.add_to_playlist` (Каталог), слоёв: 3
- `main.choose_viewer` (Команды меню и их общие части) → `Catalog.find_viewer` (Каталог), слоёв: 3
- `main.get_data` (Команды меню и их общие части) → `Catalog.__init__` (Каталог), слоёв: 3
- `main.print_playlist` (Консоль и файлы) → `Playlist.numbered_lines` (Зритель и плейлист), слоёв: 3
- `main.raise_up` (Команды меню и их общие части) → `Catalog.raise_rating` (Каталог), слоёв: 3
- `main.rate_film` (Команды меню и их общие части) → `Catalog.rate` (Каталог), слоёв: 3
- `main.register_viewer` (Команды меню и их общие части) → `Catalog.with_viewer` (Каталог), слоёв: 3
- `main.remove_duplicates` (Команды меню и их общие части) → `Catalog.without_duplicates` (Каталог), слоёв: 3
- `main.sort_by_name` (Команды меню и их общие части) → `Catalog.sorted_by_name` (Каталог), слоёв: 3
- `main.sort_by_rating` (Команды меню и их общие части) → `Catalog.sorted_by_rating` (Каталог), слоёв: 3
- `main.statistics` (Команды меню и их общие части) → `Catalog.statistics` (Каталог), слоёв: 3
- `main.watch_film` (Команды меню и их общие части) → `Catalog.watch` (Каталог), слоёв: 3
- `storage.save_playlist` (Консоль и файлы) → `Playlist.get_all` (Зритель и плейлист), слоёв: 3

## Обращения к внутренностям каталога и плейлиста извне

- `constructors.make_test_catalog` → `Playlist.__init__`
- `constructors.parse_playlist` → `Playlist.__init__`
- `main.check_data` → `Catalog: поля`
- `main.check_data` → `Playlist.__len__`
- `main.choose_film` → `Playlist.get_all`
- `main.choose_viewer` → `Catalog: поля`
- `main.compare` → `Catalog: поля`
- `main.filter_films` → `Catalog: поля`
- `main.filter_films` → `Playlist.find_all`
- `main.filter_films` → `Playlist: поля`
- `main.get_file` → `Catalog: поля`
- `main.print_playlist` → `Playlist.numbered_lines`
- `main.raise_up` → `Catalog: поля`
- `main.recommend` → `Catalog: поля`
- `main.recommend` → `Playlist.__iter__`
- `main.remove_duplicates` → `Catalog: поля`
- `main.remove_duplicates` → `Playlist.__len__`
- `main.sort_films` → `Catalog: поля`
- `main.with_viewer_and_film` → `Catalog: поля`
- `main.writer` → `Catalog: поля`
- `main.writer` → `Playlist.__iter__`
- `storage.save_playlist` → `Playlist.get_all`

## Функции верхних слоёв, напрямую зависящие от данных и языка

- `main.add_to_viewer_playlist`
- `main.check_data`
- `main.choose_film`
- `main.choose_viewer`
- `main.compare`
- `main.filter_films`
- `main.get_data`
- `main.get_file`
- `main.main`
- `main.raise_up`
- `main.rate_film`
- `main.recommend`
- `main.register_viewer`
- `main.remove_duplicates`
- `main.sort_films`
- `main.statistics`
- `main.test_database`
- `main.viewer_profile`
- `main.watch_film`
- `main.with_viewer_and_film`
- `main.writer`
