
document.querySelector(".form-questionario").addEventListener("submit", function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const respostas = {};
  formData.forEach((value, key) => respostas[key] = value);

  const idadeMin = 16;
  const idadeMax = 69;
  const pesoMin = 50;

  const hoje = new Date();
  const nascimento = new Date(respostas.dtNascimento);
  const idade = hoje.getFullYear() - nascimento.getFullYear() - ((hoje.getMonth() < nascimento.getMonth()) || (hoje.getMonth() === nascimento.getMonth() && hoje.getDate() < nascimento.getDate()) ? 1 : 0);
  const peso = parseFloat(respostas.peso);

  const inaptos = [
    respostas.doencasgerais === "sim",
    respostas.problemacardiaco === "sim",
    respostas.diabetes === "insulina",
    respostas.cancersangue === "sim",
    respostas.doencarenal === "sim",
    respostas.problemacoagulacao === "sim",
    respostas.problemaepilepsia === "recorrente",
    respostas.doencaorgaos === "sim",
    idade < idadeMin || idade > idadeMax,
    peso < pesoMin
  ];

  document.getElementById("botao-enviar").style.display = "none";

  const mensagemContainer = document.getElementById("mensagem-container");
  window.scrollTo({
  top: 0,
  behavior: "smooth"
  });

  const mensagemTexto = document.getElementById("mensagem-texto");
  const mensagemBotao = document.getElementById("mensagem-botao");

  mensagemContainer.style.display = "block";

  if (inaptos.includes(true)) {
    mensagemTexto.textContent = "Você não está apto para doar sangue no momento.";
    mensagemBotao.onclick = () => window.location.href = "/";
  } else {
    mensagemTexto.textContent = "Parabéns! Você está apto para doar sangue.";
    mensagemBotao.onclick = () => form.submit();
  }
});