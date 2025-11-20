import typer
from typing import Optional
from services import add_habits_cmd, done_habit_cmd, list_habits_cmd, records_cmd, stats_cmd, delete_habit_name
from db import init_tables

init_tables()

app = typer.Typer()

@app.command()
def add(name: str):
    """Add a new habit."""
    add_habits_cmd(name)
    
@app.command()
def done(habit_name: str, date_mark: Optional[str] = typer.Argument(None)):
    done_habit_cmd(habit_name, date_mark)    

@app.command()
def habits():
    list_habits_cmd()

@app.command()
def records():
    records_cmd()

@app.command()
def stats():
    stats_cmd()

@app.command()
def delete(habit_name: str):
    delete_habit_name(habit_name)

if __name__ == "__main__":
    app()