const API_URL = "http://127.0.0.1:5000/api";

async function addToCart(productId) {

    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first.");
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch(`${API_URL}/cart/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": token
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        const data = await res.json();

        if (res.ok) {
            alert("Added to cart!");
            loadCartCount();
        } else {
            alert(data.error || "Error adding to cart");
        }

    } catch (error) {
        console.error("Cart error:", error);
    }
}


async function loadCartCount() {

    const token = localStorage.getItem("token");
    if (!token) return;

    try {
        const res = await fetch(`${API_URL}/cart`, {
            headers: {
                "Authorization": token
            }
        });

        const data = await res.json();

        const badge = document.querySelector(".badge");
        if (badge) {
            badge.innerText = data.total_items || 0;
        }

    } catch (error) {
        console.error("Cart count error:", error);
    }
}

document.addEventListener("DOMContentLoaded", loadCartCount);
