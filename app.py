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
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_all():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

# Маршрут для удаления задачи
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

# Маршрут для редактирования задачи
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Проверка: существует ли задача
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    # Если GET запрос - показываем форму
    if request.method == 'GET':
        return render_template('edit.html', task=tasks[task_id])
    
    # Если POST запрос - сохраняем изменения
    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        
        # Проверка на пустое поле
        if new_text == '':
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="Текст не может быть пустым!")
        
        # Проверка: ничего не изменилось
        old_text = tasks[task_id]['text']
        if new_text == old_text:
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="Ничего не изменено")
        
        # Сохраняем изменения
        tasks[task_id]['text'] = new_text
        save_tasks(tasks)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)