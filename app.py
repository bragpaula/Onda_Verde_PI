from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ondaverde_chave'

def conectar_bd():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row  # otimização - buscando por nome de coluna
    return conn

def criar_tabela_pessoa():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoa (
        cpf INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        data_nasc DATE NOT NULL,
        telefone TEXT NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'pessoa'
    )
    ''')
    conn.commit()
    conn.close()

criar_tabela_pessoa()

def criar_tabela_org():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS org (
        cnpj INTEGER PRIMARY KEY,
        nomef TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        area_atuacao TEXT NOT NULL,
        telefone TEXT NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'org'
    )
    ''')
    conn.commit()
    conn.close()

criar_tabela_org()


@app.route('/')
def index():
    return render_template('index.html')

# Rota para acessar a plataforma (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = conectar_bd()
        cursor = conn.cursor()

        # Verificação de pessoa física
        cursor.execute('SELECT * FROM pessoa WHERE email = ?', (email,))
        pessoa = cursor.fetchone()

        if pessoa and check_password_hash(pessoa['senha'], senha):
            session['usuario'] = pessoa['nome']
            session['tipo'] = 'pessoa'
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        # Procurando na tabela org
        cursor.execute('SELECT * FROM org WHERE email = ?', (email,))
        org = cursor.fetchone()

        conn.close()

        if org and check_password_hash(org['senha'], senha):
            session['usuario'] = org['nomef']
            session['tipo'] = 'org' 
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        # Se não encontrou em nenhuma das tabelas
        flash('Erro no login! Verifique suas credenciais.', 'danger')
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
        senha = generate_password_hash(request.form['senha'])

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pessoa (cpf, nome, email, data_nasc, telefone, senha, tipo)
            VALUES (?, ?, ?, ?, ?, ?, 'pessoa')
        ''', (cpf, nome, email, data_nascimento, telefone, senha))
        conn.commit()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro_fisica.html')

# Rota para cadastro de pessoa jurídica (ONG, Empresa, etc)
@app.route('/cadastro_juridica', methods=['GET', 'POST'])
def cadastro_juridica():
    if request.method == 'POST':
        nomef = request.form['nome']
        email = request.form['email']
        cnpj = request.form['cnpj']
        area_atuacao = request.form['area_atuacao']
        telefone = request.form['telefone']
        senha = generate_password_hash(request.form['senha'])

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO org (cnpj, nomef, email, area_atuacao, telefone, senha, tipo)
            VALUES (?, ?, ?, ?, ?, ?, 'org')
        ''', (cnpj, nomef, email, area_atuacao, telefone, senha))
        conn.commit()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro_juridica.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar o dashboard.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

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

# Rota para logout do usuário
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
