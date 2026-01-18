import subprocess
import sys


def main():
    while True:
        print("\nSelect interface:")
        print("1) CLI")
        print("2) FastAPI")
        print("0) Exit")

        choice = input("> ").strip()

        if choice == "1":
            from app.interfaces.cli.main import main as cli_main
            cli_main()

        elif choice == "2":
            print("Starting FastAPI server...")

            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.interfaces.fastapi.main:app",
                    "--reload",
                    "--port", "8001"

                ]
            )

            print("FastAPI is running at http://127.0.0.1:8001")
            input("Press Enter to stop the server and return to the menu...")

            proc.terminate()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
