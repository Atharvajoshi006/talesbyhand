/* =====================
   script.js - safe & robust
   ===================== */

/* ---- Utilities ---- */
const qs = (s, ctx = document) => ctx.querySelector(s);
const qsa = (s, ctx = document) => Array.from(ctx.querySelectorAll(s));

/* ---- Fade-in on scroll (works across pages) ---- */
function handleScrollFade() {
  const items = qsa('.fade-in, .fade-up, .product-card, .about, .cart, .hero h2, .hero p');
  const windowH = window.innerHeight;
  items.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < windowH - 100) {
      el.classList.add('visible');
    }
  });
}
window.addEventListener('scroll', handleScrollFade);
window.addEventListener('load', handleScrollFade);

/* ---- Product filters (only if filter buttons exist) ---- */
const filterButtons = qsa('.filter-btn');
const productCards = qsa('.product-card');

if (filterButtons.length > 0 && productCards.length > 0) {
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const state = btn.dataset.state || btn.getAttribute('data-state');

      // visual active class
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // show/hide cards
      productCards.forEach(card => {
        if (state === 'all' || card.dataset.state === state) {
          card.classList.remove('hidden');
          // trigger fade-in visible (in case)
          setTimeout(() => card.classList.add('visible'), 30);
        } else {
          card.classList.add('hidden');
          card.classList.remove('visible');
        }
      });
    });
  });
}

/* ---- Cart: store in localStorage under key "cart" ---- */
function getCart() {
  try {
    return JSON.parse(localStorage.getItem('cart')) || [];
  } catch (e) {
    return [];
  }
}
function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

/* Add-to-cart buttons (if present on page) */
qsa('.add-cart-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    // attempt to read data attributes for product name/price, fallback to text
    const card = e.currentTarget.closest('.product-card');
    const name = (card && (card.dataset.name || qs('h4', card)?.innerText || qs('h3', card)?.innerText)) || 'Product';
    const priceText = (card && (card.dataset.price || qs('.price', card)?.innerText)) || '';
    // try to parse price number
    let price = 0;
    if (priceText) {
      const num = priceText.replace(/[^0-9.]/g, '');
      price = parseFloat(num) || 0;
    }

    const cart = getCart();
    cart.push({ name, price });
    saveCart(cart);

    // small button feedback
    btn.classList.add('clicked');
    setTimeout(() => btn.classList.remove('clicked'), 250);

    // optional: small toast or alert
    if (typeof window.alert === 'function') {
      alert(`🧺 "${name}" added to cart`);
    }
  });
});

/* ---- Cart page rendering & remove button ---- */
function renderCartPage() {
  const container = qs('#cartContainer');
  const summary = qs('#cartSummary');
  if (!container) return; // not on cart page

  const cart = getCart();
  container.innerHTML = '';

  if (cart.length === 0) {
    container.innerHTML = '<p>Your cart is empty.</p>';
    summary.innerHTML = '';
    return;
  }

  let total = 0;
  cart.forEach((item, idx) => {
    total += Number(item.price || 0);
    const itemEl = document.createElement('div');
    itemEl.className = 'cart-item';
    itemEl.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;">
        <div>
          <strong>${item.name}</strong><br>
          <small style="color:#6d5648">₹${Number(item.price || 0).toFixed(2)}</small>
        </div>
        <div>
          <button class="remove-item-btn" data-index="${idx}" style="background:#c64b2e;color:#fff;border-radius:8px;padding:6px 10px;border:none;cursor:pointer">Remove</button>
        </div>
      </div>
    `;
    container.appendChild(itemEl);
  });

  summary.innerHTML = `
    <p style="margin-top:1rem;font-weight:600">Total: ₹${total.toFixed(2)}</p>
    <div style="margin-top:0.6rem;">
      <button id="checkoutBtn" style="background:#8b5e3c;color:#fff;padding:8px 14px;border-radius:12px;border:none;cursor:pointer">Checkout</button>
    </div>
  `;

  // attach remove handlers
  qsa('.remove-item-btn', container).forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = Number(e.currentTarget.dataset.index);
      let c = getCart();
      c.splice(idx, 1);
      saveCart(c);
      renderCartPage(); // re-render
    });
  });

  // checkout click (demo only)
  const checkoutBtn = qs('#checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      alert('This demo does not process payments. Implement checkout backend to complete purchase.');
    });
  }
}

// call once at load (in case we're on cart page)
window.addEventListener('load', renderCartPage);
