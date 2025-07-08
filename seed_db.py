import psycopg2

# Database connection info
conn = psycopg2.connect("postgresql://postgres:12345@localhost:5432/mailagent")
cur = conn.cursor()

# Step 1: Create the table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS user_emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

# Step 2: Insert the provided email/password pairs
users = [
    ('baskaran.arumugam@winvinaya.com', 'Admin##2025'),
    ('aravindan.ganesa@winvinaya.com', 'Admin##2025'),
    ('akila.sankar@winvinaya.com', 'Admin##2025@'),
    ('shiva.jayagopal@winvinaya.com', 'Admin##2025'),
    ('akila.sankar@winvinayafoundation.org', 'Admin##2024'),
    ('ann.jannet@winvinayafoundation.org', 'Admin##2024'),
    ('aravindan.ganesa@winvinayafoundation.org', 'Admin##2024'),
    ('baskaran.arumugam@winvinayafoundation.org', 'Admin##2024'),
    ('menaga.veeramani@winvinayafoundation.org', 'Admin##2024'),
    ('rathna.pm@winvinayafoundation.org', 'Admin##2024'),
    ('nagaratna.m@winvinayafoundation.org', 'Admin##2024'),
    ('shiva.jayagopal@winvinayafoundation.org', 'Admin##2024'),
    ('marimuthu.t@winvinayafoundation.org', 'Admin##2024'),
    ('yogasri.a@winvinayafoundation.org', 'Admin##2024'),
    ('danetta.jose@winvinayafoundation.org', 'Admin##2024'),
    ('ruchita.p@winvinayafoundation.org', 'Admin##2024'),
    ('as.ranya@winvinayafoundation.org', 'Admin##2024')
]

for email, password in users:
    try:
        cur.execute("""
            INSERT INTO user_emails (email, password)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, (email, password))
    except Exception as e:
        print(f"❌ Error inserting {email}: {e}")

# Commit and close
conn.commit()
cur.close()
conn.close()

print("✅ Database setup complete with all users.")
