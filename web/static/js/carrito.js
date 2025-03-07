// filepath: /c:/Users/Ambiente 105/Downloads/proyectouno-main/proyectouno-main/web/static/js/carrito.js
document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    updateCartCount();

    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            const productName = button.getAttribute('data-name');
            const productPrice = button.getAttribute('data-price');

            const product = { id: productId, name: productName, price: productPrice, quantity: 1 };

            const existingProductIndex = cart.findIndex(item => item.id === productId);
            if (existingProductIndex !== -1) {
                cart[existingProductIndex].quantity += 1;
            } else {
                cart.push(product);
            }

            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCount();
            alert('Producto agregado al carrito');
        });
    });

    const payButton = document.querySelector('.payment-method button');
    const paymentSummaryModal = document.querySelector('.payment-summary-modal');
    const closeSummaryButton = document.querySelector('.payment-summary-content .close-btn');
    const cartItems = document.querySelectorAll('.cart-item');
    const totalElement = document.querySelector('.cart-total .total');

    payButton.addEventListener('click', function() {
        const summaryList = paymentSummaryModal.querySelector('ul');
        summaryList.innerHTML = '';

        cartItems.forEach(item => {
            const itemName = item.querySelector('.cart-item-details').textContent.trim();
            const itemPrice = item.querySelector('.cart-item-price').textContent.trim();
            const listItem = document.createElement('li');
            listItem.textContent = `${itemName} - ${itemPrice}`;
            summaryList.appendChild(listItem);
        });

        const totalAmount = totalElement.textContent.trim();
        paymentSummaryModal.querySelector('.total').textContent = `Total a pagar: ${totalAmount}`;

        paymentSummaryModal.style.display = 'flex';
    });

    closeSummaryButton.addEventListener('click', function() {
        paymentSummaryModal.style.display = 'none';
    });
});

function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCount = cart.reduce((total, product) => total + product.quantity, 0);
    document.getElementById('cart-count').textContent = cartCount;
}

function renderCartItems() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalContainer = document.getElementById('cart-total');

    cartItemsContainer.innerHTML = '';
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>El carrito está vacío</p>';
    } else {
        let total = 0;
        cart.forEach(item => {
            total += item.price * item.quantity;
            cartItemsContainer.innerHTML += `
                <div class="cart-item col-md-4">
                    <img src="${item.image}" alt="${item.name}" class="img-fluid">
                    <div class="cart-item-details">
                        <h5>${item.name}</h5>
                        <p>Precio: $${item.price} COP</p>
                        <p>Cantidad: ${item.quantity}</p>
                        <button class="remove-from-cart" data-id="${item.id}">Eliminar</button>
                    </div>
                </div>
            `;
        });
        cartTotalContainer.innerHTML = `<h3>Total: $${total} COP</h3>`;
    }

    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            const productIndex = cart.findIndex(item => item.id === productId);
            if (productIndex !== -1) {
                cart.splice(productIndex, 1);
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartCount();
                renderCartItems();
            }
        });
    });
}


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

document.addEventListener('DOMContentLoaded', () => {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalContainer = document.getElementById('cart-total');
    const payButton = document.getElementById('pay-button');
    const paymentModal = document.getElementById('payment-modal');
    const modalContent = document.querySelector('.modal-content');
    const cartSummary = document.getElementById('cart-summary');
    const qrCode = document.getElementById('qr-code');
    const userMessage = document.getElementById('user-message');

    function updateCart() {
        fetch('/api/get_cart/')
            .then(response => response.json())
            .then(cart => {
                if (cart.length === 0) {
                    cartItemsContainer.innerHTML = '<p>El carrito está vacío</p>';
                    cartTotalContainer.innerHTML = '';
                } else {
                    cartItemsContainer.innerHTML = '';
                    let total = 0;
                    cart.forEach((item, index) => {
                        total += item.price * item.quantity;
                        cartItemsContainer.innerHTML += `
                            <div class="cart-item">
                                <img src="{% static 'img/${item.img}' %}" alt="${item.name}" class="cart-item-image">
                                <div class="cart-item-details">
                                    <h5>${item.name}</h5>
                                    <p>Precio: $${item.price} COP</p>
                                    <p>Cantidad: 
                                        <button class="btn btn-secondary btn-sm" onclick="decrementQuantity(${index})">-</button>
                                        ${item.quantity}
                                        <button class="btn btn-secondary btn-sm" onclick="incrementQuantity(${index})">+</button>
                                    </p>
                                    <button class="btn btn-danger btn-sm" onclick="removeFromCart(${index})">Eliminar</button>
                                </div>
                            </div>
                        `;
                    });
                    cartTotalContainer.innerHTML = `<h3>Total: $${total} COP</h3>`;
                }
            });
    }

    window.incrementQuantity = function(index) {
        fetch('/api/increment_quantity/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ index: index })
        }).then(updateCart);
    }

    window.decrementQuantity = function(index) {
        fetch('/api/decrement_quantity/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ index: index })
        }).then(updateCart);
    }

    window.removeFromCart = function(index) {
        fetch('/api/remove_from_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ index: index })
        }).then(updateCart);
    }

    payButton.addEventListener('click', () => {
        fetch('/api/get_cart/')
            .then(response => response.json())
            .then(cart => {
                if (cart.length > 0) {
                    let total = 0;
                    let summary = '';
                    cart.forEach(item => {
                        total += item.price * item.quantity;
                        summary += `<p>${item.name} x ${item.quantity} - $${item.price * item.quantity} COP</p>`;
                    });
                    cartSummary.innerHTML = summary + `<h3>Total: $${total} COP</h3>`;
                    qrCode.src = "{% static 'img/qr.png' %}"; // Asegúrate de tener la imagen del código QR en la ruta correcta

                    // Obtener el nombre del usuario y actualizar el mensaje
                    const userName = "{{ user.get_full_name }}"; // Asegúrate de que esta variable esté disponible en tu plantilla
                    userMessage.innerHTML = `Señor@ ${userName}, por favor escanee el código QR para completar su pago.`;

                    paymentModal.style.display = 'block';
                    modalContent.classList.remove('slide-up');
                    modalContent.classList.add('slide-down');
                }
            });
    });

    window.closeModal = function() {
        modalContent.classList.remove('slide-down');
        modalContent.classList.add('slide-up');
        setTimeout(() => {
            paymentModal.style.display = 'none';
        }, 500); // Duración de la animación
    }

    window.sendWhatsApp = function() {
        const phoneNumber = '3133260694'; // Reemplaza con el número de teléfono al que deseas enviar el mensaje
        const message = encodeURIComponent('Hola, aquí está mi comprobante de pago.');
        const url = `https://wa.me/${phoneNumber}?text=${message}`;
        window.open(url, '_blank');
    }

    updateCart();
});






