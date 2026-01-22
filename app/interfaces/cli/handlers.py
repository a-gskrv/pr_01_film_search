from typing import Optional, Callable, Any

from app.core.services import FilmSearchService, QueryLogService
from app.interfaces.cli.user_settings import msg, page_size
from app.interfaces.cli import formatters
from app.interfaces.cli.utils import clear_screen

utils_clear_screen = clear_screen
fs_service = FilmSearchService()

def search_film_by_keyword() -> None:
    """
    Search films by keyword using interactive pagination.

    """
    user_input = input(msg.menu_keyword).strip()
    header_text = msg.films_by_keyword_header.format(keyword=user_input)
    render_page = formatters.print_films
    paginate(fs_service.search_by_keyword, render_page, header_text=header_text, keyword=user_input)


def select_category() -> Optional[dict]:
    """
        Display categories and prompt the user to select one.

        Returns:
            dict | None: Selected category info:
                - category_id (int)
                - category_name (str)
            Returns None if input is invalid.
        """
    list_category = fs_service.list_all_categories()
    dict_category = None

    formatters.print_categories(list_category)

    user_input = input(msg.menu_category).strip()
    if user_input.isnumeric():
        selected_index = int(user_input)
        if selected_index - 1 >= len(list_category) or selected_index <= 0:
            return None
        category = list_category[selected_index - 1]
        category_id = category.get('category_id')
        category_name = category.get('category_name')
        dict_category = {"category_id": category_id, "category_name": category_name}
    else:
        return None
    return dict_category


def search_film_by_category() -> None:
    """
    Search films by category using interactive pagination.
    """
    dict_category = select_category()
    if dict_category is None:
        print(msg.input_error)
        input(msg.press_enter_to_return_to_menu)
        return None

    header_text = msg.films_by_category_header.format(category_name=dict_category.get('category_name', '...'))

    render_page = formatters.print_films
    paginate(fs_service.search_by_category, render_page, header_text, dict_category=dict_category)


def normalize_year_range_input(period: dict[str, Any], year_1: str, year_2: str) -> tuple[int, int]:
    """
    Normalize user input for year range.

    Args:
        period: Dict with available year range (year_from/year_to).
        year_1: User input for the first year.
        year_2: User input for the second year.

    Returns:
        tuple[int, int]: Normalized (year_from, year_to).
    """

    if year_1.isnumeric():
        year_1 = int(year_1)
    else:
        year_1 = None

    if year_2.isnumeric():
        year_2 = int(year_2)
    else:
        year_2 = None

    if year_1 == year_2 == None or year_1 == year_2 == 0:
        year_1, year_2 = period.get("year_from"), period.get("year_to")
    elif year_1 == None or year_1 == 0:
        year_1 = year_2
    elif year_2 == None or year_2 == 0:
        year_2 = year_1

    year_from = min(year_1, year_2)
    year_to = max(year_1, year_2)

    return year_from, year_to


def get_year_range_input(period: dict[str, Any]) -> dict[str, int]:
    """
    Prompt the user to enter a year range.

    Args:
        period: Dict with available period info (min/max years).

    Returns:
        dict: Normalized year range: {"year_from": int, "year_to": int}.
    """
    print(msg.period_info.format(category_name=period.get("category_name"),
                                 year_from=period.get("year_from"),
                                 year_to=period.get("year_to"),
                                 ))

    year_1 = input(msg.menu_period_from)
    year_2 = input(msg.menu_period_to)

    year_from, year_to = normalize_year_range_input(period, year_1, year_2)

    years = {"year_from": year_from, "year_to": year_to}

    return years

def search_film_by_category_year():
    """Search films by category and year range using interactive pagination."""
    dict_category = select_category()
    if dict_category is None:
        print(msg.input_error)
        input(msg.press_enter_to_return_to_menu)
        return None

    get_period = fs_service.get_year_range_by_category(dict_category)
    if get_period is None:
        print(msg.not_found)
        return None

    years_period = get_year_range_input(get_period)
    year_from = years_period.get("year_from")
    year_to = years_period.get("year_to")
    text_period = f"{year_from} - {year_to}"

    header_text = msg.films_by_category_period_header.format(category_name=dict_category.get('category_name', '...'),
                                                             period=text_period)
    render_page = formatters.print_films

    paginate(fs_service.search_by_category_year, render_page, header_text,
             dict_category=dict_category, year_from=year_from, year_to=year_to)



def apply_pagination_command(is_first_page: bool, page: int, pages: int) -> tuple[int, Optional[str]]:
    """
    Read a pagination command from user input and calculate the next page number.

    Args:
        is_first_page: If True, the function does not ask for user input and uses the default command
            to display the first page.
        page: Current page number.
        pages: Total number of pages.

    Returns:
        tuple:
            - page (int): Updated page number. Returns 0 if user selected exit.
            - error_msg (str | None): Error message if the command is invalid or not allowed.
    """
    if not is_first_page:
        use_select = input(msg.menu_pagination).strip()
    else:
        use_select = "1"

    error_msg = None
    if use_select == '0':
        page = 0
    elif use_select.isnumeric():
        page = int(use_select)
    elif use_select.lower() == 'n':
        if page + 1 > pages:
            error_msg = msg.no_next_page
        else:
            page += 1
    elif use_select.lower() == 'p':
        if page - 1 <= 0:
            error_msg = msg.no_prev_page
        else:
            page -= 1
    else:
        error_msg = msg.input_error
    return page, error_msg


def paginate(fetch_page_fn: Callable[..., dict],
             render_page: Callable[[list[dict], int], None],
             header_text: Optional[str] = None,
             **kwargs: Any,
             ) -> None:
    """
    Run an interactive pagination loop.

    The function requests paginated data using `fetch_page_fn` and displays items using
    the provided `render_page` function.

    Args:
        fetch_page_fn: Function that returns paginated data in the standard format:
            {
                "items": list,
                "total": int,
                "page": int,
                "page_size": int,
                "pages": int
            }
        render_page: Function that prints a list of result items to the screen.
            It receives:
                - items: list of result items
                - start_i: start index for numbering (1-based)
        header_text: Optional text printed above the page results.
        **kwargs: Extra parameters passed to `fetch_page_fn`.

    Returns:
        None
    """
    pages = 1
    page = last_valid_page = 1
    kwargs['page_size'] = page_size

    is_first_page = True
    while True:
        print("*" * 50, "\n")
        page, error_msg = apply_pagination_command(is_first_page, page, pages)
        if page == 0:
            break
        elif error_msg:
            print(error_msg)
            continue

        if page <= pages:
            utils_clear_screen()
            if header_text:
                print(header_text)
            kwargs['page'] = page
            result = fetch_page_fn(log=is_first_page, **kwargs)
            items = result.get('items')
            if items:
                start_i = page * page_size - page_size + 1
                last_valid_page = page
                render_page(items, start_i)
            else:
                print(msg.not_found)
                input(msg.press_enter_to_return_to_menu)
                break
            pages = result['pages']
            print(msg.page_info.format(page=page, pages=pages))

            if result['pages'] == 1:
                input(msg.press_enter_to_return_to_menu)
                break
        else:
            print(msg.invalid_page_number.format(page=page, pages=pages))
            page = last_valid_page

        is_first_page = False


def show_top_5queries():
    """Display the top 5 most frequent search queries."""
    qs = QueryLogService()
    result = qs.get_top_queries(limit=5)
    print(msg.top_queries_header)
    formatters.print_top_queries(result)
    input(msg.press_enter_to_return_to_menu)


def show_last_unique_queries():
    """Display the last unique search queries."""
    qs = QueryLogService()
    result = qs.get_last_unique_queries()
    print(msg.last_queries_header)
    formatters.print_last_unique_queries(result)
    input(msg.press_enter_to_return_to_menu)


def show_all_reports():
    """Display the last unique search queries."""
    qs = QueryLogService()

    result = qs.get_last_unique_queries()
    print(msg.last_queries_header)
    formatters.print_last_unique_queries(result)

    print("*" * 50, "\n")

    result = qs.get_top_queries(limit=5)
    print(msg.top_queries_header)
    formatters.print_top_queries(result)

    input(msg.press_enter_to_return_to_menu)