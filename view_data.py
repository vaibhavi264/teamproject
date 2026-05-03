import psycopg2
import os

DATABASE_URL = os.getenv("postgresql://postgres:password@containers-us-west-xx.railway.app:6543/railway")

# If running locally, paste your Railway DATABASE_URL manually:
# DATABASE_URL = "postgresql://user:password@host:port/dbname"

conn = psycopg2.connect(postgresql://postgres:password@containers-us-west-xx.railway.app:6543/railway)
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