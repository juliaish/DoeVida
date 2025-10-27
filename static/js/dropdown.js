document.addEventListener('DOMContentLoaded', function () {
  const dropdowns = document.querySelectorAll('.dropdown');

  dropdowns.forEach(function (dropdown) {
    const content = dropdown.querySelector('.dropdown-content');

    // Abre/fecha ao clicar
    dropdown.addEventListener('click', function (e) {
      e.stopPropagation(); // evita que feche imediatamente
      content.classList.toggle('show');
    });
  });

  // Fecha se clicar fora do menu
  document.addEventListener('click', function () {
    document.querySelectorAll('.dropdown-content').forEach(content => {
      content.classList.remove('show');
    });
  });
});
