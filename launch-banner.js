/**
 * Launch Banner sticky — 20% OFF LANZAMIENTO20
 * Aparece en TODAS las páginas, sticky top, con botón cerrar.
 * Se recuerda dismissed con localStorage (24h).
 */

/* ── Carga el sistema de idiomas (inglés por defecto + botón ES/EN) en todas las páginas ── */
(function loadI18n() {
  var V = '20260614c'; // versión: súbela al actualizar el idioma para evitar caché
  function add(src, cb) {
    if (document.querySelector('script[data-kd-i18n="' + src + '"]')) { if (cb) cb(); return; }
    var s = document.createElement('script');
    s.src = src + '?v=' + V;
    s.setAttribute('data-kd-i18n', src);
    if (cb) s.onload = cb;
    (document.head || document.documentElement).appendChild(s);
  }
  // primero el diccionario, luego la engine
  add('i18n-dict.js', function () { add('i18n.js'); });
})();

(function() {
  const KEY = 'kodara_launch_banner_dismissed';
  const dismissed = localStorage.getItem(KEY);
  if (dismissed && (Date.now() - parseInt(dismissed)) < 24 * 60 * 60 * 1000) return;

  const STYLE = `
.kd-launch-banner{position:fixed;top:0;left:0;right:0;z-index:99997;background:linear-gradient(135deg,#C15431,#B58850);color:#fff;text-align:center;padding:10px 44px 10px 16px;font-family:'Inter',system-ui,sans-serif;font-size:13.5px;font-weight:600;letter-spacing:0.2px;line-height:1.4;box-shadow:0 2px 12px rgba(0,0,0,0.15);animation:kdSlideDown 0.4s ease}
@keyframes kdSlideDown{from{transform:translateY(-100%)}to{transform:translateY(0)}}
.kd-launch-banner strong{font-weight:800;background:rgba(255,255,255,0.22);padding:3px 10px;border-radius:6px;font-family:'JetBrains Mono','Courier New',monospace;letter-spacing:1px;margin:0 4px;display:inline-block}
.kd-launch-banner a{color:#fff;text-decoration:underline;font-weight:700}
.kd-launch-close{position:absolute;top:50%;right:10px;transform:translateY(-50%);background:rgba(255,255,255,0.18);border:none;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:18px;color:#fff;display:flex;align-items:center;justify-content:center;line-height:1;padding:0;transition:background 0.2s}
.kd-launch-close:hover{background:rgba(255,255,255,0.32)}
body{padding-top:42px !important}
/* Empujar topnav/navbar sticky para que NO queden tapados por el banner */
nav.topnav, .topnav, .nav-bar, header.sticky, .nav.sticky{top:42px !important}
@media(max-width:600px){
  .kd-launch-banner{font-size:11.5px;padding:8px 36px 8px 12px;line-height:1.3}
  .kd-launch-banner strong{padding:2px 7px;margin:0 2px}
  body{padding-top:50px !important}
  nav.topnav, .topnav, .nav-bar, header.sticky, .nav.sticky{top:50px !important}
}
@media(max-width:380px){
  .kd-launch-banner{font-size:10.5px}
}
  `;

  const style = document.createElement('style');
  style.textContent = STYLE;
  document.head.appendChild(style);

  const banner = document.createElement('div');
  banner.className = 'kd-launch-banner';
  banner.setAttribute('role', 'banner');
  banner.innerHTML = `
    🎉 LANZAMIENTO: usa el código <strong>LANZAMIENTO20</strong> y recibe 20% OFF en tu primer pedido · Solo primeros 20 clientes
    <button class="kd-launch-close" aria-label="Cerrar banner">×</button>
  `;

  // Insertar al inicio del body
  if (document.body) {
    document.body.insertBefore(banner, document.body.firstChild);
  } else {
    document.addEventListener('DOMContentLoaded', () => {
      document.body.insertBefore(banner, document.body.firstChild);
    });
  }

  banner.querySelector('.kd-launch-close').addEventListener('click', () => {
    banner.style.animation = 'kdSlideUp 0.3s ease forwards';
    const upStyle = document.createElement('style');
    upStyle.textContent = `@keyframes kdSlideUp{to{transform:translateY(-100%);opacity:0}}
body{padding-top:0 !important}
nav.topnav, .topnav, .nav-bar, header.sticky, .nav.sticky{top:0 !important}`;
    document.head.appendChild(upStyle);
    setTimeout(() => {
      banner.remove();
    }, 300);
    localStorage.setItem(KEY, Date.now().toString());
  });
})();
