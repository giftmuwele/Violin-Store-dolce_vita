document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
});

const API_URL = "http://127.0.0.1:5000/api";

async function loadProducts() {
    try {
        const res = await fetch(`${API_URL}/products`);
        const products = await res.json();

        const container = document.querySelector(".product-grid");

        if (!container) return; // Only runs on product pages

        container.innerHTML = "";

        products.forEach(product => {
            container.innerHTML += `
                <div class="product-card">
                    <img src="${product.image_url}" alt="${product.name}" />
                    <h3>${product.name}</h3>
                    <p class="price">K ${product.price}</p>
                    <button onclick="addToCart(${product.id})">
                        Add to Cart 🛒
                    </button>
                </div>
            `;
        });

    } catch (error) {
        console.error("Error loading products:", error);
    }
}
