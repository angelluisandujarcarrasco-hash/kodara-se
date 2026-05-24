"""
Limpieza V2: busca y elimina el bloque garbage especifico que quedo:
  });
  return;
    }
    if(zone.classList.contains('uploading')){...}
  });
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"
pages = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])

count_fixed = 0
count_clean = 0

for filename in pages:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Patron especifico: }); seguido de return;...if(zone.classList.contains)...});
    pattern = r'\}\);\s*return;\s*\}\s*if\s*\(\s*zone\.classList\.contains\([\'"]uploading[\'"]\).*?\}\s*\}\);'
    content = re.sub(pattern, '});', content, flags=re.DOTALL)

    # Patron alternativo si return; esta en linea diferente
    pattern2 = r'\}\);\s*\n\s*return;\s*\n\s*\}\s*\n\s*if\s*\(\s*zone\.classList.*?\}\);'
    content = re.sub(pattern2, '});', content, flags=re.DOTALL)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"FIX  {filename}")
        count_fixed += 1
    else:
        # verificar si tiene el patron problematico
        if 'return;\n  }\n  if(zone.classList.contains' in original or 'return;' in original.split('addToCart(item);')[-1].split('// WIZARD')[0]:
            print(f"WARN {filename}  (patron no detectado)")
        else:
            count_clean += 1

print(f"\n=== DONE ===")
print(f"Fixed: {count_fixed}")
print(f"Clean: {count_clean}")
