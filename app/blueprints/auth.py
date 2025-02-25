from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, lm
from app.models.usuarios import Pessoa, Org

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        pessoa = Pessoa.query.filter_by(email=email).first()
        if pessoa and check_password_hash(pessoa.senha, senha):
            login_user(pessoa)
            return redirect(url_for('dashboard'))

        org = Org.query.filter_by(email=email).first()
        if org and check_password_hash(org.senha, senha):
            login_user(org)
            return redirect(url_for('dashboard'))

        flash('Erro no login! Verifique suas credenciais.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))
