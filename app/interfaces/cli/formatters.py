def print_films(items, start_i=1):
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('title')} ({item.get('release_year')})")


def print_categories(items, start_i=1):
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('name')}")
