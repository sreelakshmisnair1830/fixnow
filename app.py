from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"


# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# CREATE TABLES
# ----------------------------
def create_tables():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            location TEXT,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            work_type TEXT,
            experience INTEGER,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER,
            date TEXT,
            time TEXT,
            description TEXT,
            payment_method TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER,
            rating INTEGER,
            review TEXT,
            recommend INTEGER,
            task_completed INTEGER
        )
    """)

    conn.commit()
    conn.close()


create_tables()


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route('/')
def home():
    return render_template("home.html")


# ----------------------------
# USER REGISTER
# ----------------------------
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        location = request.form.get('location')
        password = request.form.get('password')

        if not name or not phone or not location or not password:
            return "All fields are required"

        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, phone, location, password) VALUES (?, ?, ?, ?)",
            (name, phone, location, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('user_login'))

    return render_template("user_register.html")


# ----------------------------
# USER LOGIN
# ----------------------------
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE phone = ? AND password = ?",
            (phone, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid phone or password"

    return render_template("user_login.html")


# ----------------------------
# USER LOGOUT
# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ----------------------------
# USER DASHBOARD
# ----------------------------
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    conn = get_db()
    workers = conn.execute("SELECT * FROM workers").fetchall()
    conn.close()

    return render_template("dashboard.html", workers=workers)


# ----------------------------
# WORKER REGISTER
# ----------------------------
@app.route('/worker_register', methods=['GET', 'POST'])
def worker_register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        work_type = request.form.get('work_type')
        experience = request.form.get('experience')
        password = request.form.get('password')

        if not name or not phone or not work_type or not experience or not password:
            return "All fields are required"

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, phone, work_type, experience, password) VALUES (?, ?, ?, ?, ?)",
            (name, phone, work_type, experience, password)
        )
        worker_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return redirect(url_for('worker_dashboard', worker_id=worker_id))

    return render_template("worker_register.html")


# ----------------------------
# WORKER DASHBOARD
# ----------------------------
@app.route('/worker_dashboard/<int:worker_id>')
def worker_dashboard(worker_id):

    conn = get_db()

    worker = conn.execute(
        "SELECT * FROM workers WHERE id = ?",
        (worker_id,)
    ).fetchone()

    rating_data = conn.execute(
        "SELECT AVG(rating) as avg_rating FROM feedback WHERE worker_id = ?",
        (worker_id,)
    ).fetchone()

    avg_rating = round(rating_data["avg_rating"], 1) if rating_data["avg_rating"] else 0

    total_feedback = conn.execute(
        "SELECT COUNT(*) as total FROM feedback WHERE worker_id = ?",
        (worker_id,)
    ).fetchone()["total"]

    completed_jobs = conn.execute(
        "SELECT COUNT(*) as total FROM feedback WHERE worker_id = ? AND task_completed = 1",
        (worker_id,)
    ).fetchone()["total"]

    score = int((completed_jobs / total_feedback) * 100) if total_feedback > 0 else 0

    conn.close()

    return render_template(
        "worker_dashboard.html",
        worker=worker,
        rating=avg_rating,
        score=score
    )


# ----------------------------
# BOOK WORKER
# ----------------------------
@app.route('/book/<int:worker_id>', methods=['GET', 'POST'])
def book_worker(worker_id):

    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    conn = get_db()

    worker = conn.execute(
        "SELECT * FROM workers WHERE id = ?",
        (worker_id,)
    ).fetchone()

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        description = request.form.get('description')
        payment = request.form.get('payment')

        if not date or not time or not description or not payment:
            return "All fields are required"

        conn.execute("""
            INSERT INTO bookings (worker_id, date, time, description, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, (worker_id, date, time, description, payment))

        conn.commit()
        conn.close()

        return redirect(url_for('payment_success', worker_id=worker_id))

    conn.close()
    return render_template("booking.html", worker=worker)


# ----------------------------
# PAYMENT SUCCESS
# ----------------------------
@app.route("/payment_success/<int:worker_id>")
def payment_success(worker_id):
    return redirect(url_for('feedback', worker_id=worker_id))


# ----------------------------
# FEEDBACK
# ----------------------------
@app.route("/feedback/<int:worker_id>", methods=["GET", "POST"])
def feedback(worker_id):

    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        recommend = 1 if request.form.get("recommend") else 0
        task_completed = 1 if request.form.get("task_completed") else 0

        if not rating:
            return "Please give rating"

        conn = get_db()
        conn.execute("""
            INSERT INTO feedback (worker_id, rating, review, recommend, task_completed)
            VALUES (?, ?, ?, ?, ?)
        """, (worker_id, rating, review, recommend, task_completed))
        conn.commit()
        conn.close()

        return "Thank you for your feedback!"

    return render_template("feedback.html", worker_id=worker_id)


# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
