from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- DATABASE ----------------
DATABASE = "database.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- INIT DB ----------------
def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        created_by INTEGER
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT,
        assigned_to INTEGER,
        project_id INTEGER
    )
    """)

    # Insert admin only once
    user = db.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not user:
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "123", "admin")
        )

    db.commit()
    db.close()


# Run DB init when app starts
init_db()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        result = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        ).fetchone()

        if result:
            session["user_id"] = result["id"]
            return redirect("/dashboard")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (
                request.form["username"],
                request.form["password"],
                request.form["role"]
            )
        )
        db.commit()
        db.close()
        return redirect("/")

    return render_template("register.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    db.close()
    return render_template("dashboard.html", tasks=tasks)


# ---------------- CREATE PROJECT ----------------
@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO projects (name, created_by) VALUES (?, ?)",
            (request.form["name"], session["user_id"])
        )
        db.commit()
        db.close()
        return redirect("/dashboard")

    return render_template("create_project.html")


# ---------------- CREATE TASK ----------------
@app.route("/create_task", methods=["GET", "POST"])
def create_task():
    db = get_db()

    if request.method == "POST":
        db.execute(
            "INSERT INTO tasks (title, status, assigned_to, project_id) VALUES (?, ?, ?, ?)",
            (
                request.form["title"],
                "pending",
                request.form["assigned_to"],
                request.form["project_id"]
            )
        )
        db.commit()
        db.close()
        return redirect("/dashboard")

    users = db.execute("SELECT * FROM users").fetchall()
    projects = db.execute("SELECT * FROM projects").fetchall()
    db.close()

    return render_template("create_task.html", users=users, projects=projects)


# ---------------- UPDATE TASK ----------------
@app.route("/update/<int:id>")
def update(id):
    db = get_db()
    db.execute("UPDATE tasks SET status='done' WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/dashboard")


# ---------------- DEBUG ROUTE (VERY IMPORTANT) ----------------
@app.route("/debug")
def debug():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    projects = db.execute("SELECT * FROM projects").fetchall()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    db.close()

    return f"""
    USERS: {users}
    <br><br>
    PROJECTS: {projects}
    <br><br>
    TASKS: {tasks}
    """


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)