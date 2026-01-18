class RuCliMessages:
    main_menu: str = """
*********** ГЛАВНОЕ МЕНЮ *********** 
Поиск фильмов:
1. по ключевому слову.
2. по жанру.
3. по жанру и периоду.

Отчеты:
4. Пять последних запросов.
5. Топ пять популярных запросов.

0. Выход.

Введите номер пункта меню: """

    menu_keyword: str = """
Введите ключевое слово: """

    menu_category: str = """
Введите номер выбранного жанра: """

    menu_period_from: str = """
Введите год начала периода: """

    menu_period_to: str = """
Введите год окончания периода: """

    menu_pagination: str = """
Введите для навигации по страницам: Следующая - N, Предыдущая - P, Выход - 0, или введите номер страницы: """

    period_info = "Для жанра {category_name} фильмы доступны за период с {year_from} по {year_to}"

    page_info = "Страница {page} из {pages}"

    no_next_page: str = "Нет следующей страницы!"
    no_prev_page: str = "Нет предыдущей страницы!"
    invalid_page_number: str = "Страницы {page} не существует. Доступно страниц: {pages}."

    not_found: str = "Не найдено!"
    input_error: str = "Ошибка ввода."

    press_enter_to_return_to_menu = "Нажмите Enter, чтобы вернуться в меню."

    films_by_keyword_header = "Фильмы по ключевому слову: '{keyword}'"
    films_by_category_header = "Фильмы в жанре: '{category_name}'"
    films_by_category_period_header = "Фильмы в жанре: '{category_name}' за период: '{period}'"

class EnCliMessages:
    main_menu: str = """
*********** MAIN MENU ***********
Film search:
1. by keyword.
2. by category.
3. by category and period.

Reports:
4. Last 5 unique queries.
5. Top 5 most frequent queries.

0. Exit.

Enter the menu item number: """

    menu_keyword: str = """
Enter a keyword: """

    menu_category: str = """
Enter the selected category number: """

    menu_period_from: str = """
Enter the start year: """

    menu_period_to: str = """
Enter the end year: """

    menu_pagination: str = """
Navigation: Next - N, Previous - P, Quit - 0, or enter a page number: """

    period_info = "For category {category_name}, films are available from {year_from} to {year_to}"

    page_info = "Page {page} of {pages}"

    no_next_page: str = "No next page!"
    no_prev_page: str = "No previous page!"
    invalid_page_number: str = "Page {page} does not exist. Total pages: {pages}."

    not_found: str = "Not found!"
    input_error: str = "Invalid input"

    press_enter_to_return_to_menu = "Press Enter to return to the menu."

    films_by_keyword_header = "Films by keyword: '{keyword}'"
    films_by_category_header = "Films in category: '{category_name}'"
    films_by_category_period_header = "Films in category: '{category_name}' for period: '{period}'"


class DeCliMessages:
    main_menu: str = """
*********** HAUPTMENÜ ***********
Filmsuche:
1. nach Stichwort.
2. nach Kategorie.
3. nach Kategorie und Zeitraum.

Berichte:
4. Letzte 5 eindeutige Suchanfragen.
5. Top 5 häufigste Suchanfragen.

0. Beenden.

Menüpunkt eingeben: """

    menu_keyword: str = """
Stichwort eingeben: """

    menu_category: str = """
Nummer der Kategorie eingeben: """

    menu_period_from: str = """
Startjahr eingeben: """

    menu_period_to: str = """
Endjahr eingeben: """

    menu_pagination: str = """
Navigation: Nächste - N, Vorherige - P, Beenden - 0, oder Seitenzahl eingeben: """

    period_info = "Für die Kategorie {category_name} sind Filme im Zeitraum von {year_from} bis {year_to} verfügbar"

    page_info = "Seite {page} von {pages}"

    no_next_page: str = "Keine nächste Seite!"
    no_prev_page: str = "Keine vorherige Seite!"
    invalid_page_number: str = "Seite {page} existiert nicht. Verfügbare Seiten: {pages}."

    not_found: str = "Nicht gefunden!"
    input_error: str = "Ungültige Eingabe"

    press_enter_to_return_to_menu = "Drücken Sie Enter, um zum Menü zurückzukehren."

    films_by_keyword_header = "Filme nach Stichwort: '{keyword}'"
    films_by_category_header = "Filme in der Kategorie: '{category_name}'"
    films_by_category_period_header = "Filme in der Kategorie: '{category_name}' im Zeitraum: '{period}'"

