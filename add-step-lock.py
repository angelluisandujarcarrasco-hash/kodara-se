"""
Implementa un wizard secuencial en TODAS las paginas de pedido.
Cada paso se desbloquea solo cuando se completa el anterior.
Anade CSS de paso lockeado + JavaScript que detecta y desbloquea.
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# CSS a anadir
LOCK_CSS = '''.form-step.locked{opacity:0.42;pointer-events:none;filter:grayscale(0.4);position:relative;transition:all 0.3s ease}
.form-step.locked::after{content:'\\1F512  Completa el paso anterior';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.92);color:#fff;padding:12px 24px;border-radius:999px;font-size:13px;font-weight:700;pointer-events:none;white-space:nowrap;backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);box-shadow:0 8px 24px rgba(0,0,0,0.4);z-index:10}
.form-step.unlocked-anim{animation:stepUnlock 0.5s ease}
@keyframes stepUnlock{from{transform:translateY(-6px);opacity:0.6}to{transform:translateY(0);opacity:1}}
'''

# JavaScript que detecta y desbloquea pasos secuencialmente
LOCK_JS = '''
// ===== WIZARD SECUENCIAL: desbloqueo paso a paso =====
(function(){
  const steps = Array.from(document.querySelectorAll('.form-step'));
  if (steps.length < 2) return;

  // Lockear todos menos el primero al inicio
  steps.forEach((s, i) => { if (i > 0) s.classList.add('locked'); });

  function isStepComplete(step) {
    // 1. Select obligatorio (tamano)
    const sel = step.querySelector('select[required]');
    if (sel && !sel.value) return false;

    // 2. Radios obligatorios (orientacion, grosor, color_marco, color_colgador)
    const radios = step.querySelectorAll('input[type="radio"][required]');
    if (radios.length > 0) {
      const name = radios[0].name;
      if (!step.querySelector(`input[name="${name}"]:checked`)) return false;
    }

    // 3. Upload zone (imagen): hidden #imagen-url debe tener URL valida
    const urlField = step.querySelector('#imagen-url');
    if (urlField) {
      if (!urlField.value || !urlField.value.startsWith('https://res.cloudinary.com/')) return false;
    }

    // 4. Inputs obligatorios (datos de envio): TODOS deben ser validos
    const inputs = step.querySelectorAll('input[required], textarea[required]');
    if (inputs.length > 0) {
      for (const inp of inputs) {
        if (!inp.value.trim()) return false;
        if (!inp.checkValidity()) return false;
      }
    }

    return true;
  }

  function refreshLocks() {
    let allValidUpToHere = true;
    steps.forEach((step, i) => {
      if (i === 0) {
        // Primer paso nunca lockeado
        if (!isStepComplete(step)) allValidUpToHere = false;
        return;
      }
      if (allValidUpToHere) {
        if (step.classList.contains('locked')) {
          step.classList.remove('locked');
          step.classList.add('unlocked-anim');
          setTimeout(() => step.classList.remove('unlocked-anim'), 500);
        }
        if (!isStepComplete(step)) allValidUpToHere = false;
      } else {
        step.classList.add('locked');
      }
    });
  }

  // Listeners
  document.addEventListener('change', refreshLocks);
  document.addEventListener('input', refreshLocks);
  // Tambien cuando termine upload de Cloudinary
  const urlField = document.getElementById('imagen-url');
  if (urlField) {
    // Polling ya que el value se setea via JS sin disparar evento
    let lastVal = urlField.value;
    setInterval(() => {
      if (urlField.value !== lastVal) {
        lastVal = urlField.value;
        refreshLocks();
      }
    }, 500);
  }
  // Llamada inicial
  refreshLocks();
})();
'''

# Buscar todas las paginas de pedido
pedido_files = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])

count_ok = 0
for filename in pedido_files:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar si ya tiene wizard
    if 'WIZARD SECUENCIAL' in content:
        print(f"SKIP {filename}  (ya tiene wizard)")
        continue

    # 1. Inyectar CSS antes de </style>
    if '</style>' in content:
        content = content.replace('</style>', LOCK_CSS + '\n</style>', 1)
    else:
        print(f"FAIL {filename}  (no se encontro </style>)")
        continue

    # 2. Inyectar JS antes de </script> del ultimo script (o crear nuevo)
    # Lo agrego antes de </body>
    if '</body>' in content:
        content = content.replace('</body>', '<script>' + LOCK_JS + '</script>\n</body>', 1)
    else:
        print(f"FAIL {filename}  (no se encontro </body>)")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}")
    count_ok += 1

print(f"\nDONE — wizard secuencial aplicado a {count_ok} paginas")
