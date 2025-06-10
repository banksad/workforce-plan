from flask import Flask, request, render_template, redirect, url_for, send_file
from utils import get_db_connection, run_forecast, get_budget
from datetime import datetime
import io
import csv
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend.
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage_people", methods=["GET", "POST"])
def manage_people():
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        team = request.form["team"]
        grade = request.form["grade"]
        work_stream = request.form["work_stream"]
        location = request.form["location"]
        contract_type = request.form["contract_type"]
        status = request.form["status"]
        start_date = request.form["start_date"]
        expected_end_date = request.form["expected_end_date"]
        
        c.execute('''
            INSERT INTO people (name, team, grade, work_stream, location, contract_type, status, start_date, expected_end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, team, grade, work_stream, location, contract_type, status, start_date, expected_end_date))
        conn.commit()
        return redirect(url_for("manage_people"))
    else:
        c.execute("SELECT * FROM people")
        people = c.fetchall()
        conn.close()
        return render_template("manage_people.html", people=people)


@app.route("/edit_person/<int:person_id>", methods=["GET", "POST"])
def edit_person(person_id):
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        team = request.form["team"]
        grade = request.form["grade"]
        work_stream = request.form["work_stream"]
        location = request.form["location"]
        contract_type = request.form["contract_type"]
        status = request.form["status"]
        start_date = request.form["start_date"]
        expected_end_date = request.form["expected_end_date"]

        c.execute(
            """
            UPDATE people
            SET name=?, team=?, grade=?, work_stream=?, location=?,
                contract_type=?, status=?, start_date=?, expected_end_date=?
            WHERE person_id=?
            """,
            (
                name,
                team,
                grade,
                work_stream,
                location,
                contract_type,
                status,
                start_date,
                expected_end_date,
                person_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("manage_people"))
    else:
        c.execute("SELECT * FROM people WHERE person_id=?", (person_id,))
        person = c.fetchone()
        conn.close()
        return render_template("edit_person.html", person=person)


@app.route("/delete_person/<int:person_id>", methods=["POST"])
def delete_person(person_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM people WHERE person_id=?", (person_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("manage_people"))


@app.route("/download_people_template")
def download_people_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "name",
        "team",
        "grade",
        "work_stream",
        "location",
        "contract_type",
        "status",
        "start_date",
        "expected_end_date",
    ])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="people_template.csv",
    )


@app.route("/upload_people", methods=["POST"])
def upload_people():
    file = request.files.get("csv_file")
    if not file:
        return redirect(url_for("manage_people"))

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    conn = get_db_connection()
    c = conn.cursor()
    for row in reader:
        name = row.get("name")
        team = row.get("team")
        grade = row.get("grade")
        work_stream = row.get("work_stream")
        location = row.get("location")
        contract_type = row.get("contract_type")
        status = row.get("status")
        start_date = row.get("start_date")
        expected_end_date = row.get("expected_end_date")
        if name and grade and location:
            c.execute(
                """
                INSERT INTO people (name, team, grade, work_stream, location, contract_type, status, start_date, expected_end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    team,
                    grade,
                    work_stream,
                    location,
                    contract_type,
                    status,
                    start_date,
                    expected_end_date,
                ),
            )
    conn.commit()
    conn.close()
    return redirect(url_for("manage_people"))

@app.route("/manage_posts", methods=["GET", "POST"])
def manage_posts():
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        workforce_plan_number = request.form["workforce_plan_number"]
        funding_source = request.form["funding_source"]
        post_start_date = request.form["post_start_date"]
        post_end_date = request.form["post_end_date"]
        person_id = request.form["person_id"] if request.form["person_id"] else None
        
        c.execute('''
            INSERT INTO posts (workforce_plan_number, funding_source, post_start_date, post_end_date, person_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (workforce_plan_number, funding_source, post_start_date, post_end_date, person_id))
        conn.commit()
        return redirect(url_for("manage_posts"))
    else:
        c.execute("SELECT * FROM posts")
        posts = c.fetchall()
        conn.close()
        return render_template("manage_posts.html", posts=posts)


@app.route("/download_posts_template")
def download_posts_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "workforce_plan_number",
        "funding_source",
        "post_start_date",
        "post_end_date",
        "person_id",
    ])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="posts_template.csv",
    )


@app.route("/upload_posts", methods=["POST"])
def upload_posts():
    file = request.files.get("csv_file")
    if not file:
        return redirect(url_for("manage_posts"))

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    conn = get_db_connection()
    c = conn.cursor()
    for row in reader:
        workforce_plan_number = row.get("workforce_plan_number")
        funding_source = row.get("funding_source")
        post_start_date = row.get("post_start_date")
        post_end_date = row.get("post_end_date")
        person_id = row.get("person_id") or None
        if not any([workforce_plan_number, funding_source, post_start_date, post_end_date, person_id]):
            continue
        c.execute(
            """
            INSERT INTO posts (workforce_plan_number, funding_source, post_start_date, post_end_date, person_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                workforce_plan_number,
                funding_source,
                post_start_date,
                post_end_date,
                person_id,
            ),
        )
    conn.commit()
    conn.close()
    return redirect(url_for("manage_posts"))

@app.route("/manage_budget", methods=["GET", "POST"])
def manage_budget():
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        team = request.form["team"]
        work_stream = request.form["work_stream"]
        year_month = request.form["year_month"]
        allocated_budget = float(request.form["allocated_budget"])
        
        c.execute('''
            INSERT INTO budget (team, work_stream, year_month, allocated_budget)
            VALUES (?, ?, ?, ?)
        ''', (team, work_stream, year_month, allocated_budget))
        conn.commit()
        return redirect(url_for("manage_budget"))
    else:
        c.execute("SELECT * FROM budget")
        budgets = c.fetchall()
        conn.close()
        return render_template("manage_budget.html", budgets=budgets)


@app.route("/download_budget_template")
def download_budget_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["team", "work_stream", "year_month", "allocated_budget"])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="budget_template.csv",
    )


@app.route("/upload_budget", methods=["POST"])
def upload_budget():
    file = request.files.get("csv_file")
    if not file:
        return redirect(url_for("manage_budget"))

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    conn = get_db_connection()
    c = conn.cursor()
    for row in reader:
        team = row.get("team")
        work_stream = row.get("work_stream")
        year_month = row.get("year_month")
        allocated_budget = row.get("allocated_budget")
        if year_month and allocated_budget:
            try:
                budget_val = float(allocated_budget)
            except ValueError:
                continue
            c.execute(
                """
                INSERT INTO budget (team, work_stream, year_month, allocated_budget)
                VALUES (?, ?, ?, ?)
                """,
                (team, work_stream, year_month, budget_val),
            )
    conn.commit()
    conn.close()
    return redirect(url_for("manage_budget"))


@app.route("/manage_pay", methods=["GET", "POST"])
def manage_pay():
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        location = request.form["location"]
        grade = request.form["grade"]
        year_month = request.form["date"]
        pay = float(request.form["pay"])

        c.execute(
            """
            INSERT INTO salaries (grade, location, year_month, monthly_planning_rate)
            VALUES (?, ?, ?, ?)
            """,
            (grade, location, year_month, pay),
        )
        conn.commit()
        return redirect(url_for("manage_pay"))
    else:
        c.execute("SELECT * FROM salaries")
        salaries = c.fetchall()
        conn.close()
        return render_template("manage_pay.html", salaries=salaries)


@app.route("/download_pay_template")
def download_pay_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["location", "grade", "date", "pay"])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="pay_template.csv",
    )


@app.route("/upload_pay", methods=["POST"])
def upload_pay():
    file = request.files.get("csv_file")
    if not file:
        return redirect(url_for("manage_pay"))

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    conn = get_db_connection()
    c = conn.cursor()
    for row in reader:
        location = row.get("location")
        grade = row.get("grade")
        year_month = row.get("date")
        pay = row.get("pay")
        if location and grade and year_month and pay:
            try:
                pay_val = float(pay)
            except ValueError:
                continue
            c.execute(
                """
                INSERT INTO salaries (grade, location, year_month, monthly_planning_rate)
                VALUES (?, ?, ?, ?)
                """,
                (grade, location, year_month, pay_val),
            )
    conn.commit()
    conn.close()
    return redirect(url_for("manage_pay"))


@app.route("/edit_pay/<int:salary_id>", methods=["GET", "POST"])
def edit_pay(salary_id):
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == "POST":
        location = request.form["location"]
        grade = request.form["grade"]
        year_month = request.form["date"]
        pay = float(request.form["pay"])
        c.execute(
            """
            UPDATE salaries
            SET grade=?, location=?, year_month=?, monthly_planning_rate=?
            WHERE salary_id=?
            """,
            (grade, location, year_month, pay, salary_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("manage_pay"))
    else:
        c.execute("SELECT * FROM salaries WHERE salary_id=?", (salary_id,))
        record = c.fetchone()
        conn.close()
        return render_template("edit_pay.html", record=record)


@app.route("/delete_pay/<int:salary_id>", methods=["POST"])
def delete_pay(salary_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM salaries WHERE salary_id=?", (salary_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("manage_pay"))

@app.route("/run_forecast")
def run_forecast_route():
    # Use query parameters "year" and "month" if provided, otherwise default to current.
    year = int(request.args.get("year", datetime.now().year))
    month = int(request.args.get("month", datetime.now().month))
    
    forecast = run_forecast(year, month)
    budget_val = get_budget(year, month)
    return render_template("forecast.html", forecast=forecast, budget=budget_val)

@app.route("/export_csv")
def export_csv():
    """
    Exports the People table as a CSV file.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM people")
    people = c.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["person_id", "name", "team", "grade", "work_stream", "location",
                     "contract_type", "status", "start_date", "expected_end_date"])
    for row in people:
        writer.writerow([
            row["person_id"], row["name"], row["team"], row["grade"],
            row["work_stream"], row["location"], row["contract_type"],
            row["status"], row["start_date"], row["expected_end_date"]
        ])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="people.csv")

@app.route("/generate_chart")
def generate_chart():
    """
    Generates a PNG chart comparing monthly forecast cost with the allocated budget.
    """
    year = int(request.args.get("year", datetime.now().year))
    months = list(range(1, 13))
    costs = []
    budgets = []
    for month in months:
        forecast = run_forecast(year, month)
        costs.append(forecast["total_cost"])
        budgets.append(get_budget(year, month))
    
    plt.figure()
    plt.plot(months, costs, marker='o', label='Forecast Cost')
    if any(budgets):
        plt.plot(months, budgets, marker='x', label='Allocated Budget')
    plt.title(f"Monthly Workforce Cost Forecast for {year}")
    plt.xlabel("Month")
    plt.ylabel("Cost")
    plt.legend()
    plt.grid(True)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png', download_name="forecast_chart.png")

if __name__ == "__main__":
    app.run(debug=True)
