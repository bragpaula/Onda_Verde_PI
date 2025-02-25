from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from utils import db
from utils import lm
from flask_migrate import Migrate
from app.models.usuarios import Pessoa
from app.models.usuarios import Org
from app.blueprints.auth import auth
from app.models.atividades import Atividade
from app.models.atividades import Participacao
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ondaverde_chave')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onda_verde.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    # Inicializando o LoginManager
    lm.init_app(app)
    lm.login_view = 'auth.login'
    lm.login_message = "Por favor, faça login para acessar esta página."
    lm.login_message_category = "info"

    app.register_blueprint(auth, url_prefix='/auth')


    @lm.user_loader
    def load_user(user_id):
        user = Pessoa.query.get(user_id)
        if not user:
            user = Org.query.get(user_id)
        return user
    
    # Rotas da aplicação
    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/dashboard')
    @login_required
    def dashboard():
        pessoa = Pessoa.query.filter_by(email=current_user.email).first()

        return render_template('dashboard.html', pessoa=pessoa)

    @app.route('/cadastro_fisica', methods=['GET', 'POST'])
    def cadastro_fisica():
        if request.method == 'POST':
            try:
                # Coletar dados do formulário
                nome = request.form['nome']
                email = request.form['email']
                cpf = request.form['cpf']
                data_nascimento = request.form['data_nascimento']
                telefone = request.form['telefone']
                senha = generate_password_hash(request.form['senha'])

                # Criar nova pessoa
                nova_pessoa = Pessoa(
                    nome=nome,
                    email=email,
                    cpf=cpf,
                    data_nascimento=data_nascimento,
                    telefone=telefone,
                    senha=senha
                )

                # Adicionar e salvar no banco de dados
                db.session.add(nova_pessoa)
                db.session.commit()

                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('auth.login'))  
            except Exception as e:
                db.session.rollback()  # Desfazer a transação em caso de erro
                flash(f'Erro ao cadastrar: {str(e)}', 'danger')
                return redirect(url_for('cadastro_fisica'))

        return render_template('cadastro_fisica.html')

    @app.route('/cadastro_juridica', methods=['GET', 'POST'])
    def cadastro_juridica():
        if request.method == 'POST':
            nomef = request.form['nomef']
            email = request.form['email']
            cnpj = request.form['cnpj']
            area_atuacao = request.form['area_atuacao']
            telefone = request.form['telefone']
            senha = generate_password_hash(request.form['senha'])  # Hash da senha

            nova_org = Org(nomef=nomef, email=email, cnpj=cnpj, area_atuacao=area_atuacao, telefone=telefone, senha=senha)
            db.session.add(nova_org)
            db.session.commit()

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))

        return render_template('cadastro_juridica.html')
    

    # Nosso CRUD

    @app.route('/atividade/new', methods=['POST'])
    def new_atividade():
        if request.method == 'POST':
            titulo = request.form['title']
            descricao = request.form['description']
            endereco = request.form['address']
            data_str = request.form['date']
            hora_str = request.form['time']
            
            # Converte data e hora
            data = datetime.strptime(data_str, '%Y-%m-%d').date() if data_str else None
            hora = datetime.strptime(hora_str, '%H:%M').time() if hora_str else None
            
            # Cria uma nova atividade
            atividade = Atividade(
                titulo=titulo,
                descricao=descricao,
                endereco=endereco,
                data=data,
                hora=hora,
                user_id=current_user.id
            )
            
            # Adiciona a atividade ao banco de dados
            db.session.add(atividade)
            db.session.commit()
            
            # Retorna uma resposta JSON
            return jsonify({'success': True, 'message': 'Atividade cadastrada com sucesso!'})

        return jsonify({'success': False, 'message': 'Método inválido'}), 400
    

    @app.route('/atividade/edit/<int:id>', methods=['GET', 'POST'])
    def edit_atividade(id):
        atividade = Atividade.query.get_or_404(id)
        
        if atividade.user_id != current_user.id:
            return redirect(url_for('home_atividades'))  # Redireciona se o usuário não for o dono da atividade
        
        if request.method == 'POST':
            atividade.titulo = request.form['titulo']
            atividade.descricao = request.form['descricao']
            atividade.endereco = request.form['endereco']
            
            # Converte a string de data para date
            data_str = request.form['data']
            atividade.data = datetime.strptime(data_str, '%Y-%m-%d').date()
            
            # Converte a string de hora para time
            hora_str = request.form['hora']
            atividade.hora = datetime.strptime(hora_str, '%H:%M:%S').time()
            
            db.session.commit()
            return redirect(url_for('home_atividades'))
        
        return render_template('edit_atividade.html', atividade=atividade)
    
    @app.route('/atividade/delete/<int:id>', methods=['POST'])
    def delete_atividade(id):
        atividade = Atividade.query.get_or_404(id)
        
        if atividade.user_id != current_user.id:
            return redirect(url_for('home_atividades'))  # Redireciona se o usuário não for o dono da atividade
        
        db.session.delete(atividade)
        db.session.commit()
        return redirect(url_for('home_atividades'))

    
    @app.route('/atividades')
    def home_atividades():
        pessoa = Pessoa.query.filter_by(email=current_user.email).first()
        atividades = Atividade.query.all()
        return render_template('proximas_atividades.html', atividades=atividades, pessoa=pessoa)


    @app.route('/atividade/participar/<int:id>', methods=['POST'])
    @login_required
    def participar_atividade(id):
        atividade = Atividade.query.get_or_404(id)
        
        # Verifica se o usuário já está participando
        if Participacao.query.filter_by(usuario_id=current_user.id, atividade_id=atividade.id).first():
            flash("Você já está participando dessa atividade!", "warning")
            return redirect(url_for('home_atividades'))
        
        participacao = Participacao(usuario_id=current_user.id, atividade_id=atividade.id)
        db.session.add(participacao)
        db.session.commit()
        
        flash("Inscrição na atividade realizada com sucesso!", "success")
        return redirect(url_for('home_atividades'))

    
    @app.route('/atividade/cancelar_participacao/<int:id>', methods=['POST'])
    def cancelar_participacao(id):
        usuario_id = 1  # ID do usuário logado
        participacao = Participacao.query.filter_by(usuario_id=usuario_id, atividade_id=id).first()
        if participacao:
            db.session.delete(participacao)
            db.session.commit()
        return redirect(url_for('home_atividades'))


    # Rotas adicionais
    @app.route('/areas_disponiveis')
    def areas_disponiveis():
        return render_template('areas_disponiveis.html')

    @app.route('/minhas_areas')
    def minhas_areas():
        return render_template('minhas_areas.html')

    @app.route('/relatorios')
    def relatorios():
        return render_template('relatorios.html')

    @app.route('/configuracoes')
    def configuracoes():
        return render_template('configuracoes.html')

    @app.route('/ajuda')
    def ajuda():
        return render_template('ajuda.html')

    @app.route('/sobre')
    def sobre():
        return render_template('sobre.html')

    @app.route('/adocao')
    def adocao():
        return render_template('adocao.html')

    @app.route('/feedbacks')
    def feedbacks():
        return render_template('feedbacks.html')


    return app
