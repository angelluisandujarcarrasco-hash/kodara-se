/**
 * Serverless function: recibe una reseña del formulario público
 * y la agrega a reviews.json en GitHub via API.
 *
 * Recibe via POST FormData o JSON:
 *   { name, location, rating, text_es, text_en, image_base64 }
 *
 * Requiere env vars en Vercel:
 *   GITHUB_TOKEN      - Personal Access Token con scope "repo" (o solo "public_repo")
 *   GITHUB_REPO       - "angelluisandujarcarrasco-hash/kodara-se"
 *   GITHUB_BRANCH     - "main"
 *
 * Anti-spam: validaciones de longitud, sin URLs en texto, rate limit por IP.
 */

const REPO = process.env.GITHUB_REPO || 'angelluisandujarcarrasco-hash/kodara-se';
const BRANCH = process.env.GITHUB_BRANCH || 'main';
const TOKEN = process.env.GITHUB_TOKEN;

// Memoria simple para rate limit (se reinicia con cold start, suficiente para prevenir spam burst)
const recentSubmissions = new Map();
const RATE_LIMIT_WINDOW_MS = 5 * 60 * 1000; // 5 min
const RATE_LIMIT_MAX = 3; // máximo 3 reseñas por IP cada 5 min

function cleanRateLimit() {
  const now = Date.now();
  for (const [ip, times] of recentSubmissions.entries()) {
    const filtered = times.filter(t => now - t < RATE_LIMIT_WINDOW_MS);
    if (filtered.length === 0) recentSubmissions.delete(ip);
    else recentSubmissions.set(ip, filtered);
  }
}

function checkRateLimit(ip) {
  cleanRateLimit();
  const times = recentSubmissions.get(ip) || [];
  if (times.length >= RATE_LIMIT_MAX) return false;
  times.push(Date.now());
  recentSubmissions.set(ip, times);
  return true;
}

function sanitize(text, maxLen = 500) {
  if (typeof text !== 'string') return '';
  return text.trim().slice(0, maxLen);
}

function containsUrls(text) {
  return /https?:\/\/|www\.|\.com|\.net|\.org|\.io/i.test(text);
}

async function ghGet(path) {
  const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}?ref=${BRANCH}`, {
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'kodarase-reviews',
    },
  });
  if (!res.ok) throw new Error(`GitHub GET failed: ${res.status} ${await res.text()}`);
  return await res.json();
}

async function ghPut(path, contentBase64, sha, message) {
  const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'kodarase-reviews',
    },
    body: JSON.stringify({
      message,
      content: contentBase64,
      sha,
      branch: BRANCH,
    }),
  });
  if (!res.ok) throw new Error(`GitHub PUT failed: ${res.status} ${await res.text()}`);
  return await res.json();
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!TOKEN) {
    return res.status(500).json({ error: 'GITHUB_TOKEN no configurado en Vercel' });
  }

  // Rate limit
  const ip = req.headers['x-forwarded-for']?.split(',')[0] || req.connection?.remoteAddress || 'unknown';
  if (!checkRateLimit(ip)) {
    return res.status(429).json({ error: 'Demasiados envíos. Intenta en unos minutos.' });
  }

  try {
    const body = req.body || {};
    const name = sanitize(body.name, 60);
    const location = sanitize(body.location, 100) || 'Cliente verificado';
    const rating = Math.min(5, Math.max(1, parseInt(body.rating, 10) || 5));
    const text_es = sanitize(body.text_es, 600);
    const text_en = sanitize(body.text_en, 600) || text_es;
    const honeypot = body.website; // honeypot

    // Validaciones
    if (honeypot) {
      // bot caught — pretend success
      return res.status(200).json({ ok: true });
    }
    if (!name || name.length < 2) {
      return res.status(400).json({ error: 'Nombre inválido' });
    }
    if (!text_es || text_es.length < 10) {
      return res.status(400).json({ error: 'El comentario es muy corto (mín 10 caracteres)' });
    }
    if (containsUrls(text_es) || containsUrls(text_en)) {
      return res.status(400).json({ error: 'No se permiten enlaces en el comentario' });
    }

    // Subir imagen si viene en base64
    let image_url = '';
    if (body.image_base64 && typeof body.image_base64 === 'string' && body.image_base64.length > 100) {
      const match = body.image_base64.match(/^data:image\/(jpeg|jpg|png|webp);base64,(.+)$/i);
      if (match) {
        const ext = match[1].toLowerCase() === 'jpeg' ? 'jpg' : match[1].toLowerCase();
        const imgB64 = match[2];
        // Tamaño máximo ~3MB en base64
        if (imgB64.length > 4 * 1024 * 1024) {
          return res.status(400).json({ error: 'Imagen muy grande (máx 3MB)' });
        }
        const imgFilename = `img/reviews/${Date.now()}-${Math.random().toString(36).slice(2,8)}.${ext}`;
        await ghPut(imgFilename, imgB64, undefined, `review: imagen de ${name}`);
        image_url = imgFilename;
      }
    }

    // Leer reviews.json actual
    const reviewsFile = await ghGet('reviews.json');
    const currentContent = JSON.parse(Buffer.from(reviewsFile.content, 'base64').toString('utf8'));
    const reviews = Array.isArray(currentContent.reviews) ? currentContent.reviews : [];

    // Crear nueva reseña
    const newReview = {
      id: 'r-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6),
      name,
      location,
      rating,
      text_es,
      text_en,
      image_url,
      date: new Date().toISOString().slice(0, 10),
      approved: true,
      placeholder: false,
    };

    // Si las primeras son placeholders, las eliminamos en el primer envío real
    const cleanedReviews = reviews.filter(r => !r.placeholder);
    cleanedReviews.unshift(newReview);

    const newContent = JSON.stringify({ reviews: cleanedReviews }, null, 2) + '\n';
    const newContentBase64 = Buffer.from(newContent, 'utf8').toString('base64');

    await ghPut(
      'reviews.json',
      newContentBase64,
      reviewsFile.sha,
      `review: nueva reseña de ${name} (${rating}★)`
    );

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('submit-review error:', err);
    return res.status(500).json({ error: 'Error al guardar. Intenta más tarde.' });
  }
};
