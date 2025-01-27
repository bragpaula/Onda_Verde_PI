from database import db

class Usuario(db.Model):
    __tablename__="usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String (100))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    telefone = db.Column(db.Integer(16))
    rua = db.Column(db.String(100))
    numero = db.Column(db.Integer(60))
    bairro = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    tipo_usuario = db.Column(db.String(100))


    senha = db.Column(db.String(100))

    def __init__(self, nome, email, endereco,telefone, rua, numero, bairro, estado, tipo_usuario):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.estado = estado


    def __repr__(self):
        return "Usuario: {}".format(self.nome)