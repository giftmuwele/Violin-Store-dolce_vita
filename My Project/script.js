let cart = [];

// Add to Cart Function
function addToCart(product) {
  cart.push(product);
  updateCartCount();
  console.log('Added to Cart:', product);
}

// Update Cart Count
function updateCartCount() {
  const cartCount = document.getElementById('cart-count');
  cartCount.textContent = cart.length;
}

// Search Functionality
document.getElementById('search-form').addEventListener('submit', function (e) {
  e.preventDefault();
  const query = document.querySelector('input[name="query"]').value;
  console.log('Searching for:', query);
  // Implement search logic (e.g., filter products or redirect to search results page)
});