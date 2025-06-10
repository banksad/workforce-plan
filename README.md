# Workforce Plan

This project serves as a starting point for building a workforce modeling application.
Its goals are to store workforce data, forecast staffing costs, and compare them
to allocated budgets. The codebase uses a lightweight Python stack so it can be
run in restricted environments and gradually grow into a web service that offers
reporting tools for human resources teams.

The repository currently contains modules that will evolve into a full
application:

- `src/app.py` — entry point exposing a basic Flask server
- `src/database.py` — utilities for connecting to a SQLite database

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python src/app.py
```

3. Initialize the database by visiting `http://localhost:5000/init` in your
browser. You can then add people records with a POST request to `/people` using
JSON payloads.

Future development will add more functionality, including data ingestion,
forecasting algorithms, and a user interface.
