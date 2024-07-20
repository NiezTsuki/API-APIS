// Función para formatear la fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Función para obtener y mostrar los productos
async function fetchProducts() {
    const response = await fetch('/products/json/');
    const products = await response.json();
    const tableBody = document.getElementById('product-table-body');
    
    products.forEach(product => {
        const row = document.createElement('tr');
        
        const productCodeCell = document.createElement('td');
        productCodeCell.textContent = product['Código del producto'];
        row.appendChild(productCodeCell);

        const brandCell = document.createElement('td');
        brandCell.textContent = product['Marca'];
        row.appendChild(brandCell);

        const codeCell = document.createElement('td');
        codeCell.textContent = product['Código'];
        row.appendChild(codeCell);

        const nameCell = document.createElement('td');
        nameCell.textContent = product['Nombre'];
        row.appendChild(nameCell);

        const priceCell = document.createElement('td');
        product['Precio'].forEach(price => {
            const dateElement = document.createElement('p');
            dateElement.textContent = formatDate(price['Fecha']);
            priceCell.appendChild(dateElement);

            const valueElement = document.createElement('p');
            valueElement.textContent = price['Valor'];
            priceCell.appendChild(valueElement);
        });
        row.appendChild(priceCell);

        const stockCell = document.createElement('td');
        stockCell.textContent = product['Stock'];
        row.appendChild(stockCell);

        const actionCell = document.createElement('td');
        const addButton = document.createElement('button');
        addButton.textContent = 'Agregar al carrito';
        addButton.onclick = () => addToCart(product['Código del producto'], product['Nombre'], product['Precio'][0]['Valor']);
        actionCell.appendChild(addButton);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
    });
}

const cart = [];

// Función para agregar productos al carrito
function addToCart(id, name, price) {
    const cartItem = cart.find(item => item.id === id);

    if (cartItem) {
        cartItem.quantity++;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    displayCart();
}

// Función para mostrar el carrito
function displayCart() {
    const cartTableBody = document.getElementById('cart-table-body');
    cartTableBody.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        total += item.price * item.quantity;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>${item.quantity}</td>
            <td>${(item.price * item.quantity).toFixed(2)}</td>
            <td><button onclick="removeFromCart('${item.id}')">Eliminar</button></td>
        `;
        cartTableBody.appendChild(row);
    });

    const totalRow = document.createElement('tr');
    totalRow.innerHTML = `
        <td colspan="3">Total</td>
        <td>${total.toFixed(2)}</td>
        <td></td>
    `;
    cartTableBody.appendChild(totalRow);

    // Actualizar el botón de PayPal
    renderPaypalButton(total);
}

// Función para eliminar productos del carrito
function removeFromCart(id) {
    const cartItemIndex = cart.findIndex(item => item.id === id);
    if (cartItemIndex > -1) {
        cart.splice(cartItemIndex, 1);
    }
    displayCart();
}

// Función para renderizar el botón de PayPal
function renderPaypalButton(total) {
    // Destruir el botón de PayPal si ya existe
    const paypalContainer = document.getElementById('paypal-button-container');
    paypalContainer.innerHTML = '';

    paypal.Buttons({
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: total.toFixed(2),
                        currency_code: 'CLP'
                    }
                }]
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                alert('Pago completado por ' + details.payer.name.given_name);
                cart.length = 0;
                displayCart();
            });
        }
    }).render('#paypal-button-container');
}

// Llamar a la función para obtener y mostrar los productos
fetchProducts();

