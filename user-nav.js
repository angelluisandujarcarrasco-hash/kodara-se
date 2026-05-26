// User nav widget - se inyecta en topnav de cualquier página
// Muestra "Iniciar sesión" si no logged in, o avatar + dropdown si logged in

import { onUserChange, signOut } from './auth.js';

const STYLE = `
.user-nav{display:inline-flex;align-items:center;gap:8px;position:relative}
.user-nav-btn{background:transparent;border:1px solid rgba(255,255,255,0.12);color:rgba(255,255,255,0.85);font-size:13px;padding:8px 16px;border-radius:999px;font-weight:600;cursor:pointer;font-family:inherit;transition:all 0.2s;text-decoration:none;display:inline-flex;align-items:center;gap:8px}
.user-nav-btn:hover{border-color:#F97316;color:#F97316}
.user-nav-btn.primary{background:linear-gradient(135deg,#F97316,#EC4899);border:none;color:#fff}
.user-nav-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#F97316,#EC4899);display:inline-flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:#fff;cursor:pointer;border:none;overflow:hidden;font-family:inherit}
.user-nav-avatar img{width:100%;height:100%;object-fit:cover}
.user-nav-menu{position:absolute;top:calc(100% + 8px);right:0;background:#0F1A2E;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:8px;min-width:200px;box-shadow:0 16px 40px rgba(0,0,0,0.4);display:none;z-index:200}
.user-nav-menu.open{display:block}
.user-nav-menu a, .user-nav-menu button{display:block;width:100%;padding:10px 14px;border-radius:8px;color:rgba(255,255,255,0.85);font-size:14px;text-decoration:none;background:transparent;border:none;cursor:pointer;font-family:inherit;font-weight:600;text-align:left}
.user-nav-menu a:hover, .user-nav-menu button:hover{background:rgba(255,255,255,0.06);color:#F97316}
.user-nav-menu .menu-info{padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:6px}
.user-nav-menu .menu-name{font-size:13px;font-weight:700;color:#fff}
.user-nav-menu .menu-email{font-size:11px;color:#6B7689}
`;

function injectStyle() {
  if (document.getElementById('user-nav-style')) return;
  const s = document.createElement('style');
  s.id = 'user-nav-style';
  s.textContent = STYLE;
  document.head.appendChild(s);
}

// Encuentra el contenedor del nav. Busca por orden:
function findSlot() {
  return document.getElementById('user-nav-slot')
    || document.querySelector('.topnav-actions')
    || document.querySelector('.nav-right')
    || (() => {
      const topnav = document.querySelector('.topnav') || document.querySelector('#nav') || document.querySelector('nav');
      if (!topnav) return null;
      const slot = document.createElement('div');
      slot.style.cssText = 'display:flex;gap:10px;align-items:center';
      topnav.appendChild(slot);
      return slot;
    })();
}

function renderLoggedOut(slot) {
  slot.innerHTML = `
    <a href="login.html" class="user-nav-btn">Iniciar sesión</a>
    <a href="registro.html" class="user-nav-btn primary">Crear cuenta</a>
  `;
}

function renderLoggedIn(slot, user) {
  const initial = (user.displayName || user.email).charAt(0).toUpperCase();
  const avatar = user.photoURL
    ? `<img src="${user.photoURL}" alt="">`
    : initial;
  slot.innerHTML = `
    <div class="user-nav">
      <button class="user-nav-avatar" id="un-avatar-btn" aria-label="Menú de cuenta">${avatar}</button>
      <div class="user-nav-menu" id="un-menu">
        <div class="menu-info">
          <div class="menu-name">${escapeHtml(user.displayName || 'Usuario')}</div>
          <div class="menu-email">${escapeHtml(user.email)}</div>
        </div>
        <a href="mi-cuenta.html">👤 Mi perfil</a>
        <a href="mi-cuenta.html#pedidos">📦 Mis pedidos</a>
        <a href="mi-cuenta.html#direcciones">📍 Mis direcciones</a>
        <a href="mi-cuenta.html#descuentos">💎 Mis descuentos</a>
        <button id="un-logout">🚪 Cerrar sesión</button>
      </div>
    </div>
  `;
  const btn = slot.querySelector('#un-avatar-btn');
  const menu = slot.querySelector('#un-menu');
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    menu.classList.toggle('open');
  });
  document.addEventListener('click', () => menu.classList.remove('open'));
  slot.querySelector('#un-logout').addEventListener('click', async () => {
    await signOut();
    location.reload();
  });
}

function escapeHtml(s) {
  return String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
}

// INIT
(function() {
  injectStyle();
  const slot = findSlot();
  if (!slot) return;

  // Si el slot ya tiene contenido (botones existentes), creamos un sub-contenedor
  let userSlot = slot.querySelector('.user-nav-injected');
  if (!userSlot) {
    userSlot = document.createElement('div');
    userSlot.className = 'user-nav-injected';
    userSlot.style.cssText = 'display:flex;gap:8px;align-items:center';
    slot.appendChild(userSlot);
  }

  onUserChange(user => {
    if (user) renderLoggedIn(userSlot, user);
    else renderLoggedOut(userSlot);
  });
})();
