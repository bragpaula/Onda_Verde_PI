from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import models  # Importando o arquivo models.py

app = Flask(__name__)
app.secret_key = 'ondaverde_chave'

models.criar_tabela_pessoa()
models.criar_tabela_org()
models.criar_tabela_atividades()
models.criar_tabela_areas()
models.criar_tabela_usuario_areas()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('usuarios.db')
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM pessoa WHERE email = ?', (email,))
        pessoa = cursor.fetchone()

        if pessoa and check_password_hash(pessoa['senha'], senha): 
            session['usuario'] = pessoa['nome']
            session['tipo'] = 'pessoa'
            flash('Login realizado com sucesso!', 'success')
            conn.close()
            return redirect(url_for('dashboard'))

        cursor.execute('SELECT * FROM org WHERE email = ?', (email,))
        org = cursor.fetchone()

        conn.close()

        if org and check_password_hash(org['senha'], senha):
            session['usuario'] = org['nomef']
            session['tipo'] = 'org' 
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        flash('Erro no login! Verifique suas credenciais.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastro_fisica', methods=['GET', 'POST'])
def cadastro_fisica():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        senha = generate_password_hash(request.form['senha'])

        try:
            models.cadastrar_pessoa(nome, email, cpf, data_nascimento, telefone, senha)
            flash('Cadastro realizado com sucesso!', 'success')
        except ValueError as e:
            flash(str(e), 'danger')

        return redirect(url_for('login'))

    return render_template('cadastro_fisica.html')

@app.route('/cadastro_juridica', methods=['GET', 'POST'])
def cadastro_juridica():
    if request.method == 'POST':
        nomef = request.form['nome']
        email = request.form['email']
        cnpj = request.form['cnpj']
        area_atuacao = request.form['area_atuacao']
        telefone = request.form['telefone']
        senha = generate_password_hash(request.form['senha'])

        try:
            models.cadastrar_org(nomef, email, cnpj, area_atuacao, telefone, senha)
            flash('Cadastro realizado com sucesso!', 'success')
        except ValueError as e:
            flash(str(e), 'danger')

        return redirect(url_for('login'))

    return render_template('cadastro_juridica.html')


@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar o dashboard.', 'danger')
        return redirect(url_for('login'))
    
    tipo_usuario = session.get('tipo')
    usuario_nome = session.get('usuario')


    if tipo_usuario == 'pessoa':
        return render_template('dashboard.html', tipo_usuario=tipo_usuario, usuario_nome=usuario_nome)
    
    elif tipo_usuario == 'org':
        return render_template('dashboard.html', tipo_usuario=tipo_usuario, usuario_nome=usuario_nome)

    return redirect(url_for('login'))


# Rota para detalhes de uma área
@app.route('/detalhes/<int:id_area>')
def detalhes_area(id_area):
    return render_template('detalhes.html', id_area=id_area)

# Rota para adotar uma área
@app.route('/adotar/<int:id_area>')
def adotar_area(id_area):
    if 'usuario_id' not in session:
        flash('Por favor, faça login para adotar uma área.', 'danger')
        return redirect(url_for('login'))
    
    usuario_id = session['usuario_id']
    
    try:
        adotar_area_bd(usuario_id, id_area)  # Função do database.py
        flash(f'Você adotou a área com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao adotar a área. Tente novamente.', 'danger')

    return redirect(url_for('dashboard'))

# Rota para participar de uma atividade
@app.route('/participar/<int:atividade_id>')
def participar_atividade(atividade_id):
    if 'usuario_id' not in session:
        flash('Por favor, faça login para participar de uma atividade.', 'danger')
        return redirect(url_for('login'))
    
    usuario_id = session['usuario_id']

    try:
        participar_atividade_bd(usuario_id, atividade_id)  # Função do database.py
        flash(f'Você se inscreveu na atividade com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao participar da atividade. Tente novamente.', 'danger')

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
        "Evento de plantio amanhã às 15h no IFRN-zona Norte.",
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

# Rota para logout do usuário
@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))  


if __name__ == '__main__':
    app.run(debug=True)
