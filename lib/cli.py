# lib/cli.py
# Command-line interface for interacting with the Expense Tracker system.
# Includes CRUD, summary reports, and search/filter features.
# Uses only built-in Python to draw tables (no external libraries).

from lib.models.user import User
from lib.models.category import Category
from lib.models.transaction import Transaction
from lib.database import CURSOR

# --------------------------------------------------------------------
# Helper function: print simple tables (no external libraries needed)
# --------------------------------------------------------------------
def print_table(headers, rows):
    """Draws a clean text table using only string formatting."""
    if not rows:
        print("(No data found.)")
        return
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |")
    print(line)
    for r in rows:
        print("| " + " | ".join(str(r[i]).ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)

# --------------------------------------------------------------------
def main_menu():
    """Main interactive loop to handle user input and commands."""
    while True:
        print("\n=== EXPENSE TRACKER & BUDGET MONITOR ===")
        print("1. Add User")
        print("2. Add Category")
        print("3. Record Transaction")
        print("4. View Transactions")
        print("5. View All Users")
        print("6. View All Categories")
        print("7. Delete Category")
        print("8. Delete Transaction")
        print("9. Delete User")
        print("10. Exit")
        print("11. Category Summary Report")
        print("12. User Summary Report")
        print("13. Search or Filter Transactions")

        choice = input("\nSelect an option: ").strip()

        # ---------------- Add User ----------------
        if choice == "1":
            name = input("Enter user name: ").strip()
            if name:
                User(name).save()
                print(f"User '{name}' added successfully.")
            else:
                print("Name cannot be empty.")

        # ---------------- Add Category ----------------
        elif choice == "2":
            name = input("Enter category name: ").strip()
            if name:
                Category(name).save()
                print(f"Category '{name}' added successfully.")
            else:
                print("Category name cannot be empty.")

        # ---------------- Record Transaction ----------------
        elif choice == "3":
            print("\n-- Record a New Transaction --")

            users = User.get_all()
            if not users:
                print("No users found. Please add one first.")
                continue
            print_table(["User ID", "Name"], [[u.id, u.name] for u in users])

            categories = Category.get_all()
            if not categories:
                print("No categories found. Please add one first.")
                continue
            print_table(["Category ID", "Category"], [[c.id, c.name] for c in categories])

            try:
                user_id = int(input("\nEnter user ID: "))
                category_id = int(input("Enter category ID: "))
                amount = float(input("Enter actual amount spent: "))
                budgeted = float(input("Enter budgeted amount: "))
                date = input("Enter date (YYYY-MM-DD): ").strip()

                t = Transaction(user_id, category_id, amount, budgeted, date)
                t.save()
                print("\nTransaction recorded successfully.")
                if t.variance > 0:
                    print(f"Under budget by KES {t.variance:.2f}")
                elif t.variance < 0:
                    print(f"Overspent by KES {-t.variance:.2f}")
                else:
                    print("Spent exactly as budgeted.")
            except ValueError:
                print("Invalid input. Please enter numbers correctly.")

        # ---------------- View Transactions ----------------
        elif choice == "4":
            data = Transaction.get_all()
            if not data:
                print("No transactions yet.")
            else:
                rows = []
                for t in data:
                    status = "Under" if t[5] > 0 else ("Over" if t[5] < 0 else "Exact")
                    rows.append([
                        t[0], t[1], t[2],
                        f"KES {t[3]:,.2f}",
                        f"KES {t[4]:,.2f}",
                        f"KES {t[5]:,.2f}",
                        status, t[6]
                    ])
                print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Status", "Date"], rows)

        # ---------------- View Users ----------------
        elif choice == "5":
            users = User.get_all()
            print_table(["ID", "Name"], [[u.id, u.name] for u in users])

        # ---------------- View Categories ----------------
        elif choice == "6":
            cats = Category.get_all()
            print_table(["ID", "Category"], [[c.id, c.name] for c in cats])

        # ---------------- Delete Category ----------------
        elif choice == "7":
            cats = Category.get_all()
            print_table(["ID", "Category"], [[c.id, c.name] for c in cats])
            try:
                cid = int(input("Enter category ID to delete: "))
                if input("Are you sure? (y/n): ").lower() == "y":
                    if Category.delete(cid):
                        print("Category deleted.")
            except ValueError:
                print("Invalid ID.")

        # ---------------- Delete Transaction ----------------
        elif choice == "8":
            data = Transaction.get_all()
            print_table(["ID", "User", "Category", "Actual"], [[t[0], t[1], t[2], f"KES {t[3]:,.2f}"] for t in data])
            try:
                tid = int(input("Enter transaction ID to delete: "))
                if input("Are you sure? (y/n): ").lower() == "y":
                    Transaction.delete(tid)
                    print("Transaction deleted.")
            except ValueError:
                print("Invalid ID.")

        # ---------------- Delete User ----------------
        elif choice == "9":
            users = User.get_all()
            print_table(["ID", "Name"], [[u.id, u.name] for u in users])
            try:
                uid = int(input("Enter user ID to delete: "))
                if input("Are you sure? (y/n): ").lower() == "y":
                    if User.delete(uid):
                        print("User deleted.")
            except ValueError:
                print("Invalid ID.")

        # ---------------- Exit ----------------
        elif choice == "10":
            print("Goodbye! All data saved in 'database.db'.")
            break

        # ---------------- Category Summary Report ----------------
        elif choice == "11":
            q = '''
                SELECT c.name, SUM(t.amount), SUM(t.budgeted_amount), SUM(t.variance)
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                GROUP BY c.name
            '''
            rows = CURSOR.execute(q).fetchall()
            table = []
            for r in rows:
                status = "Under" if r[3] > 0 else ("Over" if r[3] < 0 else "Exact")
                table.append([r[0], f"KES {r[1]:,.2f}", f"KES {r[2]:,.2f}", f"KES {r[3]:,.2f}", status])
            print_table(["Category", "Total Actual", "Total Budget", "Variance", "Status"], table)

        # ---------------- User Summary Report ----------------
        elif choice == "12":
            q = '''
                SELECT u.name, SUM(t.amount), SUM(t.budgeted_amount), SUM(t.variance)
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                GROUP BY u.name
            '''
            rows = CURSOR.execute(q).fetchall()
            table = []
            for r in rows:
                status = "Under" if r[3] > 0 else ("Over" if r[3] < 0 else "Exact")
                table.append([r[0], f"KES {r[1]:,.2f}", f"KES {r[2]:,.2f}", f"KES {r[3]:,.2f}", status])
            print_table(["User", "Total Actual", "Total Budget", "Variance", "Status"], table)

        # ---------------- Search / Filter Feature ----------------
        elif choice == "13":
            print("\n--- SEARCH / FILTER TRANSACTIONS ---")
            print("1. Search by User")
            print("2. Search by Category")
            print("3. Search by Date Range")
            print("4. Search by Amount Range")
            print("5. Filter by Variance Status")
            print("6. Back to Main Menu")
            sub_choice = input("\nSelect an option: ").strip()

            # Search by User
            if sub_choice == "1":
                name = input("Enter user name (or part of it): ").lower()
                q = '''
                    SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
                    FROM transactions t
                    JOIN users u ON t.user_id = u.id
                    JOIN categories c ON t.category_id = c.id
                    WHERE LOWER(u.name) LIKE ?
                '''
                rows = CURSOR.execute(q, (f"%{name}%",)).fetchall()
                print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Date"],
                            [[r[0], r[1], r[2], f"KES {r[3]:,.2f}", f"KES {r[4]:,.2f}", f"KES {r[5]:,.2f}", r[6]] for r in rows])

            # Search by Category
            elif sub_choice == "2":
                category = input("Enter category name (or part of it): ").lower()
                q = '''
                    SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
                    FROM transactions t
                    JOIN users u ON t.user_id = u.id
                    JOIN categories c ON t.category_id = c.id
                    WHERE LOWER(c.name) LIKE ?
                '''
                rows = CURSOR.execute(q, (f"%{category}%",)).fetchall()
                print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Date"],
                            [[r[0], r[1], r[2], f"KES {r[3]:,.2f}", f"KES {r[4]:,.2f}", f"KES {r[5]:,.2f}", r[6]] for r in rows])

            # Filter by Date Range
            elif sub_choice == "3":
                start = input("Start date (YYYY-MM-DD): ").strip()
                end = input("End date (YYYY-MM-DD): ").strip()
                q = '''
                    SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
                    FROM transactions t
                    JOIN users u ON t.user_id = u.id
                    JOIN categories c ON t.category_id = c.id
                    WHERE date(t.date) BETWEEN date(?) AND date(?)
                '''
                rows = CURSOR.execute(q, (start, end)).fetchall()
                print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Date"],
                            [[r[0], r[1], r[2], f"KES {r[3]:,.2f}", f"KES {r[4]:,.2f}", f"KES {r[5]:,.2f}", r[6]] for r in rows])

            # Filter by Amount Range
            elif sub_choice == "4":
                try:
                    min_amt = float(input("Enter minimum amount: "))
                    max_amt = float(input("Enter maximum amount: "))
                    q = '''
                        SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
                        FROM transactions t
                        JOIN users u ON t.user_id = u.id
                        JOIN categories c ON t.category_id = c.id
                        WHERE t.amount BETWEEN ? AND ?
                    '''
                    rows = CURSOR.execute(q, (min_amt, max_amt)).fetchall()
                    print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Date"],
                                [[r[0], r[1], r[2], f"KES {r[3]:,.2f}", f"KES {r[4]:,.2f}", f"KES {r[5]:,.2f}", r[6]] for r in rows])
                except ValueError:
                    print("Invalid input. Please enter numbers correctly.")

            # Filter by Variance Status (Under / Over / Exact)
            elif sub_choice == "5":
                print("1. Under Budget")
                print("2. Over Budget")
                print("3. Exact Budget")
                status_choice = input("Select: ").strip()
                if status_choice == "1":
                    condition = "t.variance > 0"
                elif status_choice == "2":
                    condition = "t.variance < 0"
                elif status_choice == "3":
                    condition = "t.variance = 0"
                else:
                    print("Invalid selection.")
                    continue
                q = f'''
                    SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
                    FROM transactions t
                    JOIN users u ON t.user_id = u.id
                    JOIN categories c ON t.category_id = c.id
                    WHERE {condition}
                '''
                rows = CURSOR.execute(q).fetchall()
                print_table(["ID", "User", "Category", "Actual", "Budget", "Variance", "Date"],
                            [[r[0], r[1], r[2], f"KES {r[3]:,.2f}", f"KES {r[4]:,.2f}", f"KES {r[5]:,.2f}", r[6]] for r in rows])

            else:
                # Back or invalid -> return to main menu
                pass

        else:
            print("Invalid choice. Please enter a number between 1 and 13.")
