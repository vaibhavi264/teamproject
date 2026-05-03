import psycopg2

DATABASE_URL = "postgresql://postgres:password@containers-us-west-xx.railway.app:5432/railway"

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

print("USERS:")
cur.execute("SELECT * FROM users;")
print(cur.fetchall())

print("\nPROJECTS:")
cur.execute("SELECT * FROM projects;")
print(cur.fetchall())

print("\nTASKS:")
cur.execute("SELECT * FROM tasks;")
print(cur.fetchall())

conn.close()