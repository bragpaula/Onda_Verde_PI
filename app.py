from flask import Flask, render_template,redirect, url_for, request,flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verificarlogin', methods=['POST'])
def acessoverific():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == 'Jepale' and senha == 'flores3m':
        return redirect(url_for('perfil'))
    else: 
        flash('Login ou senha inválidos')
    return redirect(url_for('login'))


@app.route('/perfil', methods=['GET','POST'])
def index2():
    return render_template('perfil.html')