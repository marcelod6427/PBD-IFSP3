from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# função pra conectar no banco
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
        conn.execute(
            'INSERT INTO users (nome, email, senha, idioma) VALUES (?, ?, ?, ?)',
            (nome, email, senha, idioma)
        )
        conn.commit()
        conn.close()

        return f"Usuário {nome} cadastrado com sucesso!"

    return render_template('add.html')

@app.route('/news.html')
def news():
    return render_template('news.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404