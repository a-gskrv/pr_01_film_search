class RuCliMessages():
    main_menu: str = """
Поиск фильмов:
1. по ключевому слову.
2. по жанру.
3. по жанру и периоду.

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

    period_info = "Для жанра {name} фильмы доступны за период с {year_from} по {year_to}"

    page_info = "Страница {page} из {pages}"

    no_next_page: str = "Нет следующей страницы!"
    no_prev_page: str = "Нет предыдущей страницы!"
    invalid_page_number: str = "Страницы {page} не существует. Доступно страниц: {pages}."

    not_found: str = "Не найдено!"
    input_error: str = "Ошибка ввода"


class EnCliMessages():
    main_menu: str = """
Film search:
1. by keyword.
2. by category.
3. by category and period.

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

    period_info = "For category {name}, films are available from {year_from} to {year_to}"

    page_info = "Page {page} of {pages}"

    no_next_page: str = "No next page!"
    no_prev_page: str = "No previous page!"
    invalid_page_number: str = "Page {page} does not exist. Total pages: {pages}."

    not_found: str = "Not found!"
    input_error: str = "Invalid input"

#
# menu_keyword_ru = """
# Введите ключевое слово: """
#
# menu_keyword_en = """
# Enter a keyword: """
#
# menu_category_ru = """
# Введите номер выбранного жанра: """
#
# menu_category_en = """
# Enter the selected category number: """
#
# menu_period_from_ru = """
# Введите год начала периода: """
#
# menu_period_to_ru = """
# Введите год окончания периода: """
#
# menu_period_from_en = """
# Enter the start year: """
#
# menu_period_to_en = """
# Enter the end year: """
#
# menu_pagination_ru = """
# Введите для навигации по страницам: Следующая - N, Предыдущая - P, Выход - 0, или введите номер страницы: """
#
# menu_pagination_en = """
# Navigation: Next - N, Previous - P, Quit - Q, or enter a page number: """
#
#
#
