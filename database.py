import sqlite3
def init_db():
    conn = sqlite3.connect('muthu_mobiles.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, category TEXT, amount REAL, notes TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, customer_name TEXT, amount REAL, due_date TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()
    print('Database Created!')
if __name__ == '__main__':
    init_db()
