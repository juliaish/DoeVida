from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import database
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) #chave aleatoria

database.init_db()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        tipo = request.form["tipo"]
        sexo_biologico = request.form["sexo_biologico"]

        nome_completo = f"{nome} {sobrenome}"

        #verifica se a senha ta no padrao de letra, numero e simbolo
        if not re.search(r"[A-Za-z]", senha) or not re.search(r"\d", senha) or not re.search(r"[^\w\s]", senha):
            flash("A senha deve conter pelo menos uma letra, um número e um símbolo.", "error")
            return redirect(url_for("cadastro"))

        senha_hash = generate_password_hash(senha)

        try:
            database.inserir_usuario(nome, sobrenome, email, senha_hash, tipo, sexo_biologico)
            usuario = database.buscar_usuario_por_email(email)
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("minha_area"))

        except Exception as e:
            flash("Erro: e-mail já cadastrado.", "error")
            return redirect(url_for("cadastro"))
         
    return render_template("login_cadastro.html", add_class = 1)

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

@app.route("/minha-area")
def minha_area():
   return render_template("minha-area.html")
    #if "usuario_id" not in session:
     #   flash("Você precisa estar logado para acessar essa página.", "error")
    #  return redirect(url_for("login"))
    #return render_template("minha_area.html", nome=session["usuario_nome"])

if __name__ == "__main__":
    app.run(debug=True)
