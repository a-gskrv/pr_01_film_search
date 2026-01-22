from app.interfaces.cli.utils import clear_screen
from app.interfaces.cli.user_settings import msg
from app.interfaces.cli import handlers


def main():
    """Run the interactive CLI main menu loop."""
    while True:
        clear_screen()
        user_choice = input(msg.main_menu).strip()
        clear_screen()
        print("*" * 50, "\n")
        if user_choice == '0':
            break
        elif user_choice == '1':
            handlers.search_film_by_keyword()
        elif user_choice == '2':
            handlers.search_film_by_category()
        elif user_choice == '3':
            handlers.search_film_by_category_year()
        elif user_choice == '4':
            handlers.show_last_unique_queries()
        elif user_choice == '5':
            handlers.show_top_5queries()
        elif user_choice == '6':
            handlers.show_all_reports()
        else:
            print(msg.input_error)
            input(msg.press_enter_to_return_to_menu)


if __name__ == '__main__':
    main()
