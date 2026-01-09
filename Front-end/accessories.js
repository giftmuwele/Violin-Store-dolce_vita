// Category Filter Functionality
const filterButtons = document.querySelectorAll('.filter-btn');
const productCards = document.querySelectorAll('.product-card');

filterButtons.forEach(button => {
  button.addEventListener('click', function() {
    // Remove active class from all buttons
    filterButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    this.classList.add('active');
    
    // Get the category to filter
    const category = this.getAttribute('data-category');
    
    // Filter products
    productCards.forEach(card => {
      if (category === 'all') {
        card.style.display = 'block';
        // Add animation
        card.style.animation = 'fadeIn 0.5s ease';
      } else {
        if (card.getAttribute('data-category') === category) {
          card.style.display = 'block';
          card.style.animation = 'fadeIn 0.5s ease';
        } else {
          card.style.display = 'none';
        }
      }
    });
  });
});

// Add to Cart Functionality
const addToCartButtons = document.querySelectorAll('.add-to-cart');
const cartBadge = document.querySelector('.cart-btn .badge');

let cartCount = parseInt(cartBadge.textContent);

addToCartButtons.forEach(button => {
  button.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Get product info
    const productCard = this.closest('.product-card');
    const productName = productCard.querySelector('h3').textContent;
    const productPrice = productCard.querySelector('.price').textContent;
    
    // Increment cart count
    cartCount++;
    cartBadge.textContent = cartCount;
    
    // Button feedback
    const originalText = this.textContent;
    this.textContent = '✓ Added!';
    this.style.background = 'linear-gradient(135deg, #25D366 0%, #128C7E 100%)';
    
    // Reset button after 2 seconds
    setTimeout(() => {
      this.textContent = originalText;
      this.style.background = 'linear-gradient(135deg, #d97038 0%, #c05f2a 100%)';
    }, 2000);
    
    // Show notification
    showNotification(`${productName} added to cart!`);
    
    // Log to console (you can replace this with actual cart logic)
    console.log('Added to cart:', {
      name: productName,
      price: productPrice
    });
  });
});

// Notification Function
function showNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
    z-index: 1000;
    animation: slideIn 0.3s ease;
    font-weight: 600;
  `;
  
  document.body.appendChild(notification);
  
  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

// Search Functionality
const searchInput = document.getElementById('searchInput');

searchInput.addEventListener('input', function(e) {
  const searchTerm = e.target.value.toLowerCase();
  
  productCards.forEach(card => {
    const productName = card.querySelector('h3').textContent.toLowerCase();
    const productDesc = card.querySelector('.product-desc').textContent.toLowerCase();
    
    if (productName.includes(searchTerm) || productDesc.includes(searchTerm)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
  
  // If search is empty, show all products
  if (searchTerm === '') {
    const activeFilter = document.querySelector('.filter-btn.active');
    const activeCategory = activeFilter.getAttribute('data-category');
    
    productCards.forEach(card => {
      if (activeCategory === 'all') {
        card.style.display = 'block';
      } else {
        if (card.getAttribute('data-category') === activeCategory) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      }
    });
  }
});

// Sort Functionality
const sortDropdown = document.querySelector('.sort-dropdown');

sortDropdown.addEventListener('change', function() {
  const sortValue = this.value;
  const productsGrid = document.getElementById('productsGrid');
  const productsArray = Array.from(productCards);
  
  productsArray.sort((a, b) => {
    if (sortValue.includes('Price - Low to High')) {
      const priceA = parseFloat(a.querySelector('.price').textContent.replace('ZMW ', ''));
      const priceB = parseFloat(b.querySelector('.price').textContent.replace('ZMW ', ''));
      return priceA - priceB;
    } else if (sortValue.includes('Price - High to Low')) {
      const priceA = parseFloat(a.querySelector('.price').textContent.replace('ZMW ', ''));
      const priceB = parseFloat(b.querySelector('.price').textContent.replace('ZMW ', ''));
      return priceB - priceA;
    } else if (sortValue.includes('Name A-Z')) {
      const nameA = a.querySelector('h3').textContent;
      const nameB = b.querySelector('h3').textContent;
      return nameA.localeCompare(nameB);
    }
    return 0;
  });
  
  // Re-append sorted products
  productsArray.forEach(product => {
    productsGrid.appendChild(product);
  });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

console.log('Accessories page loaded successfully!');