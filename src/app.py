"""Entry point for the workforce modeling application."""

from flask import Flask, jsonify, request

from database import get_connection, init_db

app = Flask(__name__)


@app.route('/')
def index():
    return "Workforce Modeling API"


@app.route('/init')
def init_route():
    """Initialize the SQLite database with required tables."""
    init_db()
    return jsonify({'status': 'initialized'})


@app.route('/people', methods=['GET', 'POST'])
def manage_people():
    """Create or list people records."""
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json(force=True)
        cur.execute(
            (
                "INSERT INTO people (name, grade, location, contract_type, status, start_date, end_date)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                data.get('name'),
                data.get('grade'),
                data.get('location'),
                data.get('contract_type'),
                data.get('status'),
                data.get('start_date'),
                data.get('end_date'),
            ),
        )
        conn.commit()
    cur.execute("SELECT * FROM people")
    rows = cur.fetchall()
    conn.close()
    return jsonify({'people': rows})


if __name__ == '__main__':
    app.run(debug=True)
