"""Database utilities for the workforce modeling application."""

import sqlite3
from sqlite3 import Connection

DATABASE_NAME = 'workforce.db'


SCHEMA = [
    '''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT,
        location TEXT,
        contract_type TEXT,
        status TEXT,
        start_date TEXT,
        end_date TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date TEXT,
        end_date TEXT,
        funding_source TEXT,
        occupant_id INTEGER,
        FOREIGN KEY(occupant_id) REFERENCES people(id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS salary_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade TEXT NOT NULL,
        location TEXT NOT NULL,
        planning_rate REAL NOT NULL
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT,
        start_date TEXT,
        end_date TEXT,
        amount REAL NOT NULL
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS parameters (
        name TEXT PRIMARY KEY,
        value TEXT
    );
    '''
]


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def init_db(conn: Connection | None = None) -> None:
    """Create required tables if they do not exist."""
    close = False
    if conn is None:
        conn = get_connection()
        close = True

    cur = conn.cursor()
    for ddl in SCHEMA:
        cur.executescript(ddl)
    conn.commit()

    if close:
        conn.close()
