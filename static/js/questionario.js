document.querySelector(".form-questionario").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const respostas = {};

  formData.forEach((value, key) => {
    respostas[key] = value;
  });

  const prompt = `
Avalie se esta pessoa está apta para doar sangue com base nas respostas abaixo. Responda apenas com "Apto" ou "Inapto".

- Data de nascimento: ${respostas.dtNascimento}
- Gênero: ${respostas.genero}
- Tipo sanguíneo: ${respostas.tipo}
- Peso: ${respostas.peso}
- Teve doenças graves (HIV, hepatite, etc): ${respostas.doencasgerais}
- Problema cardíaco grave: ${respostas.problemacardiaco}
- Diabetes: ${respostas.diabetes}
- Câncer no sangue: ${respostas.cancersangue}
- Doença renal crônica: ${respostas.doencarenal}
- Problemas de coagulação: ${respostas.problemacoagulacao}
- Epilepsia: ${respostas.problemaepilepsia}
- Doença autoimune em órgãos: ${respostas.doencaorgaos}
`;
const GEMINI_API_KEY = "AIzaSyBCnayTPVuRYOeCU178SrIn1uui5XdLXzE"; 

  const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=SUA_API_KEY", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }]
    })
  });

  const result = await response.json();
  const output = result?.candidates?.[0]?.content?.parts?.[0]?.text || "Erro na análise";

  if (output.includes("Apto")) {
    form.submit(); 
  } else {
    alert("Você não está apto para doar sangue neste momento.");
  }
});
