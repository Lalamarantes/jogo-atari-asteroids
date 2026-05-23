// script.js

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Smooth Scrolling para os links âncora
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            // Verifica se é apenas '#'
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Rola a página até o elemento alvo de forma suave
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 2. Intersection Observer para Animação de Fade-in ao Rolar a Página
    const observerOptions = {
        root: null, // Usa o viewport como área de detecção
        rootMargin: '0px',
        threshold: 0.15 // Dispara quando 15% do elemento está visível
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Adiciona a classe que inicia a transição CSS
                entry.target.classList.add('is-visible');
                // Opcional: Desobserva o elemento após animar (ocorre apenas uma vez)
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Seleciona todos os elementos com a classe .animate-on-scroll
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => scrollObserver.observe(el));

});
