const searchInput = document.querySelector('#search-input');
const productListss = document.querySelector('#product-list');

searchInput.addEventListener('keyup', function(event) {
  const searchQuery = event.target.value.toLowerCase();
  const products = productListss.querySelectorAll('.product');

  products.forEach(function(product) {
    const productName = product.querySelector('.product-title a').textContent.toLowerCase();
    
    if (productName.includes(searchQuery)) {
      product.style.display = 'block';
    } else {
      product.style.display = 'none';
    }
  });
});



