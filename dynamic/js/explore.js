const searchInput = document.getElementById('searchInput');
const container = document.getElementById('productsContainer');
let allProducts = [];

async function fetchProducts() {
    try {
        const response = await fetch('/get_all_products');
        const data = await response.json();
        // Populate allProducts as an array of [name, details] pairs
        allProducts = Object.entries(data.product_data);

        renderProducts(allProducts); // Render all products initially
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

fetchProducts();

function renderProducts(products) {
    container.innerHTML = '';
    const fragment = document.createDocumentFragment();
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
        fragment.appendChild(card);
    });
    container.appendChild(fragment);
}

// Debounce utility
function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

function handleSearch() {
    const query = searchInput.value.toLowerCase();
    let filtered;
    if (query === "") {
        // Show all products (including out of stock) when search is empty
        filtered = allProducts;
    } else {
        // Show all matching products (including out of stock)
        filtered = allProducts.filter(([name, info]) =>
            name.toLowerCase().includes(query) ||
            (info.Category && info.Category.toLowerCase().includes(query))
        );
    }
    renderProducts(filtered);
}

searchInput.addEventListener('input', debounce(handleSearch, 200));