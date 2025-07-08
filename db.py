import psycopg2

def get_user_credentials():
    conn = psycopg2.connect("postgresql://postgres:12345@localhost:5432/mailagent")
    cur = conn.cursor()
    cur.execute("SELECT email, password FROM user_emails")
    users = cur.fetchall()
    conn.close()
    return users
