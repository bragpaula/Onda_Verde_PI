from flask import Flask, render_template, request, redirect, url_for, flash
from utils import db
from utils import lm
from flask_migrate import Migrate
from app.models.usuarios import Pessoa
from app.models.usuarios import Org
from app.blueprints.auth import auth
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ondaverde_chave')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onda_verde.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Instanciando o Migrate corretamente antes de usá-lo
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
    @app.route('/proximas_atividades')
    def proximas_atividades():
        return render_template('proximas_atividades.html')


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
