import sqlite3
from faker import Faker

def create_and_populate_db(db_path):
    """Create tables and populate them with fake data."""
    fake = Faker()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product TEXT,
        amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Insert fake data into users table
    for _ in range(100):  # Adjust the range for more or less data
        name = fake.name()
        age = fake.random_int(min=18, max=80)
        email = fake.email()
        cursor.execute('''
        INSERT INTO users (name, age, email) VALUES (?, ?, ?)
        ''', (name, age, email))

    # Insert fake data into orders table
    for _ in range(200):  # Adjust the range for more or less data
        user_id = fake.random_int(min=1, max=100)
        product = fake.word()
        amount = fake.random_number(digits=5, fix_len=True) / 100
        cursor.execute('''
        INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)
        ''', (user_id, product, amount))

    conn.commit()
    conn.close()

# Path to your SQLite DB file
db_path = 'your_database.db'
create_and_populate_db(db_path)