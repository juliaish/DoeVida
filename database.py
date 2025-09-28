import sqlite3
import json

def get_db_connection():
    """conexao com o bd"""
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """inicia com a tabela dos usuarios"""
    with get_db_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT,
            sexo_biologico TEXT
        )
        """)
        #questionario
        conn.execute("""
        CREATE TABLE IF NOT EXISTS questionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            respostas TEXT NOT NULL,
            resultado TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

def inserir_usuario(nome, sobrenome, email, senha_hash, tipo, sexo):
    """adiciona um novo usuario"""
    with get_db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO usuarios (nome, sobrenome, email, senha, tipo, sexo_biologico)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, sobrenome, email, senha_hash, tipo, sexo))
        conn.commit()  # Garante que a transação seja salva
        return cursor.lastrowid

def buscar_usuario_por_email(email):
    """busca usuario por email"""
    with get_db_connection() as conn:
        usuario = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    return usuario

def salvar_questionario(usuario_id, respostas, resultado):
    with get_db_connection() as conn:
        conn.execute("""
             INSERT INTO questionarios (usuario_id, respostas, resultado)
             VALUES (?, ?, ?)
        """, (usuario_id, json.dumps(respostas), resultado))
        conn.commit()

if __name__=="__main__":
    init_db()
    print("Banco de dados inicializado!")