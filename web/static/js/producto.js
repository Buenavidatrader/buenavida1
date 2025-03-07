//animacion de hamburguesa

function openMenu() {
    document.getElementById("sideMenu").style.right = "0";
}
function closeMenu() {
    document.getElementById("sideMenu").style.right = "-100%";
}

 // Agrega la clase 'slide-in' cuando el DOM esté listo
 document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".contact-container").classList.add("slide-in");
});


document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.2 }); // Se activa cuando el 20% de la tarjeta es visible

    cards.forEach(card => {
        observer.observe(card);
    });
});