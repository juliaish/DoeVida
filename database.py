import sqlite3

def get_db_connection():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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
    conn.commit()
    conn.close()

def inserir_usuario(nome, sobrenome, email, senha_hash, tipo, sexo):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO usuarios (nome, sobrenome, email, senha, tipo, sexo_biologico)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, sobrenome, email, senha_hash, tipo, sexo))
    conn.commit()
    conn.close()

def buscar_usuario_por_email(email):
    conn= get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    conn.close()
    return usuario

if __name__=="__main__":
    init_db()
    print("Banco de dados inicializado!")