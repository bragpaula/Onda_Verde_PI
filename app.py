from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = 'projetoI'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acessarplataforma')
def login():
    return render_template('acessarplataforma.html')

@app.route('/decidir_cadastro', methods=['GET', 'POST'])
def decidir_cadastro():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        if tipo == 'cidadao':
            return render_template('cadastro_cidadao.html')
        elif tipo == 'ong':
            return render_template('cadastro_ong.html')
        elif tipo == 'empresa':
            return render_template('cadastro_empresa.html')
    return render_template('decidir_cadastro.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/verificarlogin', methods=['POST'])
def acessoverific():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == 'Jepale' and senha == 'Onda1234':
        return redirect(url_for('perfil'))
    else:
        flash('Login ou senha inválidos')
    return redirect(url_for('login'))

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    return render_template('perfil.html')

@app.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')

@app.route('/adoteumamuda')
def adotar():
    return render_template('adoteumamuda.html')

@app.route('/feedbacks')
def feedbacks():
    return render_template('feedbacks.html')
