# DoeVida

DoeVida é um site voltado para pessoas que nunca doaram sangue, oferecendo informações sobre doação, cuidados pós-doação,
requisitos para doar, locais de coleta, tipos sanguíneos (quem doa para quem), entre outros. 
O objetivo principal é conectar potenciais doadores à doação de sangue, tornando esse ato importante mais acessível. 
Com apenas uma doação, é possível salvar até quatro vidas. Se uma família se reunir em um sábado para doar, podem salvar até 16 pessoas.

---
## Tecnologias Utilizadas

* Flask (Python)
* SQLite
* Google Gemini API (IA)
* HTML, CSS, JavaScript
* VLibras (acessibilidade)

---
## Funcionalidades

* Cadastro e login de usuários.
* Questionário de triagem para doação de sangue.
* Avaliação via IA utilizando a Gemini API.
* Área do usuário para gerenciar informações pessoais.
* Mapas de localização de doações (quando logado).
* Mensagens e feedback visual (flash messages).
* Páginas informativas:
  * Pós-doação
  * Requisitos para doar
  * Tipos sanguíneos

---
## Instalação
1. Clone o repositório:

   ```bash
   git clone <link-do-repositório>
   ```
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` com suas variáveis de ambiente:

   ```env
   FLASK_ENV=development
   SECRET_KEY=sua_chave_secreta
   GEMINI_API_KEY=sua_chave_gemini
   ```

---
## Estrutura do Projeto

```
DoeVida/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/
│   ├── endereços.html
│   ├── index.html
│   ├── login_cadastro.html
│   ├── minha-area.html
│   ├── pos.html
│   ├── questionario.html
│   ├── requisitos.html
│   ├── sobre.html
│   └── tipos-sanguineos.html
│
├── .env                # Variáveis de ambiente (Gemini API)
├── a.env               # Chave secreta do Flask
├── main.py
├── database.py
└── config.py
```

---
## Considerações

* **Limitações**:
* A triagem feita pelo site é apenas informativa e não substitui a avaliação médica realizada na unidade de saúde.
* 
* Além disso, é uma versão simples, praticamente um protótipo, com potencial para evoluir em funcionalidades futuras.
* **Acessibilidade**: O site conta com o widget VLibras para suporte a Libras.

---
## Créditos

* Desenvolvido por **Julia Queiroz e Wanessa Estrela**
* Integração com **Google Gemini API** para avaliação via IA.
* Recursos de acessibilidade com **VLibras**.
