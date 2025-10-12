document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.querySelector('.search-form');

  if (searchForm) {
    searchForm.addEventListener('submit', e => {
      e.preventDefault();
      alert('Busca ainda não implementada!');
    });
  }
});