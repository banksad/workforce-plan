# Workforce Plan

This project serves as a starting point for building a workforce modeling application.
Its goals are to store workforce data, forecast staffing costs, and compare them
to allocated budgets. The codebase uses a lightweight Python stack so it can be
run in restricted environments and gradually grow into a web service that offers
reporting tools for human resources teams.

The repository currently contains the following modules:

- `app.py` — Flask server providing pages to manage people, posts, budget data and pay rates.
- `database.py` — utilities for connecting to a SQLite database.
- `init_db.py` — script to create the required tables.
- `utils.py` — helper functions used for forecasting and budgeting.

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

The project uses Python's built-in `sqlite3` module, so the previous
`pysqlite3-binary` dependency has been removed. If you have an older
environment where SQLite is not compiled into Python, you can add a
`pysqlite3` package that matches your Python version, but it is usually
unnecessary.

2. Initialize the database:

```bash
python init_db.py
```

This creates the SQLite tables defined in `init_db.py`.

3. Run the application:

```bash
python app.py
```

4. Open `http://localhost:5000/` in your browser and use the navigation links to
manage records or run a forecast. The interface now includes a tab to manage
monthly pay rates where you can upload or edit rates in bulk. You can also export the people table to CSV
and generate a monthly cost chart from the interface.

Future development will add more functionality, including data ingestion,
forecasting algorithms, and a user interface.
