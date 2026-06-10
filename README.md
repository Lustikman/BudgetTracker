# BudgetTracker 

A command-line budget tracker built with Python and SQLite. Add expenses, organize them into categories, and track where your money is going — all from the terminal.

---

## Features

- Add and manage expenses with names, amounts, and categories
- Add and manage categories independently
- Auto-creates a category if it doesn't exist when adding an expense
- List all expenses or filter by category
- Get a total summary of all expenses or by specific category
- Delete expenses by ID or delete a whole category (removes its expenses too)

---

## Tech Stack

- **Python** — core language
- **SQLite** — local database storage via the `sqlite3` module
- **argparse** — CLI commands and argument parsing

---

## Project Structure

```
BudgetTracker/
│
├── BudgetTracker.py        ← entry point, CLI commands
├── Database.py             ← all database logic and queries
├── Modules.py              ← helper functions (formatting, etc.)
└── BudgetTrackerDatabase.db  ← created automatically on first run
```

---

## Getting Started

**Clone the repo**
```bash
git clone https://github.com/Lustikman/BudgetTracker.git
cd BudgetTracker
```

**Run it**
```bash
python BudgetTracker.py
```

No external dependencies — uses Python's standard library only.

---

## Usage

### Add

```bash
# Add a new expense
python BudgetTracker.py add expense "Coffee" 4.50 food

# Add a category manually
python BudgetTracker.py add category transport
```

> If the category doesn't exist when adding an expense, it gets created automatically.

---

### List

```bash
# List all expenses
python BudgetTracker.py list expenses

# List all categories
python BudgetTracker.py list category

# List all expenses inside a specific category
python BudgetTracker.py list category food
```

---

### Summary

```bash
# Total of all expenses
python BudgetTracker.py sum

# Total for a specific category
python BudgetTracker.py sum food
```

---

### Delete

```bash
# Delete an expense by its ID
python BudgetTracker.py delete expense 3

# Delete a category by name (also deletes all its expenses)
python BudgetTracker.py delete category food
```

---

## Database Design

Two tables with a foreign key relationship:

**Categories**
| Column | Type    |
|--------|---------|
| id     | INTEGER |
| name   | TEXT    |

**Expenses**
| Column     | Type    |
|------------|---------|
| id         | INTEGER |
| name       | TEXT    |
| amount     | REAL    |
| categoryId | INTEGER → FK to Categories.id |

---

## What I Learned Building This

- Structuring a Python project across multiple files
- Using `argparse` for nested CLI subcommands
- SQLite with the `sqlite3` module — CREATE, INSERT, SELECT, DELETE, JOIN
- Relational database design with foreign keys
- Handling edge cases and missing data gracefully
