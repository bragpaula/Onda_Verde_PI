from flask import Flask, render_template, redirect, url_for, request, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'projetoI')  

# Rota para a página inicial (home)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para acessar a plataforma (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'Paula' and senha == 'Onda1234':
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha inválidos')
            return redirect(url_for('login'))
    return render_template('login.html')

# Rota para cadastro de pessoa física
@app.route('/cadastro_fisica', methods=['GET', 'POST'])
def cadastro_fisica():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        senha = request.form['senha']

        return redirect(url_for('login'))
    
    return render_template('cadastro_fisica.html')

# Rota para cadastro de pessoa jurídica (ONG, Empresa, etc)
@app.route('/cadastro_juridica', methods=['GET', 'POST'])
def cadastro_juridica():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cnpj = request.form['cnpj']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        senha = request.form['senha']

        return redirect(url_for('login'))
    
    return render_template('cadastro_juridica.html')

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