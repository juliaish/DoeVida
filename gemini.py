def perguntas():
    return [
        {"pergunta": "zz"},
        {"pergunta": "zz"},
        {"pergunta": "zz"}
    ]
def parecer(respostas):
    if int(respostas.get("idade", 0)) < 16:
        return "Inapto para doar (menor de idade)"
    return "Apto para doar"