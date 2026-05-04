from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = 'tasks.json'

# Загрузка задач из файла
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение задач в файл
def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Загружаем задачи при запуске
tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form['task']
    if new_task:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tasks.append({'text': new_task, 'date': now})
        save_tasks(tasks)  # Сохраняем в файл
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_all():
    tasks.clear()
    save_tasks(tasks)  # Сохраняем в файл
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)