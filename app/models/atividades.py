from utils import db
from app.models.usuarios import Pessoa

class Atividade(db.Model):
    __tablename__ = "atividade"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    data = db.Column(db.Date, nullable=True) 
    hora = db.Column(db.Time, nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)  # Relacionamento com o usuario (pessoa)
    user = db.relationship('Pessoa', backref=db.backref('atividades', lazy=True))  # Define o relacionamento com o usuario (pessoa)

    def __repr__(self):
        return f"<Atividade {self.titulo}>"
    
class Participacao(db.Model):
    __tablename__ = "participacao"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False) 
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'), nullable=False)
    
    atividade = db.relationship('Atividade', backref='participacoes', lazy=True)

    def __repr__(self):
        return f"<Participacao {self.usuario_id} na Atividade {self.atividade_id}>"
