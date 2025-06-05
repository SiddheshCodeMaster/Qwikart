const searchInput = document.getElementById('searchInput');
const container = document.getElementById('productsContainer');
let allProducts = [];

async function fetchProducts() {
    try {
        const response = await fetch('/get_all_products');
        const data = await response.json();
        const container = document.getElementById('productsContainer');
        container.innerHTML = ""; // Clear previous content

        for (const [name, details] of Object.entries(data.product_data)) {
            const card = document.createElement('div');
            card.className = 'product-card';

            card.innerHTML = `
                <h3>${name}</h3>
                <p><strong>Price:</strong> Rs.${details.Price}</p>
                <p><strong>Description:</strong> ${details.Description}</p>
                <p><strong>Category:</strong> ${details.Category}</p>
                <p>
                    ${
                        details.Quantity > 0
                            ? `<strong>In Stock</strong>`
                            : '<strong style="color: red;">Out of Stock</strong>'
                    }
                </p>
            `;

            container.appendChild(card);
        }
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

fetchProducts();

function renderProducts(products) {
  container.innerHTML = ''; // Clear existing
  products.forEach(([name, info]) => {
    const card = document.createElement('div');
    card.classList.add('product-card');
    card.innerHTML = `
      <h3>${name}</h3>
      <p><strong>Price:</strong> Rs.${info.Price}</p>
      <p><strong>Category:</strong> ${info.Category}</p>
      <p>${info.Description}</p>
      <p>
        ${
          info.Quantity > 0
            ? `<strong>In Stock</strong>`
            : '<strong style="color: red;">Out of Stock</strong>'
        }
      </p>
    `;
    container.appendChild(card);
  });
}

// Filter on input
searchInput.addEventListener('input', () => {
  console.log('Entered Searching')
  const query = searchInput.value.toLowerCase();
  const filtered = allProducts.filter(([name, info]) =>
    name.toLowerCase().includes(query) ||
    (info.Description && info.Description.toLowerCase().includes(query))
  );

  console.log('Filtered Products: ' || filtered);
  renderProducts(filtered);
});
