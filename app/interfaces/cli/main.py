from app.core.services import FilmSearchService
from app.interfaces.cli.user_settings import msg
from app.interfaces.cli import handlers

fs_service = FilmSearchService()



def main():
    while True:
        user_choice = input(msg.main_menu).strip()
        print("*" * 50, "\n")
        if user_choice == '0':
            break
        elif user_choice == '1':
            handlers.search_film_by_keyword(fs_service)
        elif user_choice == '2':
            handlers.search_film_by_category(fs_service)
        elif user_choice == '3':
            handlers.search_film_by_category_year(fs_service)


if __name__ == '__main__':
    main()
