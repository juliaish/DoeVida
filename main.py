from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from google import genai
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps
import sqlite3
import database
import re
import os

load_dotenv()
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyCf1PUfY2-h9j6p7bjT26JpFnyS7xj_eA8")

env = os.environ.get("FLASK_ENV", "development")
if env == "production":
    app.config.from_object(ProductionConfig)
elif env == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

database.init_db()

#decoradores python
def login_required(f):
    @wraps(f)
    def decor_funcao(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Você precisa estar logado para acessar essa página.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decor_funcao

def cadastro_temp_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not all(k in session for k in ["temp_nome", "temp_sobrenome", "temp_email", "temp_senha"]):
            flash("Você precisa preencher o cadastro antes de acessar o questionário.", "error")
            return redirect(url_for("cadastro"))
        return f(*args, **kwargs)
    return wrapper
#------------------------------------------------------------------------------
#rotas para paginas
@app.route("/")
def inicio():
    return render_template("index.html")

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

@app.route("/doe-aqui")
@login_required
def doe_aqui():
    return render_template("doe-aqui.html")

@app.route("/endereços")
def endereços():
    return render_template("endereços.html")
#------------------------------------------------------------------------------
#login, cadastro, minha area e mapa
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

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("inicio"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # validação de e-mail
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Insira um endereço de e-mail válido.", "error")
            return redirect(url_for("cadastro"))

        # validação de senha (maiúscula, minúscula, número e símbolo obrigatórios)
        if (not re.search(r"[a-z]", senha) or
            not re.search(r"[A-Z]", senha) or
            not re.search(r"\d", senha) or
            not re.search(r"[^\w\s]", senha)):
            flash("A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um símbolo.", "error")
            return render_template("login_cadastro.html", add_class=1)

        session["temp_nome"] = nome
        session["temp_sobrenome"] = sobrenome
        session["temp_email"] = email
        session["temp_senha"] = senha

        return redirect(url_for("questionario"))
    return render_template("login_cadastro.html", add_class=1)

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

@app.route("/maps", methods=["POST"])
@login_required
def maps():
    data = request.get_json(silent=True) or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    #API...
    return {"status": "ok", "latitude": latitude, "longitude": longitude}
#------------------------------------------------------------------------------
#questionario
@app.route("/questionario", methods=["GET", "POST"])
def questionario():
    if request.method == "POST":
        respostas = {
            "dtNascimento": request.form.get("dtNascimento"),
            "peso": request.form.get("peso"),
            "tipo": request.form.get("tipo"),
            "doencasgerais": request.form.get("doencasgerais"),
            "problemacardiaco": request.form.get("problemacardiaco"),
            "diabetes": request.form.get("diabetes"),
            "cancersangue": request.form.get("cancersangue"),
            "doencarenal": request.form.get("doencarenal"),
            "problemacoagulacao": request.form.get("problemacoagulacao"),
            "problemaepilepsia": request.form.get("problemaepilepsia"),
            "doencaorgaos": request.form.get("doencaorgaos")
        }
        idadeMin = 16
        idadeMax = 69
        pesoMin = 50
        try:
            nascimento = datetime.strptime(respostas["dtNascimento"], "%Y-%m-%d")
            hoje = datetime.today()
            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            peso = float(respostas["peso"])
        except (ValueError, TypeError):
            flash("Dados inválidos. Verifique sua data de nascimento e peso.", "error")
            return redirect(url_for("questionario"))

        inaptos = [
            respostas["doencasgerais"] == "sim",
            respostas["problemacardiaco"] == "sim",
            respostas["diabetes"] == "insulina",
            respostas["cancersangue"] == "sim",
            respostas["doencarenal"] == "sim",
            respostas["problemacoagulacao"] == "sim",
            respostas["problemaepilepsia"] == "recorrente",
            respostas["doencaorgaos"] == "sim",
            idade < idadeMin or idade > idadeMax,
            peso < pesoMin
        ]

        if any(inaptos):
            flash("Você está inapto a doar sangue no momento, mas ainda pode nos ajudar!", "warning")
            for key in ["temp_nome", "temp_sobrenome", "temp_senha", "temp_email"]:
             session.pop(key, None)
            return redirect(url_for("inicio"))
        else:
            nome = session.get("temp_nome")
            sobrenome = session.get("temp_sobrenome")
            email = session.get("temp_email")
            senha = session.get("temp_senha")
            senha_hash = generate_password_hash(senha)
            tipo = respostas["tipo"]

            try:
                database.inserir_usuario(nome, sobrenome, email, senha_hash,tipo)
                usuario = database.buscar_usuario_por_email(email)
                session["usuario_id"] = usuario["id"]
                session["usuario_nome"] = usuario["nome"]

                for key in ["temp_nome", "temp_sobrenome", "temp_senha", "temp_email"]:
                    session.pop(key, None)

                flash("Cadastro concluído com sucesso!", "success")
                return redirect(url_for("minha_area"))
            except sqlite3.IntegrityError:
                flash("Erro: e-mail já cadastrado.", "error")
                return redirect(url_for("cadastro"))
    return render_template("questionario.html")

def avaliar_aptidao_via_ia(dados):
    prompt = f"""
    Você é um avaliador médico de triagem de doadores de sangue.
    Analise as informações do doador e responda apenas "APTO" ou "INAPTO"
    conforme os critérios de saúde e segurança de doação.

    Dados do doador:
    - Idade: {dados.get("idade")}
    - Peso: {dados.get("peso")}
    - Doenças gerais: {dados.get("doencasgerais")}
    - Problemas cardíacos: {dados.get("problemacardiaco")}
    - Diabetes: {dados.get("diabetes")}
    - Câncer no sangue: {dados.get("cancersangue")}
    - Doença renal: {dados.get("doencarenal")}
    - Problemas de coagulação: {dados.get("problemacoagulacao")}
    - Epilepsia: {dados.get("problemaepilepsia")}
    - Doença em órgãos: {dados.get("doencaorgaos")}

    Retorne apenas uma palavra: APTO ou INAPTO.
    """

    resposta = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    resultado = resposta.text.strip()

    print("\n===== RESPOSTA DO GEMINI =====")
    print(resultado)
    print("===== FIM DA RESPOSTA =====\n")

    texto = resposta.text.strip().upper()

    if "INAPTO" in texto:
        return "INAPTO"
    return "APTO"

@app.route("/avaliar-questionario", methods=["POST"])
@cadastro_temp_required
def avaliar_questionario():
    dados = request.get_json() or {}

    try:
        nascimento = datetime.strptime(dados["dtNascimento"], "%Y-%m-%d")
        hoje = datetime.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        peso = float(dados["peso"])
    except (ValueError, TypeError, KeyError):
        return {"parecer": "Você não está apto para doar sangue no momento."}

    dados["idade"] = idade
    dados["peso"] = peso
    parecer = avaliar_aptidao_via_ia(dados)

    if parecer == "APTO":
        mensagem = "Parabéns! Você está apto para doar sangue."
    else:
        mensagem = "Você não está apto para doar sangue no momento."

    return {"parecer": mensagem}
#------------------------------------------------------------------------------
#inicializacao
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
