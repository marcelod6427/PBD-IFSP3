from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/add.html', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        return "<h1>Cadastro recebido</h1>"
    else:
        return render_template('add.html')

@app.route('/news.html')
def news():
    return render_template('news.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
