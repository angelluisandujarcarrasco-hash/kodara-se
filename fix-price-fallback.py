"""
Anade fallback para capturar precio del option seleccionado
cuando no hay #precio-hidden field (caso de Posteres y otros).
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"
pages = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])

# El bloque actual a buscar
OLD = """  // Capturar precio del precio-hidden o del data-price del option
  const precioHidden = form.querySelector('#precio-hidden');
  if (precioHidden && precioHidden.value) {
    item.precio_str = precioHidden.value;
    const match = precioHidden.value.match(/\\$(\\d+)/);
    if (match) item.precio_num = parseInt(match[1]);
  }"""

# El nuevo bloque con fallback al data-price del option
NEW = """  // Capturar precio del precio-hidden o del data-price del option
  const precioHidden = form.querySelector('#precio-hidden');
  if (precioHidden && precioHidden.value) {
    item.precio_str = precioHidden.value;
    const match = precioHidden.value.match(/\\$(\\d+)/);
    if (match) item.precio_num = parseInt(match[1]);
  }
  // Fallback: leer del option seleccionado (data-price o variantes con grosor)
  if (!item.precio_num) {
    const sizeSel = form.querySelector('select[name="tamano"]');
    if (sizeSel && sizeSel.selectedIndex >= 0) {
      const opt = sizeSel.options[sizeSel.selectedIndex];
      if (opt.dataset.price) {
        item.precio_num = parseInt(opt.dataset.price);
      }
      if (!item.precio_num) {
        const grosor = form.querySelector('input[name="grosor"]:checked');
        if (grosor) {
          const v = grosor.value.toLowerCase();
          if (v === 'esbelto' && opt.dataset.priceEsbelto) item.precio_num = parseInt(opt.dataset.priceEsbelto);
          else if (v === 'grueso' && opt.dataset.priceGrueso) item.precio_num = parseInt(opt.dataset.priceGrueso);
          else if (v === '10mm' && opt.dataset.pricethin) item.precio_num = parseInt(opt.dataset.pricethin);
          else if (v === '20mm' && opt.dataset.pricethick) item.precio_num = parseInt(opt.dataset.pricethick);
        }
      }
    }
  }"""

count_ok = 0
count_skip = 0

for filename in pages:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'Fallback: leer del option seleccionado' in content:
        count_skip += 1
        continue

    if OLD in content:
        content = content.replace(OLD, NEW)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK   {filename}")
        count_ok += 1
    else:
        print(f"MISS {filename}  (patron no encontrado)")

print(f"\n=== DONE === OK: {count_ok}  Skip: {count_skip}")
