from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import conectar_bd, criar_tabelas, inserir_pessoa, buscar_usuario_por_email, buscar_org_por_email, buscar_atividades, buscar_areas, buscar_areas_do_usuario
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'ondaverde_chave'

criar_tabelas()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # buscando em pessoas
        pessoa = buscar_usuario_por_email(email)
        if pessoa and check_password_hash(pessoa['senha'], senha):
            session['usuario'] = pessoa['nome']
            session['tipo'] = 'pessoa'
            session['usuario_id'] = pessoa['cpf']  # armazenando o ID do usuário
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        # buscando em organizações
        org = buscar_org_por_email(email)
        if org and check_password_hash(org['senha'], senha):
            session['usuario'] = org['nomef']
            session['tipo'] = 'org'
            session['usuario_id'] = org['cnpj']  # armazenando o ID da organização
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        flash('Erro no login! Verifique suas credenciais.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Por favor, faça login para acessar o dashboard.', 'danger')
        return redirect(url_for('login'))
    
    atividades = buscar_atividades()
    areas = buscar_areas()
    minhas_areas = buscar_areas_do_usuario(session.get('usuario_id')) # necessário armazenar o id do usuario na session
    return render_template('dashboard.html', atividades=atividades, areas=areas, minhas_areas=minhas_areas)



# Rota para detalhes de uma área
@app.route('/detalhes/<int:id_area>')
def detalhes_area(id_area):
    return render_template('detalhes.html', id_area=id_area)

# Rota para a página de adotar uma area
@app.route('/adotar/<int:id_area>')
def adotar_area(id_area):
    if 'usuario_id' not in session:
        flash('Por favor, faça login para adotar uma área.', 'danger')
        return redirect(url_for('login'))
    
    usuario_id = session['usuario_id']
    adotar_area(usuario_id, id_area)  # Função do database.py
    flash(f'Você adotou a área {id_area} com sucesso!', 'success')
    return redirect(url_for('dashboard'))

# Rota para participar de uma atividade
def participar_atividade(usuario_id, atividade_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuario_atividades (usuario_id, atividade_id)
        VALUES (?, ?)
    ''', (usuario_id, atividade_id))
    conn.commit()
    conn.close() 

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



# Rota para logout do usuário
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
