import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("USERS:")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

print("\nPROJECTS:")
for row in cursor.execute("SELECT * FROM projects"):
    print(row)

print("\nTASKS:")
for row in cursor.execute("SELECT * FROM tasks"):
    print(row)

conn.close()