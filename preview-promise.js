/**
 * Preview Promise — "Te enviamos vista previa antes de imprimir"
 * Se inyecta automáticamente en CUALQUIER página de pedido que tenga
 * un botón .submit-btn. Centralizado: cambia el texto aquí una vez y
 * se actualiza en TODOS los productos (actuales y futuros).
 */
(function(){
  // Evitar duplicados
  if (document.querySelector('.kd-preview-promise')) return;

  const btn = document.querySelector('.submit-btn');
  if (!btn) return; // solo en páginas de pedido

  const box = document.createElement('div');
  box.className = 'kd-preview-promise';
  box.style.cssText = 'display:flex;align-items:center;gap:14px;background:rgba(212,169,119,0.12);border:1px solid var(--gold,#D4A977);border-radius:14px;padding:16px 20px;margin-bottom:18px';
  box.innerHTML = `
    <span style="font-size:30px;flex-shrink:0">👁️</span>
    <div style="font-size:13.5px;line-height:1.5;color:var(--text-2,#5C4E40)">
      <strong style="color:var(--gold-dark,#B58850);display:block;margin-bottom:2px">Vista previa antes de imprimir</strong>
      Antes de producir tu pedido te enviamos una imagen de cómo quedará para que la apruebes. Solo lo imprimimos cuando estés 100% feliz. 💛
    </div>
  `;

  // Insertar justo antes del botón de compra (o del form-alert si existe)
  const alert = document.querySelector('.form-alert');
  const ref = alert || btn;
  ref.parentNode.insertBefore(box, ref);
})();
