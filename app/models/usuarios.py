from utils import db
from flask_login import UserMixin


# Modelo para Pessoa
class Pessoa(db.Model, UserMixin):
    __tablename__ = "pessoa"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # Campo CPF
    data_nascimento = db.Column(db.String(10), nullable=False)  # Campo data_nascimento
    telefone = db.Column(db.String(15), nullable=False)  # Campo telefone
    senha = db.Column(db.String(150), nullable=False)

    def __init__(self, nome, email, cpf, data_nascimento, telefone, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.senha = senha
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
    
    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'telefone': self.telefone,
            'senha': self.senha
        }

# Modelo para Organização
class Org(db.Model, UserMixin):
    __tablename__ = "org"
    id = db.Column(db.Integer, primary_key=True)
    nomef = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)  # Campo CNPJ
    area_atuacao = db.Column(db.String(50), nullable=False)  
    telefone = db.Column(db.String(15), nullable=False)  
    senha = db.Column(db.String(150), nullable=False)

    def __init__(self, nomef, email, cnpj, area_atuacao, telefone, senha):
        self.nomef = nomef
        self.email = email
        self.cnpj = cnpj
        self.area_atuacao = area_atuacao
        self.telefone = telefone
        self.senha = senha
    def __repr__(self):
        return f'<Org {self.nomef}>'