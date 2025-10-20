# lib/cli.py
# Provides the Command-Line Interface for the Expense Tracker & Budget Monitor.
# Allows users to add, view, and delete users, categories, and transactions.

from lib.models.user import User
from lib.models.category import Category
from lib.models.transaction import Transaction

def main_menu():
    """Main CLI Menu Loop."""
    while True:
        print("\n=== Expense Tracker & Budget Monitor ===")
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

        choice = input("Select an option: ").strip()

        # ADD USER
        if choice == "1":
            name = input("Enter user name: ").strip()
            if name:
                user = User(name)
                user.save()
                print(f"User '{name}' added successfully.")
            else:
                print("Name cannot be empty.")

        # ADD CATEGORY
        elif choice == "2":
            name = input("Enter category name: ").strip()
            if name:
                category = Category(name)
                category.save()
                print(f"Category '{name}' added successfully.")
            else:
                print("Category name cannot be empty.")

        # RECORD TRANSACTION
        elif choice == "3":
            print("\n-- Record a New Transaction --")

            # Display available users
            users = User.get_all()
            if not users:
                print("No users found. Please add a user first.")
                continue
            print("\nAvailable Users:")
            for u in users:
                print(f"{u.id} - {u.name}")

            # Display available categories
            categories = Category.get_all()
            if not categories:
                print("No categories found. Please add a category first.")
                continue
            print("\nAvailable Categories:")
            for c in categories:
                print(f"{c.id} - {c.name}")

            try:
                user_id = int(input("\nEnter user ID: "))
                category_id = int(input("Enter category ID: "))
                amount = float(input("Enter actual amount spent: "))
                budgeted_amount = float(input("Enter budgeted amount: "))
                date = input("Enter date (YYYY-MM-DD): ").strip()

                transaction = Transaction(user_id, category_id, amount, budgeted_amount, date)
                transaction.save()

                print("\nTransaction recorded successfully.")
                if transaction.variance > 0:
                    print(f"Under budget by KES {transaction.variance:.2f}")
                elif transaction.variance < 0:
                    print(f"Overspent by KES {-transaction.variance:.2f}")
                else:
                    print("Spent exactly as budgeted.")
            except ValueError:
                print("Invalid input. Please enter numeric IDs and valid amounts.")

        # VIEW TRANSACTIONS
        elif choice == "4":
            print("\n--- All Transactions ---")
            transactions = Transaction.get_all()
            if not transactions:
                print("No transactions found yet.")
            else:
                print("\nID | User | Category | Actual | Budget | Variance | Date")
                print("-" * 90)
                for t in transactions:
                    variance_status = "Under" if t[5] > 0 else ("Over" if t[5] < 0 else "Exact")
                    print(f"{t[0]} | {t[1]} | {t[2]} | {t[3]:.2f} | {t[4]:.2f} | {t[5]:.2f} ({variance_status}) | {t[6]}")

        # VIEW USERS
        elif choice == "5":
            users = User.get_all()
            if not users:
                print("No users found.")
            else:
                print("\n--- All Users ---")
                for u in users:
                    print(f"ID: {u.id} | Name: {u.name}")

        # VIEW CATEGORIES
        elif choice == "6":
            categories = Category.get_all()
            if not categories:
                print("No categories found.")
            else:
                print("\n--- All Categories ---")
                for c in categories:
                    print(f"ID: {c.id} | Name: {c.name}")

        # DELETE CATEGORY
        elif choice == "7":
            categories = Category.get_all()
            if not categories:
                print("No categories found.")
            else:
                print("\n--- All Categories ---")
                for c in categories:
                    print(f"ID: {c.id} | Name: {c.name}")
                try:
                    category_id = int(input("Enter category ID to delete: "))
                    confirm = input("Are you sure? (y/n): ").strip().lower()
                    if confirm == "y":
                        deleted = Category.delete(category_id)
                        if deleted:
                            print("Category deleted successfully.")
                    else:
                        print("Delete cancelled.")
                except ValueError:
                    print("Invalid ID entered.")

        # DELETE TRANSACTION
        elif choice == "8":
            transactions = Transaction.get_all()
            if not transactions:
                print("No transactions found.")
            else:
                print("\n--- All Transactions ---")
                for t in transactions:
                    print(f"ID: {t[0]} | {t[1]} | {t[2]} | {t[3]:.2f}")
                try:
                    transaction_id = int(input("Enter transaction ID to delete: "))
                    confirm = input("Are you sure? (y/n): ").strip().lower()
                    if confirm == "y":
                        Transaction.delete(transaction_id)
                        print("Transaction deleted successfully.")
                    else:
                        print("Delete cancelled.")
                except ValueError:
                    print("Invalid ID entered.")

        # DELETE USER
        elif choice == "9":
            users = User.get_all()
            if not users:
                print("No users found.")
            else:
                print("\n--- All Users ---")
                for u in users:
                    print(f"ID: {u.id} | Name: {u.name}")
                try:
                    user_id = int(input("Enter user ID to delete: "))
                    confirm = input("Are you sure? (y/n): ").strip().lower()
                    if confirm == "y":
                        deleted = User.delete(user_id)
                        if deleted:
                            print("User deleted successfully.")
                    else:
                        print("Delete cancelled.")
                except ValueError:
                    print("Invalid ID entered.")

        # EXIT PROGRAM
        elif choice == "10":
            print("Goodbye! All data saved in 'database.db'.")
            break

        # INVALID OPTION
        else:
            print("Invalid option. Please choose between 1 and 10.")
