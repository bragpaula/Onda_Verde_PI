from flask import Flask, render_template, redirect, url_for, request, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'projetoI')  

# Rota para a página inicial (home)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para acessar a plataforma (login)
@app.route('/acessarplataforma', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'Paula' and senha == 'Onda1234':
            return redirect(url_for('perfil'))
        else:
            flash('Login ou senha inválidos')
            return redirect(url_for('login'))
    return render_template('acessarplataforma.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota para decidir o tipo de cadastro
@app.route('/decidir_cadastro', methods=['GET', 'POST'])
def decidir_cadastro():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        if tipo == 'cidadao':
            return redirect(url_for('cadastro_cidadao'))
        elif tipo == 'ong':
            return redirect(url_for('cadastro_ong'))
        elif tipo == 'empresa':
            return redirect(url_for('cadastro_empresa'))
    return render_template('decidir_cadastro.html')

# Rota para cadastro de cidadão
@app.route('/cadastro_cidadao', methods=['GET', 'POST'])
def cadastro_cidadao():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        telefone = request.form['telefone']
        endereco = request.form['endereco']

        return redirect(url_for('login'))
    return render_template('cadastro_cidadao.html')

# Rota para cadastro de ONG
@app.route('/cadastro_ong', methods=['GET', 'POST'])
def cadastro_ong():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        telefone = request.form['telefone']
        endereco = request.form['endereco']

        return redirect(url_for('login'))
    return render_template('cadastro_ong.html')

# Rota para cadastro de empresa
@app.route('/cadastro_empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        telefone = request.form['telefone']
        bairro= request.form['bairro']

        return redirect(url_for('login'))
    return render_template('cadastro_empresa.html')

# Rota para o perfil do usuário
@app.route('/perfil')
def perfil():

    user = {
        'username': 'Paula',
        'email': 'paula@example.com',
        'telefone': '123456789'
    }
    return render_template('perfil.html', user=user)

# Rota sobre o projeto
@app.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')

# Rota para a página de feedbacks
@app.route('/feedbacks')
def feedbacks():
    return render_template('feedbacks.html')

# Rota para a página de adotar uma muda
@app.route('/adoteumamuda')
def adotar():
    return render_template('adoteumamuda.html')  


# Rota para o formulário de login (verificação)
@app.route('/verificarlogin', methods=['POST'])
def verificarlogin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == 'Paula' and senha == 'Onda1234':
        return redirect(url_for('perfil'))
    else:
        flash('Login ou senha inválidos')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
