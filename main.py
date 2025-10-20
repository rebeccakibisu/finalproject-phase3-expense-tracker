# main.py
# This is the main entry point of the Expense Tracker & Budget Monitor application.
# It initializes the database tables (if they don’t exist)
# and launches the Command-Line Interface (CLI) for user interaction.

from lib.database import create_tables
from lib.cli import main_menu

if __name__ == "__main__":
    create_tables()   # Create database tables if not yet created
    main_menu()       # Start the interactive CLI
