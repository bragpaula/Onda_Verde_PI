from flask import Flask, render_template, redirect, url_for, request, flash, session
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'projeto.I'


# Rota para a página inicial (home)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para acessar a plataforma (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email == 'paula@example.com' and senha == 'Onda1234':
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
@app.route('/dashboard')
def dashboard():
    user = {
        'username': 'Paula',
        'email': 'paula@example.com',
        'telefone': '123456789'
    }
    return render_template('dashboard.html', user=user)

# Rota para detalhes de uma área
@app.route('/detalhes/<int:id_area>')
def detalhes_area(id_area):
    return render_template('detalhes.html', id_area=id_area)

# Rota para adotar uma área
@app.route('/adotar/<int:id_area>')
def adotar_area(id_area):
    flash(f'Você adotou a área {id_area} com sucesso!')
    return redirect(url_for('dashboard'))  

# Rota para participar de uma atividade
@app.route('/participar/<int:id_atividade>')
def participar_atividade(id_atividade):
    return redirect(url_for('dashboard'))  

# Rota para visualizar uma área adotada
@app.route('/visualizar/<int:id_area>')
def visualizar_area(id_area):
    return render_template('visualizar.html', id_area=id_area)

# Rota para buscar áreas e atividades
@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    resultados = ["Praça Dom Casmurro", "Canteiro Central", "Bosque Esperança"]
    return render_template('resultados.html', query=query, resultados=resultados)

# Rota para exibir notificações
@app.route('/notificacoes')
def notificacoes():
    notificacoes = [
        "Nova área disponível para adoção!",
        "Evento de plantio amanhã as 15h no IFRN-zona Norte.",
        "Você foi aceito em uma nova atividade!"
    ]

    return render_template('notificacoes.html', notificacoes=notificacoes)

# Rota para logout do usuário
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))  

# Rota sobre o projeto
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para a página de feedbacks
@app.route('/feedbacks')
def feedbacks():
    return render_template('feedbacks.html')

# Rota para a página de adotar uma muda
@app.route('/adocao')
def adotar():
    return render_template('adocao.html')  

# Rota para o formulário de login (verificação)
@app.route('/verificarlogin', methods=['POST'])
def verificarlogin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == 'Paula' and senha == 'Onda1234':
        return redirect(url_for('dashboard')) 
    else:
        flash('Login ou senha inválidos')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
