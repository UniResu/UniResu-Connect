document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // ... (todo o código do IntersectionObserver para os números) ...
    // [const observer = new IntersectionObserver(...)]
    // [statNumbers.forEach(...)]

    // ... (todo o código do IntersectionObserver para os projetos) ...
    // [const projetoCards = document.querySelectorAll(...)]
    // [projetoCards.forEach(...)]
    // [const projetosObserver = new IntersectionObserver(...)]
    // [projetoCards.forEach(...)]

    // ... (todo o seu código de scroll suave) ...
    // [document.querySelectorAll('a[href^="#"]').forEach(...)]

    async function buscarUsuariosDoBackend() {

        const urlDoBackend = 'http://127.0.0.1:8000/api/usuarios';

        console.log("JS Frontend: Tentando buscar dados do backend Python...");

        try {
            const response = await fetch(urlDoBackend);

            const data = await response.json();

            if (data.usuarios) {
                console.log("✅ Sucesso! Dados recebidos do backend:", data.usuarios);

            } else if (data.erro) {
                console.error("❌ O backend Python reportou um erro:", data.erro);
            }

        } catch (error) {
            console.error("❌ Falha grave ao tentar conectar com o backend:", error);
        }
    }

    buscarUsuariosDoBackend();
});
