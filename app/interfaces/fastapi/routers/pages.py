from collections import defaultdict
from datetime import datetime
from typing import Callable, Optional, Any
from urllib import request
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from ..user_settings import page_size

from ..deps import get_film_service, get_log_service
from app.core.services import FilmSearchService, QueryLogService

router = APIRouter()
templates = Jinja2Templates(directory="app/interfaces/fastapi/templates")

# print("=== PAGES.PY LOADED v.1.0 ===", datetime.now())


@router.get("/")
def home(request: Request):
    # print("home", datetime.now())
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/search/keyword")
def keyword_form(request: Request,
                 keyword: str | None = None,
                 page: int = Query(1, ge=1),
                 service: FilmSearchService = Depends(get_film_service)):
    # print("keyword_form", datetime.now(), keyword, page)

    if not keyword:
        # пустая страница формы, без поиска
        context = {
            "request": request,
            "title": "Search by keyword",
            "keyword": "",
            "items": [],
            "columns": ["title", "genre", "year"],
            "has_prev": False,
            "has_next": False,
            "offset": 0,
            "page_size": page_size,
            "page": 1,
        }
        return templates.TemplateResponse("keyword.html", context)

    context = get_context_films_table(service=service, method='keyword', keyword=keyword, page=page)
    context.update({"request": request})

    # print('keyword_form 3', datetime.now(), context)
    return templates.TemplateResponse(
        "keyword.html",
        context,
    )


@router.post("/search/keyword")
def keyword_page(
        request: Request,
        keyword: str = Form(...),
        page: int = Query(1, ge=1),
):
    qs = urlencode({"keyword": keyword, "page": 1})
    # print("keyword_page", datetime.now(), keyword, page)
    return RedirectResponse(url=f"?{qs}", status_code=303)


@router.get("/genres")
def categories(request: Request, service: FilmSearchService = Depends(get_film_service)):
    # print("categories", datetime.now())
    items = service.list_all_categories()
    genres = [g.get("category_name") for g in items]

    return templates.TemplateResponse(
        "genres.html",
        {"request": request, "genres": genres},
    )


@router.get("/genres/{genre}")
def genre_page(request: Request, genre: str, page: int = 1, service: FilmSearchService = Depends(get_film_service)):
    # print("genre_page 111", datetime.now(), genre, page)

    context = get_context_films_table(service=service, method='genre', genre=genre, page=page)
    context.update({"request": request})
    return templates.TemplateResponse(
        "genre.html",
        context,
    )


@router.get("/search/genre_year")
def genre_year_form(request: Request,
                    genre: str | None = None,
                    year_from: int | None = None,
                    year_to: int | None = None,
                    page: int = 1,
                    service: FilmSearchService = Depends(get_film_service)):
    # print("get.genre_year", datetime.now(), genre, year_from, year_to, page)

    # список жанров для выпадающего списка
    all_categories = service.list_all_categories()
    genres = [c.get("category_name") for c in all_categories]

    if not genre:
        context = {
            "request": request,
            "title": "Search by year",

            "genres": genres,  # <-- ВАЖНО
            "selected_genre": "",  # <-- шаблон это использует
            "year_from": "",
            "year_to": "",
            "items": [],
            "columns": ["title", "genre", "year"],
            "has_prev": False,
            "has_next": False,
            "offset": 0,
            "page_size": page_size,
            "page": 1,
        }
        return templates.TemplateResponse("genre_year.html", context)

    context = get_context_films_table(
        service=service,
        method="genre_year",
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        page=page,
        page_size=page_size,
    )
    context.update({
        "request": request,
        "genres": genres,
        "selected_genre": genre,
        "year_from": year_from or "",
        "year_to": year_to or "",
    })
    return templates.TemplateResponse("genre_year.html", context)


@router.post("/search/genre_year")
def genre_year_page(
        genre: str = Form(...),
        year_from: int = Form(...),
        year_to: int = Form(...),
):
    # print("post.genre_year", datetime.now(), genre, year_from, year_to)
    qs = urlencode({"genre": genre, "year_from": year_from, "year_to": year_to, "page": 1})
    return RedirectResponse(url=f"/search/genre_year?{qs}", status_code=303)


def get_context_films_table(
        service: FilmSearchService = Depends(get_film_service),
        method: str | None = None,
        keyword: str | None = None,
        genre: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        page: int = 1,
        page_size: int = 10,
):
    context = result = defaultdict()
    # print("films_table", datetime.now())

    log = page == 1
    if page == 0:
        page = 1

    if method == 'keyword':
        result = service.search_by_keyword(keyword, page_size=page_size, page=page, log=log)
        pages = result.get("pages", 1)

        # print("pages", pages, "page", page)
        if page > pages:
            page = max(pages, 1)
            result = service.search_by_keyword(keyword, page_size=page_size, page=page, log=log)

        # print('3', datetime.now())
        count_films = result.get("total", 0)
        context.update(
            {
                "title": f"Keyword: {keyword} - {count_films} films",
                "keyword": keyword,
            },
        )

    elif method == 'genre':
        dict_category = service.get_dict_category_by_name(genre)
        result = service.search_by_category(dict_category, page_size=page_size, page=page, log=log)
        pages = result.get("pages", 1)

        # print("pages", pages, "page", page)
        if page > pages:
            page = pages
            result = service.search_by_category(dict_category, page_size=page_size, page=page, log=log)

        count_films = result.get("total", 0)
        context.update(
            {
                "title": f"Genre: {genre} - {count_films} films",
                "genre": genre,
            },
        )

    elif method == 'genre_year':
        dict_category = service.get_dict_category_by_name(genre)
        result = service.search_by_category_year(dict_category,
                                                 year_from=year_from, year_to=year_to,
                                                 page_size=page_size, page=page, log=log)
        pages = result.get("pages", 1)

        # print("pages", pages, "page", page)
        if page > pages:
            page = pages
            result = service.search_by_category_year(dict_category,
                                                     year_from=year_from, year_to=year_to,
                                                     page_size=page_size, page=page, log=log)

        count_films = result.get("total", 0)
        context.update(
            {
                "title": f"Genre: {genre} ({year_from}-{year_to}) - {count_films} films",
                "genre": genre,
            },
        )
    else:
        context.update({"request": request})

    renamed = [{**item,
                "genre": item["category_name"],
                "year": item["release_year"], }
               for item in result.get("items", [])
               ]

    for item in renamed:
        item.pop("category_name")
        item.pop("release_year")

    start_i = page * page_size - page_size

    has_prev = page > 1
    has_next = page < result.get("pages", 1)

    context.update({
        "items": renamed,
        "columns": ["title", "genre", "year"],
        "has_prev": has_prev,
        "has_next": has_next,
        "offset": start_i,
        "page_size": page_size,
        "page": page, })

    return context


# statistics

@router.get("/statistics")
def statistics(request: Request, q_service: QueryLogService = Depends(get_log_service)):
    # print("statistics", datetime.now())
    last_unique = q_service.get_last_unique_queries()
    top_5_q = q_service.get_top_queries(5)

    context = {"last_unique": last_unique, "top_5_q": top_5_q,
               "request": request}

    return templates.TemplateResponse(
        "statistics.html",
        context,
    )
