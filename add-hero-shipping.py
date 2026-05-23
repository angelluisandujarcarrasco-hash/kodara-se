"""
Añade el badge 'Envío gratis' en el header (debajo de page-sub) a todas las páginas de pedido.
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

# CSS del hero-shipping (si no está ya)
css_block = '''.hero-shipping{
  display:inline-flex;align-items:center;gap:10px;
  margin-top:22px;
  background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.35);
  border-radius:999px;padding:10px 22px;
  font-size:14px;color:#10B981;font-weight:700;
  box-shadow:0 4px 16px rgba(16,185,129,0.15);
}
.hero-shipping strong{color:#10B981;font-weight:800;letter-spacing:0.2px}
.shipping-icon{font-size:18px}
'''

# HTML del badge
shipping_html = '''    <div class="hero-shipping">
      <span class="shipping-icon">🚚</span>
      <strong>Envío gratis</strong>
    </div>
'''

# Buscar todas las páginas de pedido
pedido_files = [f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")]

for filename in sorted(pedido_files):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insertar CSS si no está
    if ".hero-shipping{" not in content:
        # Insertar antes de "/* ===== FORM =====" o "/* ===== FOOTER ===== */" o ":root"
        # Usamos un marcador estable: insertarlo antes de "/* footer */"
        if "/* footer */" in content:
            content = content.replace("/* footer */", css_block + "\n/* footer */", 1)
        else:
            # fallback: antes del </style>
            content = content.replace("</style>", css_block + "</style>", 1)

    # 2. Insertar HTML del badge después del </p> que cierra page-sub (dentro del header)
    # Patrón: </p>\n  </div>\n</header>
    # Insertamos shipping_html antes de </div>\n</header>
    if "hero-shipping" not in content.split("</header>")[0]:
        content = re.sub(
            r'(</p>\s*\n)(\s*</div>\s*\n</header>)',
            r'\1' + shipping_html + r'\2',
            content,
            count=1,
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}")

print(f"\nDONE — {len(pedido_files)} paginas de pedido actualizadas con 'Envio gratis' en header")
