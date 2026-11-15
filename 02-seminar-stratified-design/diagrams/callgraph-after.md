# Метрики графа: Граф вызовов: после изменений

Файл создан скриптом `callgraph.py`. Длина стрелки — на сколько подуровней она опускается.

| Показатель | Значение |
|---|---|
| Слоёв с назначением (вместе с «Язык Python») | 9 |
| Подуровней | 19 |
| Функций и методов | 175 |
| — из них действие | 52 |
| — из них вычисление | 123 |
| Стрелок | 501 |
| Самая длинная стрелка между функциями, слоёв | 4 |
| Стрелок между функциями через 3 слоя и больше | 16 |
| Самая длинная стрелка вообще, подуровней | 18 |
| Функций, напрямую использующих конструкции языка | 70 |
| Функций верхних слоёв, напрямую зависящих от данных и языка | 1 |
| Обращений к внутренностям каталога и плейлиста извне | 0 |

## Слои сверху вниз

**Приложение: цикл меню** (подуровень 18, узлов: 1): `main.main`

**Сценарии меню** (подуровни 15–17, узлов: 20): `commands.add_to_viewer_playlist`, `commands.rate_film`, `commands.watch_film`, `commands.recommend`, `commands.sort_by_name`, `commands.sort_by_rating`, `commands.viewer_profile`, `commands.with_viewer_and_film`, `commands.compare`, `commands.filter_films`, `commands.load_from_file`, `commands.load_test_data`, `commands.raise_rating`, `commands.register_viewer`, `commands.remove_duplicates`, `commands.save_to_file`, `commands.show_all`, `commands.sort_films`, `commands.statistics`, `commands.with_viewer`

**Операции: диалоги, файлы, история, каталог** (подуровни 12–14, узлов: 51): `Catalog.raise_rating`, `Catalog.rate`, `Catalog.watch`, `constructors.make_test_catalog`, `Catalog.add_to_playlist`, `Catalog.check_not_empty`, `Catalog.films_of_genre`, `Catalog.films_of_kind`, `Catalog.replace_film`, `Catalog.sorted_by_name`, `Catalog.sorted_by_rating`, `Catalog.statistics`, `Catalog.with_viewer`, `Catalog.without_duplicates`, `dialogs.choose_film`, `dialogs.choose_viewer`, `dialogs.report_error`, `dialogs.show_found`, `dialogs.undo`, `storage.load_catalog`, `storage.save_catalog`, `Catalog.__init__`, `Catalog.all_films`, `Catalog.can_raise`, `Catalog.compare`, `Catalog.film_at`, `Catalog.film_count`, `Catalog.films_where`, `Catalog.find_viewer`, `Catalog.has_viewers`, `Catalog.is_empty`, `Catalog.recommendations_for`, `Catalog.replace_viewer`, `Catalog.viewer_names`, `Catalog.with_films`, `constructors.make_test_films`, `dialogs.ask_filename`, `dialogs.ask_filter`, `dialogs.ask_menu_choice`, `dialogs.ask_new_filename`, `dialogs.ask_new_viewer`, `dialogs.ask_score`, `dialogs.goodbye`, `dialogs.greet`, `dialogs.show_cards`, `dialogs.show_films`, `dialogs.wrong_menu_item`, `history.can_undo`, `history.remember`, `history.undone`, `storage.write_error_log`

**Строительные блоки: представление, формат файла, консоль, плейлист, запросы** (подуровни 9–11, узлов: 64): `console.show_sections`, `queries.recommendations`, `queries.statistics`, `records.parse_films`, `views.film_details`, `Playlist.filtered`, `Playlist.replaced`, `Playlist.sorted_with`, `Playlist.unique_by`, `console.show_section`, `queries.compare_films`, `queries.most_viewed`, `queries.sorted_by_name`, `queries.sorted_by_rating`, `queries.top_by_rating`, `records.films_to_lines`, `records.parse_cinematography`, `views.numbered`, `views.serial_extra`, `Playlist.__init__`, `Playlist.__iter__`, `Playlist.__len__`, `Playlist.at`, `console.ask_number`, `console.ask_text`, `console.banner`, `console.card_title`, `console.error`, `console.header`, `console.notice`, `console.show`, `console.show_lines`, `console.success`, `queries.average_rating_by_genre`, `queries.better_of`, `queries.by_rating`, `queries.by_title_and_year`, `queries.genre_matches`, `queries.has_favorite_genre`, `queries.identity`, `queries.is_kind`, `queries.is_known_kind`, `queries.total_views`, `records.make_cartoon`, `records.make_film`, `records.make_serial`, `records.to_record`, `records.with_default_extension`, `views.added_message`, `views.cartoon_extra`, `views.common_details`, `views.comparison_lines`, `views.duplicates_message`, `views.film_extra`, `views.max_rating_message`, `views.menu_lines`, `views.profile_section`, `views.raised_message`, `views.rated_message`, `views.recommendations_section`, `views.registered_message`, `views.statistics_sections`, `views.viewers_line`, `views.watched_message`

**Сущности: произведения и зрители** (подуровни 4–8, узлов: 21): `Serial.__init__`, `Cartoon.__init__`, `Film.__init__`, `Cinematography.__init__`, `Cartoon.kind=`, `Cinematography.rating=`, `Cinematography.release=`, `Cinematography.with_raised_rating`, `Film.budget=`, `Film.effect=`, `Serial.seasons=`, `Serial.series=`, `Viewer.rated`, `Cinematography.can_raise_rating`, `Cinematography.with_view`, `Cinematography.with_vote`, `Viewer.__init__`, `Viewer.has_watched`, `Viewer.watched`, `Viewer.with_in_playlist`, `cinematography.checked`

**Правила предметной области** (подуровень 3, узлов: 6): `rules.can_raise_rating`, `rules.is_valid_rating`, `rules.is_valid_year`, `rules.parse_genres`, `rules.rating_from_votes`, `rules.split_genres`

**Общие операции** (подуровень 2, узлов: 12): `generic.average`, `generic.copy_with`, `generic.find_first`, `generic.group_by`, `generic.is_positive`, `generic.item_at`, `generic.one_of`, `generic.replaced`, `generic.same_text`, `generic.sorted_by`, `generic.split_list`, `generic.unique_by`

**Данные** (подуровень 1, узлов: 18): `Cartoon: поля`, `Catalog: поля`, `Cinematography: поля`, `Comparison: поля`, `EmptyPlaylistException`, `Film: поля`, `FilmotekaError`, `IdenticalMoviesException`, `InvalidPropertyException`, `NoDataUploadedException`, `NumberFilmException`, `Playlist: поля`, `RatingException`, `ReadingFromFileException`, `Serial: поля`, `Statistics: поля`, `Viewer: поля`, `ViewerException`

**Язык Python** (подуровень 0, узлов: 36): `any()`, `copy.copy`, `datetime.now`, `dict.get`, `dict.items`, `dict.setdefault`, `enumerate()`, `file.read`, `file.write`, `for`, `getattr()`, `input()`, `int()`, `isinstance()`, `iter()`, `len()`, `list.append`, `open()`, `print()`, `round()`, `set()`, `set.add`, `setattr()`, `sorted()`, `str()`, `str.join`, `str.lower`, `str.split`, `str.splitlines`, `str.strip`, `sum()`, `traceback.format_exc`, `tuple()`, `type()`, `индекс [ ]`, `срез [:]`

## Стрелки между функциями через 3 слоя и больше

- `Catalog.find_viewer` (Операции: диалоги, файлы, история, каталог) → `generic.find_first` (Общие операции), слоёв: 4
- `Catalog.find_viewer` (Операции: диалоги, файлы, история, каталог) → `generic.same_text` (Общие операции), слоёв: 4
- `Catalog.replace_viewer` (Операции: диалоги, файлы, история, каталог) → `generic.copy_with` (Общие операции), слоёв: 4
- `Catalog.replace_viewer` (Операции: диалоги, файлы, история, каталог) → `generic.replaced` (Общие операции), слоёв: 4
- `Catalog.with_films` (Операции: диалоги, файлы, история, каталог) → `generic.copy_with` (Общие операции), слоёв: 4
- `Catalog.with_viewer` (Операции: диалоги, файлы, история, каталог) → `generic.copy_with` (Общие операции), слоёв: 4
- `Playlist.at` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.item_at` (Общие операции), слоёв: 3
- `Playlist.replaced` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.replaced` (Общие операции), слоёв: 3
- `Playlist.unique_by` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.unique_by` (Общие операции), слоёв: 3
- `dialogs.ask_new_viewer` (Операции: диалоги, файлы, история, каталог) → `rules.parse_genres` (Правила предметной области), слоёв: 3
- `queries.average_rating_by_genre` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.average` (Общие операции), слоёв: 3
- `queries.average_rating_by_genre` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.group_by` (Общие операции), слоёв: 3
- `queries.most_viewed` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.sorted_by` (Общие операции), слоёв: 3
- `queries.sorted_by_name` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.sorted_by` (Общие операции), слоёв: 3
- `queries.sorted_by_rating` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.sorted_by` (Общие операции), слоёв: 3
- `queries.top_by_rating` (Строительные блоки: представление, формат файла, консоль, плейлист, запросы) → `generic.sorted_by` (Общие операции), слоёв: 3

## Обращения к внутренностям каталога и плейлиста извне

Нет.

## Функции верхних слоёв, напрямую зависящие от данных и языка

- `main.main`
