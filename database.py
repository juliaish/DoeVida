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
            tipo TEXT
        )
        """)

def inserir_usuario(nome, sobrenome, email, senha_hash, tipo):
    with get_db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO usuarios (nome, sobrenome, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, sobrenome, email, senha_hash, tipo))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

def buscar_usuario_por_email(email):
    """busca usuario por email"""
    with get_db_connection() as conn:
        usuario = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    return usuario

if __name__=="__main__":
    init_db()
    print("Banco de dados inicializado!")