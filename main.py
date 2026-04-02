from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# conexão com o banco
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/add.html', methods=['GET', 'POST'])
def add():
    conn = get_db_connection()

    # 🔥 cria tabela automaticamente
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        idioma TEXT
    )
    ''')

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        idioma = request.form.get('idioma')

        conn.execute(
            'INSERT INTO users (nome, email, senha, idioma) VALUES (?, ?, ?, ?)',
            (nome, email, senha, idioma)
        )

        conn.commit()
        conn.close()

        return f"Usuário {nome} cadastrado com sucesso!"

    conn.close()
    return render_template('add.html')


@app.route('/news.html')
def news():
    return render_template('news.html')


# 🔍 rota pra ver os usuários cadastrados
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return str([dict(u) for u in users])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# rodar direto pelo python (opcional)
if __name__ == '__main__':
    app.run(debug=True)