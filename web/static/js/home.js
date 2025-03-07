// animacion de hamburguesa

function openMenu() {
    document.getElementById("sideMenu").style.right = "0";
}
function closeMenu() {
    document.getElementById("sideMenu").style.right = "-100%";
}

// redireccionar al hacer clic en "Iniciar Sesion"
document.getElementById("loginButton").addEventListener("click", function() {
    window.location.href = "{% url 'inicio' %}";
});

document.getElementById("sideLoginButton").addEventListener("click", function() {
    window.location.href = "{% url 'inicio' %}";
});


//footer

