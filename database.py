import sqlite3
from werkzeug.security import generate_password_hash

def conectar_bd():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row  # Para buscar por nome de coluna
    return conn

def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Tabela de pessoas físicas
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

    # Tabela de organizações
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

    # Tabela de atividades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT
    )
    ''')

    # Tabela de áreas verdes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL,
        descricao TEXT
        estado TEXT NOT NULL
    )
    ''')

    # Tabela de relacionamento usuário-áreas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario_areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        area_id INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES pessoa(cpf),
        FOREIGN KEY (area_id) REFERENCES areas(id)
    )
    ''')

    conn.commit()
    conn.close()

# Função para inserir uma nova pessoa física
def inserir_pessoa(cpf, nome, email, data_nasc, telefone, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pessoa (cpf, nome, email, data_nasc, telefone, senha, tipo)
        VALUES (?, ?, ?, ?, ?, ?, 'pessoa')
    ''', (cpf, nome, email, data_nasc, telefone, generate_password_hash(senha)))
    conn.commit()
    conn.close()

# Função para buscar um usuário por email
def buscar_usuario_por_email(email):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoa WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Função para buscar uma organização por email
def buscar_org_por_email(email):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM org WHERE email = ?', (email,))
    org = cursor.fetchone()
    conn.close()
    return org

# Função para buscar todas as atividades
def buscar_atividades():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM atividades')
    atividades = cursor.fetchall()
    conn.close()
    return atividades

# Função para buscar todas as áreas
def buscar_areas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM areas')
    areas = cursor.fetchall()
    conn.close()
    return areas

# Função para buscar as áreas de um usuário
def buscar_areas_do_usuario(usuario_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT areas.* FROM areas
    JOIN usuario_areas ON areas.id = usuario_areas.area_id
    WHERE usuario_areas.usuario_id = ?
    ''', (usuario_id,))
    areas = cursor.fetchall()
    conn.close()
    return areas

def adotar_area(usuario_id, area_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuario_areas (usuario_id, area_id)
        VALUES (?, ?)
    ''', (usuario_id, area_id))
    conn.commit()
    conn.close()

def participar_atividade(usuario_id, atividade_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuario_atividades (usuario_id, atividade_id)
        VALUES (?, ?)
    ''', (usuario_id, atividade_id))
    conn.commit()
    conn.close()