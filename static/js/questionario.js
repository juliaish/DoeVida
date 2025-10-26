document.querySelector(".form-questionario").addEventListener("submit", function(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const dados = {};
    formData.forEach((v, k) => dados[k] = v);

    const botao = document.getElementById("botao-enviar");
    botao.style.display = "none";

    fetch("/avaliar-questionario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(resp => {
        const mensagemContainer = document.getElementById("mensagem-container");
        const mensagemTexto = document.getElementById("mensagem-texto");
        const mensagemBotao = document.getElementById("mensagem-botao");

        mensagemContainer.style.display = "block";
        mensagemTexto.textContent = resp.parecer;

        mensagemBotao.onclick = () => {
            if(resp.parecer.toUpperCase().includes("APTO")) {
                form.submit();
            } else {
                window.location.href = "/";
            }
        };

        window.scrollTo({ top: 0, behavior: "smooth" });
    })
    .catch(err => {
        alert("Erro ao processar o questionário.");
        console.error(err);
        botao.style.display = "block";
    });
});
