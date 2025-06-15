document.addEventListener('DOMContentLoaded', () => {
  const menuItems = document.querySelectorAll('.menu-item');

  menuItems.forEach(item => {
    const link = item.querySelector('a');
    const submenu = item.querySelector('.submenu');
    link.addEventListener('click', e => {
      e.preventDefault();
      menuItems.forEach(m => m.querySelector('a').classList.remove('active'));
      link.classList.add('active');
      if (submenu) submenu.classList.toggle('active');
    });
  });

  const products = [
    {
      name: 'Classic Violin',
      category: 'Violins',
      price: 1500,
      image: 'Images\Violin.png'
    },
    {
      name: 'Professional Bow',
      category: 'Bows',
      price: 500,
      image: 'Images\Bow.jpg'
    }
  ];

  function renderProducts(productList) {
    const productGrid = document.querySelector('.product-grid');
    productGrid.innerHTML = '';
    productList.forEach(product => {
      const productCard = document.createElement('div');
      productCard.classList.add('product-card');
      productCard.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <div class="product-details">
          <h3>${product.name}</h3>
          <p>${product.category}</p>
          <p>$${product.price}</p>
          <button>Add to Cart</button>
        </div>
      `;
      productGrid.appendChild(productCard);
    });
  }

  renderProducts(products);

  // Theme toggle with icon switching
  const themeToggle = document.querySelector('#theme-toggle');
  const icon = themeToggle.querySelector('i');

  function updateIcon() {
    if (document.body.classList.contains('light-mode')) {
      icon.classList.remove('fa-lightbulb');
      icon.classList.add('fa-sun');
    } else {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-lightbulb');
    }
  }

  themeToggle?.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    updateIcon();
  });

  // Initialize icon on load
  updateIcon();
});
