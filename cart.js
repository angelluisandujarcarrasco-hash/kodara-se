/**
 * Carrito de Kodara Print Studio
 * Logica compartida que usa localStorage
 */

const KODARA_CART_KEY = 'kodara_cart_v1';

// ========== STORAGE ==========
function getCart() {
  try {
    const raw = localStorage.getItem(KODARA_CART_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error('Cart parse error:', e);
    return [];
  }
}

function saveCart(items) {
  localStorage.setItem(KODARA_CART_KEY, JSON.stringify(items));
  updateCartBadge();
  document.dispatchEvent(new CustomEvent('kodara-cart-updated', { detail: items }));
}

function clearCart() {
  localStorage.removeItem(KODARA_CART_KEY);
  updateCartBadge();
  document.dispatchEvent(new CustomEvent('kodara-cart-updated', { detail: [] }));
}

// ========== OPERATIONS ==========
function addToCart(item) {
  const items = getCart();
  // Cada item tiene un ID unico
  item.id = 'item-' + Date.now() + '-' + Math.floor(Math.random() * 9999);
  item.added_at = new Date().toISOString();
  if (!item.cantidad) item.cantidad = 1;
  items.push(item);
  saveCart(items);
  return item.id;
}

function updateQuantity(itemId, cantidad) {
  const items = getCart();
  const item = items.find(i => i.id === itemId);
  if (item) {
    item.cantidad = Math.max(1, parseInt(cantidad) || 1);
    saveCart(items);
  }
}

function removeFromCart(itemId) {
  const items = getCart().filter(i => i.id !== itemId);
  saveCart(items);
}

function getCartTotal() {
  return getCart().reduce((sum, i) => sum + (parseFloat(i.precio_num || 0) * (i.cantidad || 1)), 0);
}

function getCartCount() {
  return getCart().reduce((sum, i) => sum + (i.cantidad || 1), 0);
}

// ========== UI HELPERS ==========
function updateCartBadge() {
  const badges = document.querySelectorAll('.cart-badge');
  const count = getCartCount();
  badges.forEach(b => {
    b.textContent = count;
    b.style.display = count > 0 ? 'flex' : 'none';
  });
}

// Inyecta el icono carrito en el topnav (si hay) Y un boton flotante siempre visible
function injectCartIcon() {
  // 1. Inyectar en topnav si existe
  const nav = document.querySelector('.topnav');
  if (nav && !nav.querySelector('.cart-icon')) {
    const backBtn = nav.querySelector('.topnav-back');
    const cartHTML = `
      <a href="carrito.html" class="cart-icon" title="Ver carrito" aria-label="Ver carrito">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
        <span class="cart-badge">0</span>
      </a>
    `;
    if (backBtn) {
      backBtn.insertAdjacentHTML('beforebegin', cartHTML);
    } else {
      nav.insertAdjacentHTML('beforeend', cartHTML);
    }
  }

  // 2. Inyectar el FAB (Floating Action Button) en bottom-right — siempre visible
  if (!document.querySelector('.cart-fab')) {
    const fabHTML = `
      <a href="carrito.html" class="cart-fab" title="Ver carrito" aria-label="Ver carrito">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
        <span class="cart-badge cart-fab-badge">0</span>
      </a>
    `;
    document.body.insertAdjacentHTML('beforeend', fabHTML);
  }

  updateCartBadge();
}

// ========== STYLES (auto-inyecta CSS) ==========
function injectCartStyles() {
  if (document.getElementById('kodara-cart-styles')) return;
  const style = document.createElement('style');
  style.id = 'kodara-cart-styles';
  style.textContent = `
    .cart-icon {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border: 1px solid rgba(255,255,255,0.1);
      color: #B8C0D0;
      border-radius: 10px;
      transition: all 0.2s;
      text-decoration: none;
    }
    .cart-icon:hover {
      border-color: #F97316;
      color: #F97316;
      transform: translateY(-1px);
    }
    .cart-badge {
      position: absolute;
      top: -6px;
      right: -6px;
      min-width: 20px;
      height: 20px;
      padding: 0 5px;
      background: linear-gradient(135deg, #F97316, #EC4899);
      color: #fff;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      display: none;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(249,115,22,0.4);
    }
    /* Floating action button - siempre visible en bottom-right */
    .cart-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9998;
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #F97316, #EC4899);
      color: #fff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      box-shadow: 0 8px 32px rgba(249,115,22,0.5), 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .cart-fab:hover {
      transform: translateY(-3px) scale(1.05);
      box-shadow: 0 14px 40px rgba(249,115,22,0.6), 0 6px 16px rgba(0,0,0,0.4);
    }
    .cart-fab:active {
      transform: scale(0.95);
    }
    .cart-fab .cart-badge {
      top: -2px;
      right: -2px;
      min-width: 24px;
      height: 24px;
      font-size: 12px;
      background: #fff;
      color: #F97316;
      border: 2px solid #F97316;
    }
    @media(max-width:640px){
      .cart-fab{bottom:18px;right:18px;width:54px;height:54px}
    }
    /* Toast notification */
    .cart-toast {
      position: fixed;
      top: 80px;
      right: 20px;
      z-index: 9999;
      background: linear-gradient(135deg, #10B981, #059669);
      color: #fff;
      padding: 14px 22px;
      border-radius: 14px;
      font-weight: 700;
      font-size: 14px;
      box-shadow: 0 10px 40px rgba(16,185,129,0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      transform: translateY(-150px);
      opacity: 0;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .cart-toast.show {
      transform: translateY(0);
      opacity: 1;
    }
    .cart-toast a {
      color: #fff;
      text-decoration: underline;
      font-weight: 800;
    }
  `;
  document.head.appendChild(style);
}

function showCartToast(message, linkText, linkHref) {
  injectCartStyles();
  // Quitar toast previo si existe
  document.querySelectorAll('.cart-toast').forEach(t => t.remove());

  const toast = document.createElement('div');
  toast.className = 'cart-toast';
  toast.innerHTML = `
    <span>✓</span>
    <span>${message}</span>
    ${linkHref ? `<a href="${linkHref}">${linkText || 'Ver carrito'}</a>` : ''}
  `;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 500);
  }, 4500);
}

// ========== AUTO-INIT ==========
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    injectCartStyles();
    injectCartIcon();
    updateCartBadge();
  });
} else {
  injectCartStyles();
  injectCartIcon();
  updateCartBadge();
}
