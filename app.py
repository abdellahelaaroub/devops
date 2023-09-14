from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            created_date TEXT NOT NULL,
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    due_date = request.form['due_date']
    if task:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('tasks.db')
        conn.execute('INSERT INTO tasks (task, created_date, due_date) VALUES (?, ?, ?)', (task, current_time, due_date))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/tasks')
def tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = [{'id': row[0], 'task': row[1], 'created_date': row[2], 'due_date': row[3]} for row in cursor.fetchall()]
    conn.close()
    return render_template('tasks.html', tasks=tasks)



@app.route('/delete_task/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('tasks'))




if __name__ == '__main__':
    app.run(debug=True)
