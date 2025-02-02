import sqlite3
from werkzeug.security import generate_password_hash

def conectar_bd():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row  # Configura para que o resultado seja tratado como dicionário
    return conn


# Função para criar a tabela de pessoa física
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

# Função para criar a tabela de organização
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

# Função para criar a tabela de atividades
def criar_tabela_atividades():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Função para criar a tabela de áreas verdes
def criar_tabela_areas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL,
        descricao TEXT,
        estado TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Função para criar a tabela de relacionamento usuário-áreas
def criar_tabela_usuario_areas():
    conn = conectar_bd()
    cursor = conn.cursor()
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

# Função para cadastrar pessoa física
def cadastrar_pessoa(nome, email, cpf, data_nasc, telefone, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            INSERT INTO pessoa (cpf, nome, email, data_nasc, telefone, senha, tipo)
            VALUES (?, ?, ?, ?, ?, ?, 'pessoa')
        ''', (cpf, nome, email, data_nasc, telefone, senha))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError('Erro: CPF ou e-mail já cadastrados.')
    finally:
        conn.close()

# Função para cadastrar organização
def cadastrar_org(nomef, email, cnpj, area_atuacao, telefone, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            INSERT INTO org (cnpj, nomef, email, area_atuacao, telefone, senha, tipo)
            VALUES (?, ?, ?, ?, ?, ?, 'org')
        ''', (cnpj, nomef, email, area_atuacao, telefone, senha))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError('Erro: CNPJ ou e-mail já cadastrados.')
    finally:
        conn.close()
