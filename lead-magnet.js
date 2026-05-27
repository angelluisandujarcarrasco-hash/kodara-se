/**
 * Lead Magnet Popup - Captura email + da código descuento 10%
 * Aparece a los 12 segundos o cuando intentan salir
 * No vuelve a aparecer en 7 días si ya cerró o se suscribió
 */
(function() {
  const KEY = 'kodara_lead_dismissed';
  const WEB3FORMS_KEY = '2e5a1c54-e4bf-41f4-b04c-7f4c30dace33';

  // No mostrar si ya cerró o se suscribió en últimos 7 días
  const dismissed = localStorage.getItem(KEY);
  if (dismissed && (Date.now() - parseInt(dismissed)) < 7 * 24 * 60 * 60 * 1000) return;

  // No mostrar en páginas de checkout/carrito/gracias
  const skipPages = ['/carrito.html', '/checkout.html', '/gracias.html', '/login.html', '/registro.html'];
  if (skipPages.some(p => location.pathname.endsWith(p))) return;

  const STYLE = `
.lm-backdrop{position:fixed;inset:0;background:rgba(6,11,24,0.78);backdrop-filter:blur(8px);z-index:99998;display:none;align-items:center;justify-content:center;padding:20px;animation:lmFade 0.3s ease}
.lm-backdrop.open{display:flex}
@keyframes lmFade{from{opacity:0}to{opacity:1}}
.lm-modal{background:linear-gradient(135deg,#FCF0DE,#FFF8EC);border:2px solid #C15431;border-radius:24px;padding:40px 32px;max-width:440px;width:100%;position:relative;box-shadow:0 25px 80px rgba(0,0,0,0.5);font-family:'Inter',sans-serif;animation:lmSlide 0.4s ease}
@keyframes lmSlide{from{opacity:0;transform:translateY(20px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
.lm-close{position:absolute;top:14px;right:14px;background:rgba(60,50,40,0.08);border:none;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:20px;color:#5C4E40;display:flex;align-items:center;justify-content:center;line-height:1}
.lm-close:hover{background:rgba(60,50,40,0.15)}
.lm-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(193,84,49,0.1);border:1.5px solid rgba(193,84,49,0.3);color:#C15431;font-size:11px;font-weight:700;padding:7px 14px;border-radius:999px;letter-spacing:2px;text-transform:uppercase;margin-bottom:18px}
.lm-badge::before{content:'❋';color:#B58850;font-size:13px}
.lm-title{font-family:'Playfair Display',Georgia,serif;font-size:32px;font-weight:700;color:#3C3228;line-height:1.15;margin-bottom:14px;letter-spacing:-0.5px}
.lm-title .grad{background:linear-gradient(135deg,#C15431,#B58850);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-style:italic}
.lm-sub{color:#5C4E40;font-size:14px;line-height:1.5;margin-bottom:22px}
.lm-form{display:flex;flex-direction:column;gap:10px}
.lm-input{background:#fff;border:1.5px solid rgba(60,50,40,0.18);color:#3C3228;font-size:15px;font-family:inherit;padding:14px 16px;border-radius:12px;outline:none;transition:border-color 0.2s}
.lm-input:focus{border-color:#C15431}
.lm-btn{background:#C15431;color:#fff;font-size:14px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:14px 20px;border-radius:12px;border:none;cursor:pointer;font-family:inherit;transition:all 0.2s;display:flex;align-items:center;justify-content:center;gap:8px}
.lm-btn:hover{background:#9B3F22;transform:translateY(-1px)}
.lm-btn:disabled{opacity:0.6;cursor:not-allowed}
.lm-disclaimer{font-size:11px;color:#8A7864;text-align:center;margin-top:10px;line-height:1.4}
.lm-success{text-align:center;padding:20px 0}
.lm-success-icon{font-size:48px;margin-bottom:14px}
.lm-success-title{font-family:'Playfair Display',Georgia,serif;font-size:26px;font-weight:700;color:#3C3228;margin-bottom:10px}
.lm-code{background:linear-gradient(135deg,#C15431,#B58850);color:#fff;font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:800;letter-spacing:4px;padding:14px 24px;border-radius:12px;display:inline-block;margin:18px 0;cursor:pointer;transition:transform 0.2s}
.lm-code:hover{transform:scale(1.05)}
.lm-code-hint{font-size:13px;color:#5C4E40;margin-top:8px}
@media(max-width:480px){.lm-modal{padding:32px 24px}.lm-title{font-size:26px}}
  `;

  const style = document.createElement('style');
  style.textContent = STYLE;
  document.head.appendChild(style);

  const modal = document.createElement('div');
  modal.className = 'lm-backdrop';
  modal.innerHTML = `
    <div class="lm-modal" role="dialog" aria-labelledby="lm-title">
      <button class="lm-close" aria-label="Cerrar">×</button>
      <div id="lm-content">
        <div class="lm-badge">Oferta exclusiva</div>
        <h2 id="lm-title" class="lm-title">10% de descuento en <span class="grad">tu primer pedido</span></h2>
        <p class="lm-sub">Suscríbete y obtén el código + acceso anticipado a nuevos productos, descuentos exclusivos y diseños limitados.</p>
        <form class="lm-form" id="lm-form">
          <input type="email" class="lm-input" id="lm-email" required placeholder="tu@email.com" autocomplete="email">
          <button type="submit" class="lm-btn" id="lm-submit">Quiero mi descuento →</button>
          <div class="lm-disclaimer">Sin spam. Cancela cuando quieras.</div>
        </form>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  const closeBtn = modal.querySelector('.lm-close');
  const form = modal.querySelector('#lm-form');
  const emailIn = modal.querySelector('#lm-email');
  const submitBtn = modal.querySelector('#lm-submit');
  const content = modal.querySelector('#lm-content');

  function close() {
    modal.classList.remove('open');
    localStorage.setItem(KEY, Date.now().toString());
  }
  function open() {
    if (modal.classList.contains('open')) return;
    modal.classList.add('open');
  }

  closeBtn.addEventListener('click', close);
  modal.addEventListener('click', e => { if (e.target === modal) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    const email = emailIn.value.trim();
    try {
      await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          access_key: WEB3FORMS_KEY,
          subject: '🎁 Nuevo suscriptor Kodarase (10% descuento)',
          from_name: 'Kodarase Lead Magnet',
          email: email,
          message: `Nuevo suscriptor a la lista: ${email}\nFuente: ${location.href}\nFecha: ${new Date().toISOString()}`,
        }),
      });
    } catch (err) {
      console.error('Lead magnet error:', err);
    }

    // Mostrar código aunque falle el submit (no bloquear UX)
    content.innerHTML = `
      <div class="lm-success">
        <div class="lm-success-icon">🎉</div>
        <div class="lm-success-title">¡Listo, ${email.split('@')[0]}!</div>
        <p class="lm-sub">Usa este código en checkout para tu 10% de descuento:</p>
        <div class="lm-code" id="lm-copy-code" title="Click para copiar">KODARASE10</div>
        <div class="lm-code-hint">👆 Click para copiar al portapapeles</div>
        <button class="lm-btn" id="lm-go" style="margin-top:18px">Ver productos ahora →</button>
      </div>
    `;
    localStorage.setItem(KEY, Date.now().toString());
    localStorage.setItem('kodara_lead_email', email);

    const code = content.querySelector('#lm-copy-code');
    code.addEventListener('click', () => {
      navigator.clipboard.writeText('KODARASE10');
      code.style.background = '#10B981';
      code.textContent = '¡COPIADO!';
      setTimeout(() => {
        code.style.background = 'linear-gradient(135deg,#C15431,#B58850)';
        code.textContent = 'KODARASE10';
      }, 1500);
    });
    content.querySelector('#lm-go').addEventListener('click', () => {
      location.href = 'servicio-kodara-print.html';
    });
  });

  // Trigger: 12 segundos o exit-intent (mouse arriba)
  let triggered = false;
  function trigger() {
    if (triggered) return;
    triggered = true;
    open();
  }
  setTimeout(trigger, 12000);
  document.addEventListener('mouseleave', e => {
    if (e.clientY < 0 && !triggered) trigger();
  });
})();
