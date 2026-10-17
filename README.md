# Canteen Menu Management System

A DBMS mini project. A simple web page to manage a canteen menu, backed by a MySQL database.

**Tech:** Python (Flask), MySQL, HTML/CSS

## Features
- View all menu items (JOIN of `menu_items` and `categories`)
- Add a new item with name, price and category
- Mark an item as sold out / available
- Delete an item

## Database design
| Table | Columns |
|-------|---------|
| `categories` | `category_id` (PK), `name` (UNIQUE) |
| `menu_items` | `item_id` (PK), `name`, `price` (CHECK > 0), `category_id` (FK -> categories), `available` |

One category has many menu items (1:N).

## How to run
1. Install Python 3 and MySQL (with MySQL Workbench).
2. Open `schema.sql` in MySQL Workbench and run it. This creates `canteen_db` with sample data.
3. Install the packages:
   ```
   pip install -r requirements.txt
   ```
4. Copy `config.example.py` to `config.py` and enter your MySQL password.
5. Start the app:
   ```
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## Project structure
```
canteen-menu-system/
├── app.py              # Flask app + HTML page
├── schema.sql          # Database tables and sample data
├── config.example.py   # Template for DB login (copy to config.py)
├── requirements.txt    # Python packages
├── .gitignore          # Keeps config.py out of GitHub
└── README.md
```

## Author
Your Name, Roll No., Class
