import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")

    with open("schema.sql") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()
    print("DB created")

if __name__ == "__main__":
    init_db()