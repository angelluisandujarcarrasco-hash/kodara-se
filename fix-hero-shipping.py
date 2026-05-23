"""
Añade el HTML del badge 'Envío gratis' a las páginas de pedido que solo tienen el CSS.
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

shipping_html = '''    <div class="hero-shipping">
      <span class="shipping-icon">🚚</span>
      <strong>Envío gratis</strong>
    </div>
'''

pedido_files = [f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")]

for filename in sorted(pedido_files):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if '<div class="hero-shipping">' in content:
        print(f"SKIP {filename} (ya tiene HTML del badge)")
        continue

    # Insertar antes de </div>\n</header>
    new_content, n = re.subn(
        r'(</p>\s*\n)(\s*</div>\s*\n</header>)',
        r'\1' + shipping_html + r'\2',
        content,
        count=1,
    )
    if n > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK   {filename}")
    else:
        print(f"FAIL {filename} (regex no encontro patron)")
