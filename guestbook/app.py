from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message, delete_message, get_message_count, check_user
from datetime import date

app = Flask(__name__)
app.secret_key = 'секретный_ключ_для_гостевой_книги_12345'

init_db()

@app.route('/')
def index():
    messages = get_all_messages()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template(
        'index.html',
        messages=messages,
        total_count=total_count,
        today=today,
        logged_in=session.get('logged_in', False),
        username=session.get('username')
    )

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if name and message:
        add_message(name, message)
    
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    delete_message(message_id)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if check_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            error = 'Неверный логин или пароль'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/sort/newest')
def sort_newest():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html', messages=messages, total_count=total_count, today=today, logged_in=session.get('logged_in', False), username=session.get('username'))

@app.route('/sort/oldest')
def sort_oldest():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at ASC').fetchall()
    conn.close()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html', messages=messages, total_count=total_count, today=today, logged_in=session.get('logged_in', False), username=session.get('username'))

@app.route('/delete-all')
def delete_all_page():
    total_count = get_message_count()
    return render_template('delete_all.html', total_count=total_count)

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    if not session.get('logged_in'):
        return redirect('/login')
    
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)