import sqlite3
from datetime import datetime, timedelta, date
import calendar

def get_db_connection():
    conn = sqlite3.connect("workforce_model.db")
    conn.row_factory = sqlite3.Row
    return conn

def working_days_in_month(year, month, exclude_weekends=True):
    total_working_days = 0
    cal = calendar.Calendar()
    for day in cal.itermonthdates(year, month):
        if day.month == month:
            if exclude_weekends:
                if day.weekday() < 5:  # Monday-Friday
                    total_working_days += 1
            else:
                total_working_days += 1
    return total_working_days

def working_days_in_period(period_start, period_end):
    total = 0
    current = period_start
    while current <= period_end:
        if current.weekday() < 5:
            total += 1
        current += timedelta(days=1)
    return total

def calculate_prorated_cost(monthly_planning_rate, person_start, person_end, year, month):
    month_start = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    month_end = date(year, month, last_day)
    
    # Convert string dates to date objects.
    start_date = datetime.strptime(person_start, "%Y-%m-%d").date() if person_start else month_start
    end_date = datetime.strptime(person_end, "%Y-%m-%d").date() if person_end else month_end
    
    # Determine the effective occupancy within the month.
    effective_start = max(start_date, month_start)
    effective_end = min(end_date, month_end)
    
    if effective_start > effective_end:
        return 0.0

    working_days_month = working_days_in_month(year, month)
    working_days_active = working_days_in_period(effective_start, effective_end)
    return monthly_planning_rate * (working_days_active / working_days_month)

def get_planning_rate(grade, location, forecast_year, forecast_month):
    target_ym = f"{forecast_year}-{forecast_month:02d}"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT monthly_planning_rate
        FROM salaries
        WHERE grade = ? AND location = ? AND year_month = ?
        LIMIT 1
    ''', (grade, location, target_ym))
    row = c.fetchone()
    conn.close()
    if row:
        return row["monthly_planning_rate"]
    else:
        return 0.0

def get_global_churn_rate():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT param_value FROM parameters WHERE param_name = 'churn_rate' LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return row["param_value"]
    else:
        return 0.0

def calculate_person_cost(person, year, month):
    # Retrieve planning rate for the given month.
    planning_rate = get_planning_rate(person["grade"], person["location"], year, month)
    
    status = person["status"].lower() if person["status"] else ""
    # If the status indicates an external or unpaid assignment, return zero cost.
    if status in ["loan-out", "loan-out_unpaid"]:
        return 0.0
    
    last_day = calendar.monthrange(year, month)[1]
    # Use start_date and expected_end_date fields.
    start_date = person["start_date"] if person["start_date"] else f"{year}-{month:02d}-01"
    end_date = person["expected_end_date"] if person["expected_end_date"] else f"{year}-{month:02d}-{last_day:02d}"
    
    cost = calculate_prorated_cost(planning_rate, start_date, end_date, year, month)
    return cost

def run_forecast(year, month):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM people")
    people = c.fetchall()
    conn.close()
    
    total_cost = 0.0
    details = []
    churn_rate = get_global_churn_rate()
    
    for person in people:
        cost = calculate_person_cost(person, year, month)
        adjusted_cost = cost * (1 - churn_rate)
        total_cost += adjusted_cost
        details.append({
            "person_id": person["person_id"],
            "name": person["name"],
            "cost": adjusted_cost
        })
    
    return {
        "year": year,
        "month": month,
        "total_cost": total_cost,
        "details": details
    }

def get_budget(year, month):
    """
    Retrieves the overall allocated budget for the specified month by summing all records.
    """
    target_ym = f"{year}-{month:02d}"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT SUM(allocated_budget) as total_budget
        FROM budget
        WHERE year_month = ?
    ''', (target_ym,))
    row = c.fetchone()
    conn.close()
    if row and row["total_budget"]:
        return row["total_budget"]
    else:
        return 0.0
