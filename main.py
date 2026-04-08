from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
from werkzeug.security import generate_password_hash

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        idioma TEXT
    )
    ''')
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/add.html', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        idioma = request.form.get('idioma')

        conn = get_db_connection()

        user = conn.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if user:
            conn.close()
            return render_template('error.html')

        # criptografa senha
        senha_hash = generate_password_hash(senha)

        conn.execute(
            'INSERT INTO users (nome, email, senha, idioma) VALUES (?, ?, ?, ?)',
            (nome, email, senha_hash, idioma)
        )

        conn.commit()
        conn.close()

        return render_template('success.html', nome=nome)

    return render_template('add.html')


@app.route('/news.html')
def news():
    return render_template('news.html')

@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return str([dict(u) for u in users])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

@app.route("/list")
def lista():
    url = 'https://jsonplaceholder.typicode.com/todos'
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        data = response.json()
    return render_template('list.html', data=data)
