from database import create_tables
from menu import main_menu


def main():
    create_tables()
    main_menu()


if __name__ == "__main__":
    main()