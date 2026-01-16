from collections import defaultdict
from pprint import pprint


def print_films(items, start_i=1):
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('title')} ({item.get('release_year')})")


def print_categories(items, start_i=1):
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('name')}")


def get_text_query(item):
    q_type = item.get('search_type')
    text_query = ''
    if q_type == 'keyword':
        text_query = f"{item.get('keyword')}"
    elif q_type == 'category':
        text_query = f"{item.get('category')}"
    elif q_type == 'category_year':
        text_query = f"{item.get('category')} ({item.get('years_range')})"
    return text_query


def print_last_unique_queries(items):
    unique_queries = []

    row_fmt = "{idx:>2}  {type:<15}  {query:<25}  {timestamp:>30}  {results:>7}"
    print(row_fmt.format(idx="#", type="Query Type", query="Query", timestamp="Last timestamp", results="Results"))

    idx = 0
    for i, item in enumerate(items, 1):
        format_dict = defaultdict(str)
        q_type = item.get('search_type')

        format_dict["type"] = q_type

        text_query = get_text_query(item)

        format_dict["query"] = text_query

        format_dict["timestamp"] = item.get('timestamp')
        format_dict["results"] = item.get('results_count')

        if text_query not in unique_queries:
            unique_queries.append(text_query)
            idx += 1
            print(row_fmt.format(idx=idx, **format_dict))

        if idx >= 5:
            break

    # pprint(format_results)


def print_top_queries(items):
    row_fmt = "{idx:>2}  {type:<15}  {query:<25}  {count:>5}  {results:>7}"
    print(row_fmt.format(idx="#", type="Query Type", query="Query", count="Count", results="Results"))
    for i, item in enumerate(items, 1):
        format_dict = defaultdict(str)
        q_type = item.get('search_type')
        format_dict["idx"] = str(i)
        format_dict["type"] = q_type

        text_query = get_text_query(item)
        format_dict["query"] = text_query

        format_dict["count"] = item.get('count_query')
        format_dict["results"] = item.get('results_count')
        print(row_fmt.format(**format_dict))

        # pprint(f"{i}. {item.get('title')}")
    # pprint(format_results)
