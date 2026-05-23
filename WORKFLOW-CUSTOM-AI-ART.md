# 🎨 Workflow Custom AI Art — Kodara

Guía paso a paso para procesar cada pedido del servicio Custom AI Art.

---

## 📥 FLUJO COMPLETO POR PEDIDO

### PASO 1 — Llega el pedido (email)
- FormSubmit te envía email a `kodaraservice@gmail.com`
- Contiene: nombre, email, producto, estilo, detalles, foto adjunta
- Tiempo objetivo: responder en menos de 1 hora

### PASO 2 — Confirmar al cliente (5 min)
Responder al email del cliente con plantilla:

```
Asunto: ¡Recibimos tu pedido! Próximos pasos · Kodara Custom AI Art

Hola {nombre},

¡Perfecto, ya tengo todo lo que necesito para empezar!

✓ Producto: {producto}
✓ Estilo: {estilo}
✓ Detalles registrados

Voy a generar 3 versiones diferentes con IA en las próximas 24 horas.
Te las enviaré por este mismo email para que elijas la que más te guste.

Cuando elijas, te mando enlace de pago Stripe.
Después de pagar, imprimimos premium y enviamos en 5-7 días.

¿Algo que quieras añadir o cambiar?

— Angel
Kodara SE | kodarase.com
```

### PASO 3 — Generar con IA (30-60 min)
Usar Higgsfield según producto:

**Pet Portrait:**
- Modelo: `nano_banana_pro`
- Subir foto del cliente como `image` media
- Prompt: "Transform reference pet into [STYLE] portrait, keep exact face features, [DETAILS]"
- Generar 3 variantes (count: 3)
- Aspect ratio: 2:3 (vertical) o 1:1 (square)

**Wedding Sign:**
- Modelo: `nano_banana_pro`
- Prompt con nombres + fecha + estilo botánico/elegante
- Generar 3 variantes
- Aspect ratio: 2:3

**Baby Poster:**
- Modelo: `nano_banana_pro`
- Prompt con nombre, fecha, peso, altura
- Generar 3 variantes
- Aspect ratio: 2:3

### PASO 4 — Enviar versiones al cliente (10 min)
Responder con las 3 URLs:

```
¡Listo! Aquí van las 3 versiones para que elijas:

🎨 OPCIÓN A: [URL]
🎨 OPCIÓN B: [URL]
🎨 OPCIÓN C: [URL]

¿Cuál te gusta más? Responde "A", "B" o "C".

Si quieres cambios, dime exactamente qué (color de fondo, posición del texto, estilo más vintage, etc.) y genero 3 nuevas en unas horas.

Una vez aprobada, te paso enlace de pago seguro.

— Angel
```

### PASO 5 — Cliente elige + paga (cliente lo hace)
- Cliente responde con elección (o pide revisión)
- Si pide revisión: vuelves a Paso 3 con los cambios
- Si aprueba: generas enlace de pago Stripe

### PASO 6 — Crear enlace de pago (5 min)
**Opción A — Stripe Link (mejor):**
1. Ve a stripe.com → Payment Links → Create
2. Producto: "Custom AI Art - {Tipo}"
3. Precio: el del pedido ($79/$149/$69 según caso)
4. Envía URL al cliente

**Opción B — PayPal.me:**
- Si el cliente prefiere PayPal
- URL: paypal.me/AngelLuisAndujarC/{monto}

### PASO 7 — Cliente paga → recibes notificación
- Te llega email de Stripe confirmando pago
- Ahora subes a Gelato para imprimir

### PASO 8 — Subir a Gelato (10 min)
1. Login en gelato.com
2. Click "Create Product" → "Wall Art" → "Posters"
3. Tamaño: A3 (estándar) o el que pidió el cliente
4. Sube la imagen final aprobada
5. **IMPORTANTE:** Modo "Manual Order" (no automático)
6. En la dirección de envío pones la dirección del CLIENTE
7. Confirmas y pagas a Gelato (con tarjeta, ~$8-15 por póster)
8. Gelato imprime y envía directo al cliente

### PASO 9 — Confirmar envío al cliente (5 min)
```
¡Tu pedido está en producción!

📦 Tracking: te llegará a este email cuando salga del centro de impresión
⏱️ Tiempo estimado: 5-7 días para USA, 7-12 días resto del mundo
🎁 Tu póster llegará en tubo protector resistente

Cualquier cosa, estoy aquí.
— Angel
```

### PASO 10 — Llega al cliente
- Gelato envía email con tracking
- Cliente recibe el producto
- Si todo bien: pides reseña en TrustPilot/Google Maps
- Si problema: contactar a Gelato (ellos manejan reimpresiones)

---

## 💰 ECONOMÍA POR PEDIDO

### Pet Portrait ($79)
- Higgsfield (3 imágenes): ~$3 (15 créditos × $0.20)
- Gelato impresión A3: ~$10
- Envío: ~$5
- **Tu beneficio neto: ~$60**

### Wedding Sign ($149)
- Higgsfield (3 imágenes A2): ~$5
- Gelato impresión A2: ~$18
- Envío: ~$8
- **Tu beneficio neto: ~$118**

### Baby Poster ($69)
- Higgsfield: ~$3
- Gelato impresión A3: ~$10
- Envío: ~$5
- **Tu beneficio neto: ~$51**

**Margen promedio:** 76-80% — Excelente.

---

## ⏱️ TIEMPO TOTAL POR PEDIDO

- Confirmar al cliente: 5 min
- Generar IA: 30-60 min (tú haces otras cosas mientras procesa)
- Enviar versiones: 10 min
- Esperar elección + pago: variable (4-48h, cliente)
- Subir a Gelato: 10 min
- Cliente recibe: 5-12 días (Gelato)

**Tu tiempo activo por pedido:** ~30-45 minutos.

Con **20 pedidos/mes** = 10-15h de trabajo = $1,200-2,400 beneficio.
Con **40 pedidos/mes** = 20-30h = $2,400-4,800 beneficio.

---

## 🎯 ESTRATEGIA DE PRECIOS

Si entran 10+ pedidos en una semana y no puedes seguir → SUBE PRECIOS:
- Pet portrait: $79 → $99
- Wedding: $149 → $199
- Baby: $69 → $89

Aumenta precios un 20-30% cada vez que tengas backlog de 5+ pedidos pendientes.

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### Cliente no aprueba ninguna versión después de 2 rondas
- Ofrece reembolso completo
- Pero PIDE feedback específico (qué falta) antes de generar más
- Marca como "complicado" en tu CRM mental

### IA no genera bien la cara de la mascota
- Pídale al cliente foto más clara, frontal, buena luz
- Genera con `medias` role:"image" + descripción muy detallada de raza/color

### Gelato impresión sale mal
- Contactar a Gelato support — reimprimen gratis
- Mientras tanto, mantén al cliente informado

### Cliente quiere cambio de talla después de imprimir
- No se puede cambiar (ya imprimió)
- Ofrece descuento 20% en próximo pedido
- Aprende: confirma siempre talla ANTES de imprimir

---

## 📊 KPIs A MEDIR (mensual)

- Pedidos recibidos
- Pedidos completados (conversión)
- Ticket promedio ($)
- Margen por pedido ($)
- Tiempo de respuesta promedio
- Pedidos por categoría (cuál vende más)
- Reseñas 5⭐ (objetivo: 95%+)

Si pet portraits dominan → expandir esa línea (cuadros, tazas, camisetas con mascota).

---

## 🚀 EXPANSIÓN FUTURA (cuando estés cómodo)

Productos adicionales a añadir cuando domines los 3 actuales:

- 🎨 **Family Portrait Cartoon** ($99) — foto familia → estilo Pixar
- 🌌 **Custom Star Map** ($89) — mapa del cielo en fecha especial
- 📜 **Memorial Poster** ($79) — homenaje a fallecido (gentil, emocional)
- 👫 **Couple Portrait** ($89) — pareja en cualquier estilo artístico
- 🏠 **House Portrait** ($129) — pinta de tu casa estilo acuarela
- 🚗 **Car Portrait** ($99) — coche favorito retro
- ☕ **Custom Mug** ($25) — taza con foto/diseño personalizado
- 👕 **Custom T-shirt** ($35) — camiseta con diseño IA
- 🧢 **Custom Cap** ($28) — gorra personalizada
- 📅 **Custom Calendar** ($35) — calendario con fotos del año
- 📚 **Custom Photo Book** ($89) — libro de fotos del año

**Todos siguen el MISMO workflow** — solo cambia el producto en Gelato.

---

## 🤝 RECURSOS

- **Gelato:** gelato.com (impresión + envío)
- **Higgsfield:** higgsfield.ai (generación IA — ya tienes Plus $29/mes)
- **Stripe:** stripe.com (cobros con tarjeta)
- **PayPal:** paypal.me/AngelLuisAndujarC (alternativa)
- **FormSubmit:** ya configurado en custom-ai-art.html

---

¡Esto es tu nuevo negocio escalable. Vamos por el primer pedido! 🚀
