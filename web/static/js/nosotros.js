document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });

    items.forEach(item => {
        observer.observe(item);
    });
});


// animacion de preguntas

document.addEventListener("DOMContentLoaded", () => {
    const faqItems = document.querySelectorAll(".faq-item");

    // Detectar cuando las preguntas entran en la vista del usuario
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.2 }); // Se activa cuando el 20% del elemento es visible

    faqItems.forEach(item => observer.observe(item));

    // Agregar funcionalidad de acordeón
    document.querySelectorAll(".faq-question").forEach(item => {
        item.addEventListener("click", () => {
            const faqItem = item.parentNode;
            faqItem.classList.toggle("active");
        });
    });
});