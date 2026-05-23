"""
Limpia menciones a 'IA', 'Higgsfield', 'avatar', 'Sofia' del demo-marketing.html.
Reemplaza por terminos profesionales sin mencionar IA.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"
path = os.path.join(OUT_DIR, "demo-marketing.html")

# Pares (buscar → reemplazar)
replacements = [
    # Hero meta
    ("🎬 Videos IA con Higgsfield", "🎬 Videos cinematográficos premium"),
    ("🎬 AI videos with Higgsfield", "🎬 Premium cinematic videos"),

    # Section titles
    ("Videos reales creados con Higgsfield IA", "Videos cinematográficos premium"),
    ("Real videos made with Higgsfield AI", "Premium cinematic videos"),

    # Video descriptions
    ("Comercial cinematográfico fitness con Marketing Studio Higgsfield", "Comercial cinematográfico fitness premium"),
    ("Cinematic fitness commercial with Higgsfield Marketing Studio", "Premium cinematic fitness commercial"),

    # Sofia avatar
    ("UGC — Reseña con avatar Sofia", "UGC — Reseña testimonial"),
    ("UGC — Review with avatar Sofia", "UGC — Testimonial review"),
    ("UGC — Reseña con avatar Sofia", "UGC — Reseña testimonial"),
    ("UGC — Review with avatar Sofia", "UGC — Testimonial review"),
    ("Avatar IA habla en español sobre tu producto con lip sync perfecto",
     "Presentadora habla en español sobre tu producto con sincronización perfecta"),
    ("AI Avatar speaks in Spanish about your product with perfect lip sync",
     "Presenter speaks in Spanish about your product with perfect lip sync"),

    # Sofia te explica
    ("Sofia te explica en 15 segundos todo lo que Kodara SE puede hacer por tu negocio",
     "Mira en 15 segundos todo lo que Kodara SE puede hacer por tu negocio"),
    ("Sofia explains in 15 seconds everything Kodara SE can do for your business",
     "Watch in 15 seconds everything Kodara SE can do for your business"),
    ("Sofia te explica", "Te explicamos"),
    ("Sofia explains", "We explain"),

    # Plan features - videos IA
    ("1 video IA Higgsfield", "1 video cinematográfico premium"),
    ("1 Higgsfield AI video", "1 premium cinematic video"),
    ("4 videos IA Higgsfield", "4 videos cinematográficos premium"),
    ("4 Higgsfield AI videos", "4 premium cinematic videos"),
    ("8 videos IA Higgsfield", "8 videos cinematográficos premium"),
    ("8 Higgsfield AI videos", "8 premium cinematic videos"),

    # Avatar IA personalizado
    ("Avatar IA hablando español", "Presentadora hablando español"),
    ("AI Avatar speaking Spanish", "Presenter speaking Spanish"),
    ("Avatar IA personalizado", "Presentadora personalizada"),
    ("Custom AI Avatar", "Custom presenter"),

    # Bottom CTA
    ("Marketing digital completo: estrategia, contenido con IA, anuncios optimizados",
     "Marketing digital completo: estrategia, contenido cinematográfico premium, anuncios optimizados"),
    ("Complete digital marketing: strategy, AI content, optimized ads",
     "Complete digital marketing: strategy, premium content, optimized ads"),
]

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

count = 0
for old, new in replacements:
    if old in content:
        c = content.count(old)
        content = content.replace(old, new)
        count += c
        print(f"OK ({c}x): {old[:60]}...")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# Verificar si quedan menciones residuales
residuals = ["Higgsfield", "Avatar IA", "AI Avatar", "video IA", "AI video", "videos IA", "AI videos", " Sofia"]
print("\n=== Verificación post-limpieza ===")
for term in residuals:
    n = content.count(term)
    if n > 0:
        print(f"  ⚠ Quedan {n} menciones de: '{term}'")
    else:
        print(f"  ✓ Limpio: '{term}'")

print(f"\nDONE — {count} reemplazos en demo-marketing.html")
