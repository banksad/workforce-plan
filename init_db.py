import sqlite3

def init_db():
    conn = sqlite3.connect("workforce_model.db")
    c = conn.cursor()

    # People table: includes team, work_stream, and expected_end_date.
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT,
            grade TEXT NOT NULL,
            work_stream TEXT,
            location TEXT NOT NULL,
            contract_type TEXT,
            status TEXT,
            start_date TEXT,           -- Format: YYYY-MM-DD
            expected_end_date TEXT     -- Format: YYYY-MM-DD
        )
    ''')
    
    # Posts table: updated field names.
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            workforce_plan_number TEXT,
            funding_source TEXT,
            post_start_date TEXT,      -- Format: YYYY-MM-DD
            post_end_date TEXT,        -- Format: YYYY-MM-DD
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    ''')
    
    # Salaries table: planning rates per grade/location for each month.
    c.execute('''
        CREATE TABLE IF NOT EXISTS salaries (
            salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade TEXT NOT NULL,
            location TEXT NOT NULL,
            year_month TEXT,            -- Format: "YYYY-MM"
            monthly_planning_rate REAL
        )
    ''')
    
    # Budget table (monthly budgets).
    c.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT,
            work_stream TEXT,
            year_month TEXT,            -- Format: "YYYY-MM"
            allocated_budget REAL
        )
    ''')

    # Parameters table: for global parameters (e.g. churn rate).
    c.execute('''
        CREATE TABLE IF NOT EXISTS parameters (
            parameter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            param_name TEXT,
            param_value REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
