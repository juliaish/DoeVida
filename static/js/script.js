/*responsividade do header*/
class Mobile {
  constructor(mobileMenu, navList, navLinks) {
    this.mobileMenu = document.querySelector(mobileMenu);
    this.navList = document.querySelector(navList);
    this.navLinks = document.querySelectorAll(navLinks);
    this.activeClass = "active";

    this.handleClick = this.handleClick.bind(this);
  }

  animateLinks() {
    this.navLinks.forEach((link, index) => {
      link.style.animation
        ? (link.style.animation = "")
        : (link.style.animation = `navLinkFade 0.5s ease forwards ${
            index / 7 + 0.3
          }s`);
    });
  }

  handleClick() {
    this.navList.classList.toggle(this.activeClass);
    this.mobileMenu.classList.toggle(this.activeClass);
    this.animateLinks();
  }

  addClickEvent() {
    this.mobileMenu.addEventListener("click", this.handleClick);
  }

  init() {
    if (this.mobileMenu) {
      this.addClickEvent();
    }
    return this;
  }
}
function mudarPagina(pagina) {
  window.location.href = pagina;
}


const mobile = new Mobile(
  ".mobile-menu",
  ".nav-list",
  ".nav-list li",
);
mobile.init();
const btnEditar = document.getElementById("btnEditar");
const btnSalvar = document.getElementById("btnSalvar");
const campos = document.querySelectorAll("#formPerfil input, #formPerfil select");


btnEditar.addEventListener("click", () => {
  campos.forEach(campo => {

    if (campo.tagName === "INPUT" && campo.type !== "hidden") {
      campo.readOnly = false;
    }

    if (campo.tagName === "SELECT") {
      campo.disabled = false;
    }
  });
  btnEditar.style.display = "none";
  btnSalvar.style.display = "block";
});

const form = document.getElementById("formPerfil");
form.addEventListener("submit", () => {
  const selectTipo = document.getElementById("tipo");
  const hiddenTipo = document.querySelector("input[type=hidden][name=tipo]");
  if (selectTipo && hiddenTipo) {
    hiddenTipo.value = selectTipo.value;
  }
});

// mostrar/ocultar senha
const toggleSenha = document.getElementById("toggleSenha");
const inputSenha = document.getElementById("senha");

if (toggleSenha && inputSenha) {
  toggleSenha.addEventListener("click", () => {
    if (inputSenha.type === "password") {
      inputSenha.type = "text";
      toggleSenha.textContent = "🙈";
    } else {
      inputSenha.type = "password";
      toggleSenha.textContent = "👁️";
    }
  });
};
