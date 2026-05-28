/**
 * Serverless function: crea una sesion de Stripe Checkout
 * para los items del carrito de Kodara Print Studio.
 *
 * Recibe via POST: { items: [...], cliente: {...} }
 * Devuelve: { url: 'https://checkout.stripe.com/...' }
 */

const Stripe = require('stripe');

module.exports = async (req, res) => {
  // CORS headers para que kodarase.com pueda llamar este endpoint
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2024-12-18.acacia',
    });

    const { items, customer_email } = req.body || {};

    if (!items || !Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ error: 'No items in cart' });
    }

    // Construir line_items para Stripe
    const line_items = items.map(item => {
      // Construir descripcion con todas las opciones
      const desc_parts = [
        item.tamano,
        item.color,
        item.orientacion,
        item.grosor,
        item.color_marco,
        item.color_colgador,
        item.color_panel,
      ].filter(Boolean);
      const description = desc_parts.length > 0 ? desc_parts.join(' · ') : undefined;

      // Imagen del producto (la imagen que sube el cliente)
      const images = item.imagen_url ? [item.imagen_url] : [];

      return {
        price_data: {
          currency: 'usd',
          product_data: {
            name: item.producto || 'Producto Kodara Print',
            description: description,
            images: images,
            metadata: {
              pedido_page: item.pedido_page || '',
              imagen_url: item.imagen_url || '',
            },
          },
          unit_amount: Math.round((item.precio_num || 0) * 100), // Stripe usa centavos
        },
        quantity: item.cantidad || 1,
      };
    });

    // URLs de retorno
    const origin = req.headers.origin || 'https://kodarase.com';
    const success_url = `${origin}/gracias.html?session_id={CHECKOUT_SESSION_ID}`;
    const cancel_url = `${origin}/carrito.html`;

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      payment_method_types: ['card'],
      line_items: line_items,
      customer_email: customer_email,
      allow_promotion_codes: true,
      success_url,
      cancel_url,
      shipping_address_collection: {
        allowed_countries: ['US', 'ES', 'MX', 'DO', 'AR', 'CO', 'CL', 'PE', 'PR', 'CA'],
      },
      phone_number_collection: {
        enabled: true,
      },
      metadata: {
        items_count: String(items.length),
        total_usd: String(items.reduce((sum, i) => sum + (i.precio_num || 0) * (i.cantidad || 1), 0)),
      },
    });

    return res.status(200).json({
      url: session.url,
      session_id: session.id,
    });
  } catch (err) {
    console.error('Stripe error:', err);
    return res.status(500).json({
      error: 'No se pudo crear la sesión de pago',
      detail: err.message,
    });
  }
};
