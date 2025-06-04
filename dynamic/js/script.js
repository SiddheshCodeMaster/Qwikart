const searchInput = document.getElementById('searchInput');
const container = document.getElementById('productsContainer');
let allProducts = [];

// Dynamic Text and Quotes Arrays
const phrases = [
    "The world of amazing deals!",
    "Your one-stop shop!",
    "Shopping made simple and fun!",
    "Discover something new today!"
];

const quotes = [
    "Success is 100% fulfillment delivered on time.",
    "Just-In-Time is not a principle; it’s our promise.",
    "Fast, reliable, and always on time—that’s QwiKart!",
    "Every second saved is a smile earned.",
    "Fulfillment isn’t a goal; it’s a guarantee."
];

// DOM Elements
const dynamicText = document.querySelector('.dynamic-text');
const quoteText = document.querySelector('.quote-text');

let phraseIndex = 0;
let quoteIndex = 0;

// Function to Change Phrases
function changePhrase() {
    dynamicText.textContent = phrases[phraseIndex];
    phraseIndex = (phraseIndex + 1) % phrases.length;
}

// Function to Change Quotes
function changeQuote() {
    quoteText.textContent = quotes[quoteIndex];
    quoteIndex = (quoteIndex + 1) % quotes.length;
}

// Set Intervals for Dynamic Updates
setInterval(changePhrase, 3000); // Change phrase every 3 seconds
setInterval(changeQuote, 5000);  // Change quote every 5 seconds

// Initialize First Values
changePhrase();
changeQuote();

// Fetch all products on load
fetch('/get_all_products')
  .then(response => response.json())
  .then(data => {
    allProducts = Object.entries(data.product_data); // [[productName, productInfo], ...]
    renderProducts(allProducts);
  });

function renderProducts(products) {
  container.innerHTML = ''; // Clear existing
  products.forEach(([name, info]) => {
    const card = document.createElement('div');
    card.classList.add('product-card');
    card.innerHTML = `
      <h3>${name}</h3>
      <p><strong>Price:</strong> ₹${info.Price}</p>
      <p><strong>Category:</strong> ${info.Category}</p>
      <p>${info.Description}</p>
    `;
    container.appendChild(card);
  });
}

// Filter on input
searchInput.addEventListener('input', () => {
  const query = searchInput.value.toLowerCase();
  const filtered = allProducts.filter(([name, info]) => 
    name.toLowerCase().includes(query) ||
    info.Description.toLowerCase().includes(query)
  );
  renderProducts(filtered);
});
