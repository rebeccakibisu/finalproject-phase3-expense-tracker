from lib.models.user import User
from lib.models.category import Category
from lib.models.transaction import Transaction

def main_menu():
    while True:
        print("\n=== Expense Tracker & Budget Monitor ===")
        print("1. Add User")
        print("2. Add Category")
        print("3. Record Transaction")
        print("4. View Transactions")
        print("5. View All Users")
        print("6. View All Categories")
        print("7. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add User
            name = input("Enter user name: ").strip()
            if name:
                user = User(name)
                user.save()
                print(f"User '{name}' added successfully.")
            else:
                print("Name cannot be empty.")

        elif choice == "2":
            # Add Category
            name = input("Enter category name: ").strip()
            if name:
                category = Category(name)
                category.save()
                print(f"Category '{name}' added successfully.")
            else:
                print("Category name cannot be empty.")

        elif choice == "3":
            # Record Transaction
            print("\n-- Record a New Transaction --")

            # Show available users
            users = User.get_all()
            if not users:
                print("No users found. Please add a user first.")
                continue
            print("\nAvailable Users:")
            for u in users:
                print(f"{u.id} - {u.name}")

            # Show available categories
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
                amount = float(input("Enter amount: "))
                date = input("Enter date (YYYY-MM-DD): ").strip()

                transaction = Transaction(user_id, category_id, amount, date)
                transaction.save()
                print("Transaction recorded successfully.")
            except ValueError:
                print("Invalid input. Please enter numeric IDs and a valid amount.")

        elif choice == "4":
            # View Transactions
            print("\n--- All Transactions ---")
            transactions = Transaction.get_all()

            if not transactions:
                print("No transactions found yet.")
            else:
                print("\nID | User | Category | Amount | Date")
                print("-" * 55)
                for t in transactions:
                    print(f"{t[0]} | {t[1]} | {t[2]} | KES {t[3]:.2f} | {t[4]}")

        elif choice == "5":
            # View all users
            users = User.get_all()
            if not users:
                print("No users found.")
            else:
                print("\n--- All Users ---")
                for u in users:
                    print(f"ID: {u.id} | Name: {u.name}")

        elif choice == "6":
            # View all categories
            categories = Category.get_all()
            if not categories:
                print("No categories found.")
            else:
                print("\n--- All Categories ---")
                for c in categories:
                    print(f"ID: {c.id} | Name: {c.name}")

        elif choice == "7":
            print("Goodbye! Your data has been saved.")
            break

        else:
            print("Invalid option. Please choose between 1 and 7.")
