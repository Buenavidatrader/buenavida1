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
