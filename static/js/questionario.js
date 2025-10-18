document.querySelector(".form-questionario").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const respostas = {};

  formData.forEach((value, key) => {
    respostas[key] = value;
  });

  const idadeMin = 16;
  const idadeMax = 69;
  const pesoMin = 50;

  const hoje = new Date();
  const nascimento = new Date(respostas.dtNascimento);
  const idade = hoje.getFullYear() - nascimento.getFullYear();
  const peso = parseFloat(respostas.peso);

  const inaptos = [
    respostas.doencasgerais ==="sim",
    respostas.problemacardiaco ==="sim",
    respostas.diabetes === "insulina",
    respostas.cancersangue === "sim",
    respostas.doencarenal === "sim",
    respostas.problemacoagulacao === "sim",
    respostas.problemaepilepsia === "recorrente",
    respostas.doencaorgaos === "sim",
    idade < idadeMin || idade > idadeMax,
    peso < pesoMin
  ];

  if (inaptos.incluedes(true)) {
    alert("Você nao está apto para doar sangue no momento.");
  } else {
    alert("Parabéns! Você está apto para doar sangue.");
    form.submit();
  }
});
