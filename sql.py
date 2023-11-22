import sqlite3

def create_login():
    try:
        with sqlite3.connect('config.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login (
                    token TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    hash TEXT NOT NULL
                )
            ''')
            conn.commit()
    except Exception as e:
        print(f"Table creation error: {e}")

def create_stock():
    try:
        with sqlite3.connect('config.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                    symbol TEXT PRIMARY KEY,
                    price REAL,
                    change REAL,
                    high REAL,
                    change_percentage REAL,
                    low REAL
            )
            ''')
            conn.commit()
    except Exception as e:
        print(f"Table creation error: {e}")
        
def create_transactions():
    try:
        with sqlite3.connect('config.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                    ref_number TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    lot INTEGER NOT NULL,
                    price REAL NOT NULL,
                    direction TEXT NOT NULL
                )
            ''')
            conn.commit()
    except Exception as e:
        print(f"Table creation error: {e}")

def control():
    create_login()
    create_stock()
    create_transactions()