import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',  # Replace with your actual database name
        user='odoo',
        password='odoo',
        host='localhost',
        port='5432'
    )
    print("Connection successful")
    conn.close()
except Exception as e:
    print("Connection failed")
    print(e)
