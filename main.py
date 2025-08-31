from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# "banco de dados" temporário só para teste
usuarios = {}

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

        # salva usuário no "banco"
        usuarios[email] = {"senha": senha, "nome": nome_completo}

        if sexo_biologico == "homem":
            tempo_ate_proxima_doacao = 60
        elif sexo_biologico == "mulher":
            tempo_ate_proxima_doacao = 90
        else:
            tempo_ate_proxima_doacao = None

        resposta = f"""
        <h2>Cadastro realizado com sucesso!</h2><hr>
        <p>Nome: {nome_completo}</p>
        <p>Email: {email}</p>
        <p>Tipo Sanguíneo: {tipo}</p>
        <p>Sexo biológico informado: {sexo_biologico}</p>
        """
        if tempo_ate_proxima_doacao:
            resposta += f"<p>Intervalo mínimo entre doações: {tempo_ate_proxima_doacao} dias</p>"
        else:
            resposta += f"<p>Para definir um intervalo seguro entre doações, consulte o hemocentro.</p>"

        resposta += '<br><a href="/">Voltar à página inicial</a>'
        return resposta
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # verifica se email existe e senha confere
        if email in usuarios and usuarios[email]["senha"] == senha:
            nome = usuarios[email]["nome"]
            return f"<h2>Bem-vindo de volta, {nome}!</h2><a href='/'>Voltar</a>"
        else:
            return "<h2>Usuário ou senha incorretos.</h2><a href='/login'>Tentar novamente</a>"

    return render_template("login.html")

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

if __name__ == "__main__":
    app.run(debug=True)
