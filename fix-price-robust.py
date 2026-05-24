"""
Reemplaza el fallback de precio con uno super robusto:
1. precio-hidden
2. opt.dataset.price (simple)
3. opt.dataset.priceEsbelto/Grueso o pricethin/thick
4. ULTIMO RECURSO: extrae $XX del texto del option (value o textContent)
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"
pages = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])

# Bloque viejo a reemplazar (lo que pusimos en fix-price-fallback.py)
OLD = """  // Fallback: leer del option seleccionado (data-price o variantes con grosor)
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

# Nuevo bloque MAS robusto
NEW = """  // Fallback robusto: capturar precio del option seleccionado (multiples patrones)
  if (!item.precio_num) {
    const sizeSel = form.querySelector('select[name="tamano"]');
    if (sizeSel && sizeSel.selectedIndex >= 0) {
      const opt = sizeSel.options[sizeSel.selectedIndex];
      if (opt) {
        // 1. data-price simple (Posteres, Marco Madera, etc.)
        if (opt.dataset.price) item.precio_num = parseInt(opt.dataset.price);
        // 2. Variantes con grosor
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
        // 3. Ultimo recurso: extraer $XX del value/text del option
        if (!item.precio_num) {
          const txt = (opt.value || '') + ' ' + (opt.textContent || '');
          const m = txt.match(/\\$(\\d+)/);
          if (m) item.precio_num = parseInt(m[1]);
        }
      }
    }
    // 4. Tambien intentar desde el priceAmount visible si existe
    if (!item.precio_num) {
      const pa = document.getElementById('price-amount');
      if (pa) {
        const m = pa.textContent.match(/\\$(\\d+)/);
        if (m) item.precio_num = parseInt(m[1]);
      }
    }
  }"""

count_ok = 0
count_skip = 0

for filename in pages:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'Fallback robusto' in content:
        count_skip += 1
        continue

    if OLD in content:
        content = content.replace(OLD, NEW)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK   {filename}")
        count_ok += 1
    else:
        print(f"MISS {filename}")

print(f"\n=== DONE === OK: {count_ok}, Skip: {count_skip}")
