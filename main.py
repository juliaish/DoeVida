from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/cadastro")
def cadastro():
    if request.method =="POST":
        email = request.form["email"]
        senha = request.form["senha"]
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        tipo = request.form["tipo"]
        sexo_biologico = request.form["sexo_biologico"]

        nome_completo = f"{nome} {sobrenome}"

        if sexo_biologico =="homem":
            tempo_ate_proxima_doacao = 60
        elif sexo_biologico == "mulher":
            tempo_ate_proxima_doacao = 90
        else:
            tempo_ate_proxima_doacao = None #para outro/prefiro nao informar

        resposta = f"""
        <h2>Cadastro realizado com sucesso!<hr>
        <p>Nome: {nome_completo}</p>
        <p>Email: {email}</p>
        <p>Tipo Sanguíneo: {tipo}</p>
        <Sexo biológico informado: {sexo_biologico}</p>
        """
        if tempo_ate_proxima_doacao:
            resposta+= f"<p>Intervalo mínimo entre doaçoes: {tempo_ate_proxima_doacao}"
        else:
            resposta+= f"<p>Para definir um intervalo seguro entre doaçoes, consulte o hemocentro."
        resposta += '<a href="/">Voltar à pagina inicial</a>'
        return resposta
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

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
