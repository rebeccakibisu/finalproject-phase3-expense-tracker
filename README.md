
# Expense Tracker & Budget Monitor 

A simple Command-Line Interface (CLI) application that helps users record and monitor their expenses against a budget.  
It is built entirely using Python and SQLite3 — no external libraries are required.

---

## Project Overview

The Expense Tracker & Budget Monitor is a Python-based finance management tool designed to track actual expenses versus budgeted amounts and calculate the variance (difference).  
It demonstrates practical use of databases, SQL queries, Python classes, and command-line interfaces without using any ORM libraries.

This project is focusing on:
- Database design and SQL query writing
- Object-oriented programming in Python
- CRUD (Create, Read, Update, Delete) operations
- Real-world finance application logic

---

## Core Features

- Add Users – Create and manage user profiles.
- Add Categories – Define expense categories (e.g., Food, Rent, Utilities).
- Record Transactions – Log actual and budgeted expenses, including automatic variance calculation.
- View Transactions – Display all transactions in a clean table format.
- Variance Calculation – Automatically show whether spending was Under, Over, or Exactly on budget.
- Summary Reports:
  - By Category – View total actual, budget, and variance per category.
  - By User – Summarize spending and budget variance per user.
- Search & Filter:
  - Search by User, Category, Date Range, or Amount Range.
  - Filter by Variance Status (Under Budget, Over Budget, Exact).
- Safe Delete:
  - Prevent deletion of users or categories with existing transactions.
- Persistent Storage:
  - All data is saved locally in `database.db`.

---

## Technology Stack

| Component | Technology |
|------------|-------------|
| Language | Python 3 |
| Database | SQLite (using `sqlite3` module) |
| Interface | Command-Line Interface (CLI) |
| ORM | Custom-built ORM logic using Python classes |

---

## Project Structure

```

finalproject-phase3-expense-tracker/
│
├── lib/
│   ├── cli.py               # CLI interface and menu logic
│   ├── database.py          # Database connection and table creation
│   └── models/
│       ├── user.py          # User class (CRUD operations)
│       ├── category.py      # Category class (CRUD operations)
│       └── transaction.py   # Transaction class (CRUD operations + variance logic)
│
├── database.db              # SQLite database file (auto-created)
└── main.py                  # Entry point of the application

````

---

## Installation & Setup

1. Clone or download the project folder to your machine.  
2. Open a terminal inside the project directory.  
3. Run the app:
   ```bash
   python3 main.py



4. The program automatically creates a `database.db` file if it doesn’t exist.

---

## How to Use

### Main Menu Options

```
=== EXPENSE TRACKER & BUDGET MONITOR ===
1. Add User
2. Add Category
3. Record Transaction
4. View Transactions
5. View All Users
6. View All Categories
7. Delete Category
8. Delete Transaction
9. Delete User
10. Exit
11. Category Summary Report
12. User Summary Report
13. Search or Filter Transactions
```

### Example Flow

1. Add a user → “Rebecca”
2. Add a category → “Rent”
3. Record a transaction:

   * User ID: 1
   * Category ID: 1
   * Actual: 4500
   * Budget: 5000
   * Date: 2025-10-20

**Output:**

```
Transaction recorded successfully.
Under budget by KES 500.00
```

### View Transactions

```
+----+----------+------------+------------+------------+------------+----------+------------+
| ID | User     | Category   | Actual     | Budget     | Variance   | Status   | Date       |
+----+----------+------------+------------+------------+------------+----------+------------+
| 1  | Rebecca  | Rent       | KES 4,500  | KES 5,000  | KES 500.00 | Under    | 2025-10-20 |
+----+----------+------------+------------+------------+------------+----------+------------+
```



## Search & Filter Menu

Choose Option 13 from the main menu to search or filter transactions:

```
--- SEARCH / FILTER TRANSACTIONS ---
1. Search by User
2. Search by Category
3. Search by Date Range
4. Search by Amount Range
5. Filter by Variance Status
6. Back to Main Menu
```

Examples:

* Search by User → "Rebecca"
* Filter by Date → Between `2025-10-01` and `2025-10-31`
* Filter by Variance Status → “Under Budget”

---

## Summary Reports

### Category Summary

```
+----------+--------------+--------------+--------------+----------+
| Category | Total Actual | Total Budget | Variance     | Status   |
+----------+--------------+--------------+--------------+----------+
| Rent     | KES 4,500.00 | KES 5,000.00 | KES 500.00   | Under    |
+----------+--------------+--------------+--------------+----------+
```

### User Summary

```
+----------+--------------+--------------+--------------+----------+
| User     | Total Actual | Total Budget | Variance     | Status   |
+----------+--------------+--------------+--------------+----------+
| Rebecca  | KES 4,500.00 | KES 5,000.00 | KES 500.00   | Under    |
+----------+--------------+--------------+--------------+----------+
```

---

## Key Learning Outcomes

* Implementing CRUD using raw SQL queries
* Building a mini ORM from scratch
* Designing relational databases and linking Python classes to tables
* Managing data persistence with SQLite
* Structuring Python projects professionally
* Applying finance logic (budget vs actual variance)

---

## Data Storage

* All records are stored locally in `database.db`
* The database is automatically created if missing
* You can safely delete and rerun without errors

---

## Future Improvements

* CSV/Excel export for reports
* Color-coded table output
* Monthly and quarterly summaries
* Integration with a GUI or web interface

---

## Author

**Rebecca Vugutsa Kibisu (git-rebeccakibisu)**

---

## License

This project is open-source and free to use for learning and demonstration purposes.

---
