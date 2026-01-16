from pprint import pprint

from app.core.services import FilmSearchService, QueryLogService
from app.interfaces.cli.user_settings import msg, page_size
from app.interfaces.cli import formatters


def search_film_by_keyword(fs_service: FilmSearchService):
    user_input = input(msg.menu_keyword).strip()
    paginate(fs_service.search_by_keyword, keyword=user_input)


def select_category(fs_service: FilmSearchService):
    list_category = fs_service.list_all_categories()
    dict_category = None

    formatters.print_categories(list_category)

    user_input = input(msg.menu_category).strip()
    if user_input.isnumeric():
        selected_index = int(user_input)
        if selected_index - 1 >= len(list_category) or selected_index <= 0:
            print(msg.input_error)
            return None
        category = list_category[selected_index - 1]
        category_id = category.get('category_id')
        category_name = category.get('name')
        dict_category = {"category_id": category_id, "category_name": category_name}
    return dict_category


def search_film_by_category(fs_service: FilmSearchService):
    dict_category = select_category(fs_service)
    if dict_category is None:
        return None

    paginate(fs_service.search_by_category, dict_category=dict_category)


def normalize_year_range_input(period, year_1: str, year_2: str):
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


def get_year_range_input(period):
    print(msg.period_info.format(name=period.get("name"),
                                 year_from=period.get("year_from"),
                                 year_to=period.get("year_to"),
                                 ))

    year_1 = input(msg.menu_period_from)
    year_2 = input(msg.menu_period_to)

    year_from, year_to = normalize_year_range_input(period, year_1, year_2)

    years = {"year_from": year_from, "year_to": year_to}

    return years


def search_film_by_category_year(fs_service: FilmSearchService):
    dict_category = select_category(fs_service)
    if dict_category is None:
        return None

    category_id = dict_category.get("category_id")

    get_period = fs_service.get_year_range_by_category(dict_category)
    if get_period is None:
        print(msg.not_found)
        return None

    years_period = get_year_range_input(get_period)
    year_from = years_period.get("year_from")
    year_to = years_period.get("year_to")

    paginate(fs_service.search_by_category_year, dict_category=dict_category, year_from=year_from, year_to=year_to)


def paginate(fetch_page_fn, **kwargs):
    pages = 1
    page = last_valid_page = 1
    kwargs['page_size'] = page_size

    is_first_page = True
    use_select = '1'
    while True:
        print("*" * 50, "\n")
        if not is_first_page:
            use_select = input(msg.menu_pagination).strip()

        if use_select == '0':
            break
        elif use_select.isnumeric():
            page = int(use_select)

        elif use_select.lower() == 'n':

            if page + 1 > pages:
                print(msg.no_next_page)
                continue
            else:
                page += 1

        elif use_select.lower() == 'p':
            if page - 1 <= 0:
                print(msg.no_prev_page)
                continue
            else:
                page -= 1
        else:
            print(msg.input_error)
            continue

        if page <= pages:
            kwargs['page'] = page
            result = fetch_page_fn(log=is_first_page, **kwargs)
            items = result.get('items')
            if items:
                start_i = page * page_size - page_size + 1
                last_valid_page = page
                formatters.print_films(items, start_i)
            else:
                print(msg.not_found)
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


def get_top_5queries():
    qs = QueryLogService()
    result = qs.get_top_queries(limit=5)
    formatters.print_top_queries(result)
    input(msg.press_enter_to_return_to_menu)


def get_last_unique_queries():
    qs = QueryLogService()
    result = qs.get_last_unique_queries()
    formatters.print_last_unique_queries(result)
    input(msg.press_enter_to_return_to_menu)