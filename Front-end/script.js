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
  const toggle = document.getElementById('theme-toggle');
const icon = document.getElementById('theme-icon');

toggle.addEventListener('click', () => {
  document.body.classList.toggle('light-mode');
  icon.classList.toggle('fa-sun');
  icon.classList.toggle('fa-lightbulb');

  });

  // Initialize icon on load
  updateIcon();
});
