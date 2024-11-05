from flask import Flask, render_template,redirect, url_for, request,flash

app = Flask(__name__)
app.secret_key = 'prejetoI'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/acessarplataforma')
def login():
    return render_template('acessarplataforma.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/decisao_cadastro')
def decisao_cadastro():
     if request.method == 'POST':
        tipo = request.form.get('tipo')
        if tipo == 'Cidadao':
            return render_template('cadastro-cidadao.html')
        elif tipo =='ong':
            return render_template('cadastro-ong.html') 
        elif tipo == 'Empresa':
            return render_template('cadastro-empresa.html') 
     return render_template('decisao-cadastro.html')


@app.route('/verificarlogin', methods=['POST'])
def verificarlogin():
    return render_template('verificarlogin.html')

@app.route('/perfil', methods=['GET','POST'])
def perfil():
    return render_template('perfil.html')

@app.route('/sobrenos')
def doacoes():
    return render_template('sobrenos.html')

@app.route('/adoteumamuda')
def adote():
    return render_template('adoteumamuda.html')

@app.route('/feedbacks')
def feedbacks():
    return render_template('feedbacks.html')
