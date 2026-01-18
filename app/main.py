def main():
    while True:
        print("\nSelect interface:")
        print("1) CLI")
        print("2) FastAPI (coming soon)")
        print("0) Exit")

        choice = input("> ").strip()

        if choice == "1":
            from app.interfaces.cli.main import main as cli_main
            cli_main()

        elif choice == "2":
            print("FastAPI is not implemented yet.")
            input("Press Enter to return to the menu...")

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
