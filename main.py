# main.py
# Entry point of the Expense Tracker & Budget Monitor application.
# This file initializes database tables and starts the CLI menu.

from lib.database import create_tables
from lib.cli import main_menu

if __name__ == "__main__":
    create_tables()   # Ensure required tables exist
    main_menu()       # Launch the main interactive menu
