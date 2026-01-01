// Category switching functionality
const categories = document.querySelectorAll('.category');
categories.forEach(cat => {
  cat.addEventListener('click', function() {
    // Remove active class from all categories
    categories.forEach(c => c.classList.remove('active'));
    // Add active class to clicked category
    this.classList.add('active');
    console.log('Selected category:', this.dataset.category);
  });
});

// Search functionality
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', function(e) {
  console.log('Searching for:', e.target.value);
  // Add your search logic here
});

// Order button functionality
const orderBtn = document.querySelector('.order-btn');
orderBtn.addEventListener('click', function() {
  alert('Order functionality coming soon!');
  // Add your order logic here
});

// Navigation items functionality
const navItems = document.querySelectorAll('.nav-item');
navItems.forEach(item => {
  item.addEventListener('click', function() {
    console.log('Clicked:', this.textContent.trim());
    // Add your navigation logic here
  });
});

// Cart button functionality
const cartBtn = document.querySelector('.cart-btn');
cartBtn.addEventListener('click', function() {
  alert('Cart functionality coming soon!');
  // Add your cart logic here
});

// Wishlist button functionality
const wishlistBtn = document.querySelector('.icon-btn');
wishlistBtn.addEventListener('click', function() {
  console.log('Wishlist clicked');
  // Add your wishlist logic here
});