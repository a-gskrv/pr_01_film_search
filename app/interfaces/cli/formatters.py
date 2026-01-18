from typing import Any


def print_films(items: list[dict[str, Any]], start_i: int = 1) -> None:
    """Print a numbered list of films."""
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('title')} ({item.get('release_year')})")


def print_categories(items: list[dict[str, Any]], start_i: int = 1) -> None:
    """Print a numbered list of categories."""
    for i, item in enumerate(items, start_i):
        print(f"{i}. {item.get('category_name')}")


def print_last_unique_queries(items: list[dict[str, Any]]) -> None:
    """Print the report of the last unique search queries."""
    row_fmt = "{idx:>2}  {type:<15}  {query:<25}  {timestamp:>30}  {results:>7}"
    print(row_fmt.format(idx="#", type="Query Type", query="Query", timestamp="Last timestamp", results="Results"))
    for item in items:
        print(row_fmt.format(**item))


def print_top_queries(items: list[dict[str, Any]]) -> None:
    """Print the report of the top search queries."""
    row_fmt = "{idx:>2}  {type:<15}  {query:<25}  {count:>5}  {results:>7}"
    print(row_fmt.format(idx="#", type="Query Type", query="Query", count="Count", results="Results"))
    for item in items:
        print(row_fmt.format(**item))
