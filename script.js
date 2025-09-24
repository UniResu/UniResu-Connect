document.addEventListener('DOMContentLoaded', () => {
    // Menu Hamburger
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
    
    // Animação de contagem dos números
    const statNumbers = document.querySelectorAll('.stat-number');

    const animateNumber = (element) => {
        const target = +element.getAttribute('data-target');
        let count = 0;
        const speed = 200; // quanto maior, mais lenta a animação

        const updateCount = () => {
            const increment = target / speed;
            
            if (count < target) {
                count += increment;
                element.innerText = Math.ceil(count);
                setTimeout(updateCount, 1);
            } else {
                element.innerText = target;
            }
        };
        updateCount();
    };
    
    // Observer para iniciar a animação quando a seção estiver visível
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5 // Inicia quando 50% do elemento está visível
    });

    statNumbers.forEach(number => {
        observer.observe(number);
    });
});