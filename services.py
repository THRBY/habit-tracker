from db import add_habit, mark_done, get_habits, get_records
import typer
from datetime import date, timedelta, datetime
import sqlite3

app = typer.Typer()

# Initialize the database and create tables if they don't exist

def connect_db():
    return sqlite3.connect('habit_history.db')

def add_habits_cmd(name):
    """Add a new habit."""
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute('SELECT id,name FROM habits WHERE name = ?', (name,))
    habit = cursor.fetchall()
    if habit:
        print(f"❌ Привычка с именем '{name}' уже существует.")
        connect.close()
        return
    
    add_habit(name)

def done_habit_cmd(habit_name: str, date_mark: str = None):
    """Mark a habit as done for today or a specific date (YYYY-MM-DD)."""
    if date_mark is None:
        date_mark = date.today().isoformat()

    connect = connect_db()
    cursor = connect.cursor()

    # Check if the habit exists
    cursor.execute('SELECT name FROM habits WHERE name = ?', (habit_name,))
    habit = cursor.fetchone()
    if not habit:
        print(f"❌ Привычка с {habit_name} не найдена.")
        connect.close()
        return
    
    

    # Check if the record for the given date already exists
    cursor.execute('SELECT id FROM habits WHERE name = ?', (habit_name,))
    habit_id = cursor.fetchone()[0]
    #habit_id = int(habit_id)
    
    cursor.execute('SELECT id FROM records WHERE habit_id = ? AND date = ?', (habit_id, date_mark))
    record = cursor.fetchone()
    if record:
        print(f"❌ Привычка {habit_name} уже выполнена {date_mark}.")
        connect.close()
        return
    
    mark_done(habit_id, date_mark)
    
    print(f"✅ Привычка {habit_name} выполнена {date_mark}")

def list_habits_cmd():
    """List all habists."""
    habist = get_habits()

    if not habist:
        print("❌ Нет добавленных привычек.")
        return
    print("Список привычек:\n")
    i = 0
    for habist in habist:
        i += 1
        print(f"{i}. {habist[1]} (ID: {habist[0]})")
    
def records_cmd():
    """List all records."""
    records = get_records()

    if not records:
        print("❌ Нет записей о выполненных привычках.")
        return
    
    print("Записи о выполненных привычках:\n")
    i = 0
    for record in records:
        i += 1
        print(f"{i}. {record[1]} выполнена {record[2]} (ID записи: {record[0]})")

def stats_cmd():
    stats = get_records()

    if not stats:
        print("❌ Нет записей о выполненных привычках.")
        return  
    habit_count = {}
    for stat in stats:
        habit_name = stat[1]
        if habit_name in habit_count:
            habit_count[habit_name] += 1
        else:
            habit_count[habit_name] = 1
    
    print("Статистика по выполненным привычкам:\n")
    for habit, count in habit_count.items():
        print(f"Привычка '{habit}' выполнена {count} раз(а).")

#delete habit
def delete_habit_name(habit_name: str):
    conn = connect_db()
    cursor = conn.cursor()

    # Find the habit by name
    cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
    ids = [r[0] for r in cursor.fetchall()]
    if not ids:
        print(f"❌ Привычка с именем '{habit_name}' не найдена.")
        conn.close()
        return
    
    print(f"❌ Привычка с id {ids} удалена.")
    try:
        conn.execute("BEGIN")
        # If have cascade delete, this is not necessary
        # cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))
        
        # IF have't cascade delete, this is not necessary
        cursor.execute("DELETE FROM records WHERE habit_id IN (SELECT id FROM habits WHERE name = ?)", (habit_name,))
        cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))
        conn.commit()
        print(f"✅ Записи о привычке '{habit_name}' удалены.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка при удалении привычки '{habit_name}': {e}")
    finally:
        conn.close()

