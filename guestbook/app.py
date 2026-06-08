from flask import Flask, render_template
from database import init_db, get_all_messages

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    messages = get_all_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)