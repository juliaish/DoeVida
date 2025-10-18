from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from database import get_db_connection
from datetime import datetime
from functools import wraps
import sqlite3
import database
import re
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

env = os.environ.get("FLASK_ENV", "development")

if env == "production":
    app.config.from_object(ProductionConfig)
elif env == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

database.init_db()

#decorador python
def login_required(f):
    @wraps(f)
    def decor_funcao(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Você precisa estar logado para acessar essa página.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decor_funcao

#rotas para paginas
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        senha = request.form["senha"]

        senha_hash = generate_password_hash(senha)

        try:
            database.inserir_usuario(nome, sobrenome, email, senha_hash)
            usuario = database.buscar_usuario_por_email(email)
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("minha_area"))

        except Exception as e:
            print(f"Erro no cadastro: {e}")
            flash("Erro ao cadastrar. Verifique os dados e tente novamente.", "error")
            return redirect(url_for("cadastro"))

    return render_template("login_cadastro.html", add_class=1)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = database.buscar_usuario_por_email(email)

        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash(f"Bem-vindo(a) de volta, {usuario['nome']}!", "success")
            return redirect(url_for("minha_area"))
        else:
            flash("Usuário ou senha incorretos.", "error")
            return redirect(url_for("login"))

    return render_template("login_cadastro.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/tipos-sanguineos")
def tipos_sanguineos():
    return render_template("tipos-sanguineos.html")

@app.route("/requisitos-para-doar")
def requisitos_para_doar():
    return render_template("requisitos.html")

@app.route("/pos-doacao")
def pos_doacao():
    return render_template("pos.html")

@app.route("/minha-area", methods=["GET", "POST"])
@login_required
def minha_area():
    usuario_id = session["usuario_id"]
    conn = get_db_connection()

    if request.method == "POST":
        print("FORM RECEBIDO:", request.form)

        nome = request.form.get("nome")
        sobrenome = request.form.get("sobrenome")
        email = request.form.get("email")
        tipo = request.form.get("tipo")

        conn.execute("""
            UPDATE usuarios
            SET nome = ?, sobrenome = ?, email = ?, tipo = ?
            WHERE id = ?
        """, (nome, sobrenome, email, tipo, usuario_id))
        conn.commit()
        conn.close()

        flash("Dados atualizados com sucesso!", "success")
        return redirect(url_for("minha_area"))

    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    conn.close()
    return render_template("minha-area.html", usuario=usuario)

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("inicio"))

@app.route("/doe-aqui")
@login_required
def doe_aqui():
    return render_template("doe-aqui.html")

@app.route("/endereços")
def endereços():
    return render_template("endereços.html")

@app.route("/maps", methods=["POST"])
@login_required
def maps():
    data = request.get_json(silent=True) or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    #API...
    return {"status": "ok", "latitude": latitude, "longitude": longitude}

#inicializacao
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
