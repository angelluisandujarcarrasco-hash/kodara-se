/**
 * Serverless function: Chat asistente IA con Claude API
 * Recibe via POST: { messages: [{role, content}], userMessage: string }
 * Devuelve: { reply: string }
 */

const Anthropic = require('@anthropic-ai/sdk');

const SYSTEM_PROMPT = `Eres el asistente virtual de Kodarase (kodarase.com), una agencia digital + estudio de print-on-demand para emprendedores latinoamericanos. Tu trabajo es entender qué necesita el visitante y guiarlo al servicio correcto con respuestas BREVES, cálidas y útiles.

SERVICIOS DIGITALES (kodarase.com):
1. Diseño Web Premium — webs modernas en 48-72h
2. Instagram a Web — convertir perfil IG en una web profesional
3. Auditoría SEO — análisis completo de visibilidad en Google
4. Auditoría Meta Ads — revisar anuncios Facebook/Instagram
5. Auditoría de Negocio — análisis digital completo
6. Automatizaciones n8n — flujos automáticos para procesos repetitivos
7. Prospección de Clientes — encontrar leads en tu nicho
8. Dashboard de Facturas — análisis financiero visual
9. Chat IA para Web — instalar chatbot como este en su web
10. Marketing Digital — estrategia + Meta Ads + contenido

PRINT STUDIO (subdivisión, ver kodarase.com/servicio-kodara-print.html):
- Arte mural (lienzos, pósters, madera, metal, etc.)
- Próximamente: ropa, tazas, bolsas, tarjetas, calendarios, libros de fotos

REGLAS:
- Responde SIEMPRE en español (latino)
- Máximo 2-3 oraciones por respuesta
- Tono amigable pero profesional, sin emojis excesivos (1 ok)
- Si el visitante pide algo concreto, recomienda el servicio + sugiere ver la demo (puedes mencionar los nombres tipo "demo-auditoria-seo.html")
- Si pregunta precios: deriva a "Empezar mi proyecto" para cotización personalizada
- Si pregunta plazos: 48-72h entrega típica
- Si pregunta algo no relacionado: redirige amablemente a los servicios
- Nunca inventes precios ni datos. Si no sabes algo: "Te recomiendo escribirnos a kodaraservice@gmail.com"

Sé conciso, útil y guía al siguiente paso.`;

module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'API key not configured' });
    }

    const { messages = [], userMessage = '' } = req.body || {};
    if (!userMessage || typeof userMessage !== 'string') {
      return res.status(400).json({ error: 'userMessage required' });
    }

    // Limitar historial a 10 últimos mensajes para no inflar contexto
    const history = messages.slice(-10).filter(m =>
      m && typeof m.role === 'string' && typeof m.content === 'string' &&
      ['user', 'assistant'].includes(m.role) &&
      m.content.trim().length > 0
    );

    const client = new Anthropic({ apiKey });

    const response = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 350,
      system: SYSTEM_PROMPT,
      messages: [
        ...history,
        { role: 'user', content: userMessage.slice(0, 500) },
      ],
    });

    const reply = response.content?.[0]?.text || 'Disculpa, no entendí. ¿Puedes reformular?';
    return res.status(200).json({ reply });
  } catch (err) {
    console.error('Chat asistente error:', err);
    return res.status(500).json({
      error: 'Error procesando mensaje',
      details: err.message,
    });
  }
};
