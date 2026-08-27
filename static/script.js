function updatePrice() {

    const product = document.getElementById("product");
    const selected = product.options[product.selectedIndex];

    const price = selected.dataset.price || 0;

    document.getElementById("price").textContent = price;

    calculateTotal();
}


function calculateTotal() {

    const product = document.getElementById("product");
    const selected = product.options[product.selectedIndex];

    const price = parseFloat(selected.dataset.price || 0);

    const quantity =
        parseInt(document.getElementById("quantity").value) || 0;

    const total = price * quantity;

    document.getElementById("total").textContent =
        total.toFixed(2);
}

