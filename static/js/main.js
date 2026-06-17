// ============================================================
// LICORERA INTELIGENTE — JavaScript principal
// ============================================================

// Mostrar fecha actual en el topbar
function updateDate() {
  const el = document.getElementById('current-date');
  if (!el) return;
  const now = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  el.textContent = now.toLocaleDateString('es-CO', options);
}
updateDate();

// Toggle sidebar en móvil
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// Cerrar sidebar al hacer clic fuera (móvil)
document.addEventListener('click', function(e) {
  const sidebar = document.getElementById('sidebar');
  const toggle  = document.querySelector('.menu-toggle');
  if (sidebar && sidebar.classList.contains('open') &&
      !sidebar.contains(e.target) && e.target !== toggle) {
    sidebar.classList.remove('open');
  }
});

// Auto-ocultar alertas después de 4 segundos
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(a => {
    a.style.transition = 'opacity 0.5s';
    a.style.opacity = '0';
    setTimeout(() => a.remove(), 500);
  });
}, 4000);
