import sqlite3
from datetime import date


# Function to initialize the database and create tables if they don't exist
def init_tables():
    connect = sqlite3.connect('habit_history.db')
    cursor = connect.cursor()

    #Cteate tables if they do not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        date_created TEXT NOT NULL DEFAULT (DATE('now'))
                    )''')
    
    # Create records table
    cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        UNIQUE(habit_id, date),
                        FOREIGN KEY(habit_id) REFERENCES habits(id)
                    )''')
    
    # Commit changes and close the connection
    connect.commit()
    connect.close()

def connect_db():
    return sqlite3.connect('habit_history.db')

# Function to add a new habit
def add_habit(name):
    connect = connect_db()
    cursor = connect.cursor()
    
    # Insert the new habit into the habits table
    cursor.execute('INSERT INTO habits (name) VALUES (?)', (name,))

    connect.commit()
    connect.close()
    print(f"[+] Привычка добавлена: {name}")

# Function to mark a habit as done for a specific date
def mark_done(habit_id, date_mark: str = None):
    connect = connect_db()
    cursor = connect.cursor()
    # Insert a new record into the records table
    cursor.execute('INSERT INTO records (habit_id, date) VALUES (?, ?)', (habit_id, date_mark))

    connect.commit()
    connect.close()

# Function to get all habits
def get_habits():
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute('SELECT id, name FROM habits')
    habits = cursor.fetchall()

    connect.close()
    return habits

# Function to get all records
def get_records():
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute('''
                   SELECT records.id, habits.name, records.date 
                        FROM records 
                        JOIN habits ON records.habit_id = habits.id
                        ORDER BY records.date DESC
                    ''')
    records = cursor.fetchall()

    connect.close()
    return records

