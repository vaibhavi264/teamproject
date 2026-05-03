from flask import Flask, render_template, request, redirect, session
import sqlite3
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def get_db():
    return sqlite3.connect(config.DATABASE)

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
            session["user_id"] = result[0]
            return redirect("/dashboard")

    return render_template("login.html")

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
        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    return render_template("dashboard.html", tasks=tasks)

@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO projects (name, created_by) VALUES (?, ?)",
            (request.form["name"], session["user_id"])
        )
        db.commit()
        return redirect("/dashboard")

    return render_template("create_project.html")

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
        return redirect("/dashboard")

    users = db.execute("SELECT * FROM users").fetchall()
    projects = db.execute("SELECT * FROM projects").fetchall()

    return render_template("create_task.html", users=users, projects=projects)

@app.route("/update/<int:id>")
def update(id):
    db = get_db()
    db.execute("UPDATE tasks SET status='done' WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)