/**
 * Asistente IA Kodara — Chat conversacional con Claude API
 * Backend: /api/chat-asistente (Vercel Function con ANTHROPIC_API_KEY)
 */
(function() {
  if (document.getElementById('chat-asistente-fab')) return;

  const API_URL = 'https://kodara-se-git-main-angelluisandujarcarrasco-5233s-projects.vercel.app/api/chat-asistente';
  const STORAGE_KEY = 'kodara_chat_history_v1';

  // ===== STORAGE =====
  function getHistory() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
    catch { return []; }
  }
  function saveHistory(h) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(h.slice(-20))); } catch {}
  }
  function clearHistory() { localStorage.removeItem(STORAGE_KEY); }

  // ===== ESTILOS =====
  const style = document.createElement('style');
  style.textContent = `
    #chat-asistente-fab {
      position: fixed; bottom: 24px; right: 24px; z-index: 9999;
      width: 62px; height: 62px; border-radius: 50%;
      background: linear-gradient(135deg, #F97316, #EC4899);
      box-shadow: 0 10px 30px rgba(249,115,22,0.4);
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
      border: none; padding: 0;
    }
    #chat-asistente-fab:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 14px 40px rgba(249,115,22,0.55); }
    #chat-asistente-fab svg { width: 30px; height: 30px; fill: #fff; }
    #chat-asistente-fab .pulse {
      position: absolute; inset: -4px; border-radius: 50%;
      background: rgba(249,115,22,0.4); animation: chat-pulse 2s infinite;
      pointer-events: none;
    }
    @keyframes chat-pulse {
      0% { transform: scale(1); opacity: 0.6; }
      100% { transform: scale(1.55); opacity: 0; }
    }
    #chat-asistente-panel {
      position: fixed; bottom: 100px; right: 24px; z-index: 9998;
      width: 380px; max-width: calc(100vw - 32px);
      height: 580px; max-height: calc(100vh - 130px);
      background: #0F1A2E; color: #fff;
      border-radius: 22px; border: 1px solid rgba(255,255,255,0.08);
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      display: none; flex-direction: column;
      overflow: hidden;
      font-family: 'Inter', sans-serif;
    }
    #chat-asistente-panel.open { display: flex; animation: chat-slide 0.3s ease; }
    @keyframes chat-slide {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .chat-header {
      background: linear-gradient(135deg, #F97316, #EC4899);
      padding: 16px 18px; display: flex; align-items: center; gap: 12px;
      flex-shrink: 0;
    }
    .chat-header-avatar {
      width: 38px; height: 38px; border-radius: 50%;
      background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center;
      font-size: 18px;
    }
    .chat-header-text { flex: 1; min-width: 0; }
    .chat-header-title { font-weight: 800; font-size: 15px; letter-spacing: -0.2px; }
    .chat-header-status {
      font-size: 11px; opacity: 0.9; display: flex; align-items: center; gap: 6px; margin-top: 2px;
    }
    .chat-header-status::before {
      content: ''; width: 7px; height: 7px; border-radius: 50%;
      background: #10B981; box-shadow: 0 0 8px #10B981;
    }
    .chat-close, .chat-reset {
      background: rgba(255,255,255,0.15); border: none; color: #fff;
      width: 30px; height: 30px; border-radius: 50%;
      cursor: pointer; font-size: 16px; line-height: 1;
      display: flex; align-items: center; justify-content: center;
      transition: background 0.2s;
    }
    .chat-close:hover, .chat-reset:hover { background: rgba(255,255,255,0.28); }
    .chat-reset { font-size: 14px; margin-right: 4px; }
    .chat-body {
      flex: 1; overflow-y: auto; padding: 18px;
      background: #0A1424;
      display: flex; flex-direction: column; gap: 12px;
      scroll-behavior: smooth;
    }
    .chat-body::-webkit-scrollbar { width: 6px; }
    .chat-body::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
    .chat-bubble {
      max-width: 85%; padding: 11px 15px; border-radius: 16px;
      font-size: 14px; line-height: 1.5;
      animation: chat-fade 0.3s ease;
    }
    @keyframes chat-fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; } }
    .chat-bubble.assistant {
      background: #131F36; color: #E8ECF4;
      border-top-left-radius: 4px; align-self: flex-start;
    }
    .chat-bubble.user {
      background: linear-gradient(135deg, #F97316, #EC4899); color: #fff;
      border-top-right-radius: 4px; align-self: flex-end;
    }
    .chat-bubble strong { color: #FB923C; font-weight: 700; }
    .chat-bubble.user strong { color: #fff; text-decoration: underline; }
    .chat-bubble a {
      color: #FB923C; font-weight: 600; text-decoration: underline;
    }
    .chat-bubble.user a { color: #fff; }
    .chat-typing {
      display: flex; gap: 4px; padding: 14px 16px;
      background: #131F36; border-radius: 16px; border-top-left-radius: 4px;
      align-self: flex-start;
    }
    .chat-typing span {
      width: 8px; height: 8px; border-radius: 50%; background: #6B7689;
      animation: chat-dot 1.4s infinite ease-in-out;
    }
    .chat-typing span:nth-child(2) { animation-delay: 0.2s; }
    .chat-typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes chat-dot {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
      30% { transform: translateY(-6px); opacity: 1; }
    }
    .chat-suggestions {
      display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;
    }
    .chat-sugg {
      background: rgba(249,115,22,0.08); border: 1px solid rgba(249,115,22,0.25);
      color: #FB923C; text-decoration: none;
      padding: 7px 12px; border-radius: 999px;
      font-size: 12px; font-weight: 600;
      cursor: pointer; transition: all 0.2s ease;
      display: inline-flex; align-items: center; gap: 5px;
    }
    .chat-sugg:hover {
      background: rgba(249,115,22,0.2); border-color: rgba(249,115,22,0.5);
    }
    .chat-form {
      display: flex; gap: 8px; padding: 12px;
      background: #0F1A2E; border-top: 1px solid rgba(255,255,255,0.06);
      flex-shrink: 0;
    }
    .chat-input {
      flex: 1; min-width: 0;
      background: #131F36; border: 1px solid rgba(255,255,255,0.06);
      color: #fff; font-size: 14px; font-family: inherit;
      padding: 12px 16px; border-radius: 999px;
      outline: none; transition: border-color 0.2s;
    }
    .chat-input::placeholder { color: #6B7689; }
    .chat-input:focus { border-color: #F97316; }
    .chat-send {
      width: 42px; height: 42px; border-radius: 50%; border: none;
      background: linear-gradient(135deg, #F97316, #EC4899);
      color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: transform 0.15s;
    }
    .chat-send:hover { transform: scale(1.06); }
    .chat-send:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
    .chat-send svg { width: 18px; height: 18px; fill: #fff; }
    @media (max-width: 480px) {
      #chat-asistente-panel { width: calc(100vw - 24px); right: 12px; height: calc(100vh - 110px); }
      #chat-asistente-fab { bottom: 18px; right: 18px; }
    }
  `;
  document.head.appendChild(style);

  // ===== FAB =====
  const fab = document.createElement('button');
  fab.id = 'chat-asistente-fab';
  fab.setAttribute('aria-label', 'Abrir asistente IA');
  fab.innerHTML = `
    <span class="pulse"></span>
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.48 2 2 6.04 2 11c0 2.45 1.1 4.68 2.88 6.29L4 22l5-1.5c.97.24 1.97.36 3 .36 5.52 0 10-4.04 10-9.36 0-4.97-4.48-9.5-10-9.5zm-3 8.5c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm6 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm-3-4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z"/>
    </svg>
  `;
  document.body.appendChild(fab);

  // ===== PANEL =====
  const panel = document.createElement('div');
  panel.id = 'chat-asistente-panel';
  panel.innerHTML = `
    <div class="chat-header">
      <div class="chat-header-avatar">🤖</div>
      <div class="chat-header-text">
        <div class="chat-header-title">Asistente Kodara</div>
        <div class="chat-header-status">En línea · IA real</div>
      </div>
      <button class="chat-reset" title="Nueva conversación">↻</button>
      <button class="chat-close" aria-label="Cerrar">×</button>
    </div>
    <div class="chat-body" id="chat-body"></div>
    <form class="chat-form" id="chat-form">
      <input type="text" class="chat-input" id="chat-input"
             placeholder="Escribe tu pregunta..." autocomplete="off" maxlength="500">
      <button type="submit" class="chat-send" aria-label="Enviar">
        <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
      </button>
    </form>
  `;
  document.body.appendChild(panel);

  // ===== LOGICA =====
  const body = panel.querySelector('#chat-body');
  const form = panel.querySelector('#chat-form');
  const input = panel.querySelector('#chat-input');
  const sendBtn = panel.querySelector('.chat-send');
  const resetBtn = panel.querySelector('.chat-reset');
  const closeBtn = panel.querySelector('.chat-close');
  let conversation = getHistory();

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    })[c]);
  }
  function linkify(text) {
    return escapeHtml(text)
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\b(demo-[\w-]+\.html|empezar-proyecto\.html|servicio-kodara-print\.html|kodarase\.com)\b/g,
              '<a href="$1" target="_self">$1</a>')
      .replace(/\n/g, '<br>');
  }

  function addBubble(role, content) {
    const div = document.createElement('div');
    div.className = `chat-bubble ${role}`;
    div.innerHTML = linkify(content);
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div;
  }

  function addSuggestions(items) {
    const wrap = document.createElement('div');
    wrap.className = 'chat-suggestions';
    items.forEach(it => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'chat-sugg';
      btn.textContent = it;
      btn.addEventListener('click', () => {
        input.value = it;
        form.requestSubmit();
        wrap.remove();
      });
      wrap.appendChild(btn);
    });
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function addTyping() {
    const div = document.createElement('div');
    div.className = 'chat-typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div;
  }

  function renderHistory() {
    body.innerHTML = '';
    if (conversation.length === 0) {
      addBubble('assistant', '¡Hola! 👋 Soy el asistente de **Kodara**. Pregúntame cualquier cosa sobre nuestros servicios o cuéntame qué necesitas para tu negocio.');
      addSuggestions([
        'Quiero una web',
        'Audita mi SEO',
        'Auditar Meta Ads',
        'Encontrar clientes',
        'Imprimir productos',
        'Ver precios',
      ]);
    } else {
      conversation.forEach(m => addBubble(m.role, m.content));
    }
  }

  async function sendMessage(text) {
    if (!text.trim()) return;
    addBubble('user', text);
    conversation.push({ role: 'user', content: text });
    saveHistory(conversation);

    sendBtn.disabled = true;
    input.disabled = true;
    const typingEl = addTyping();

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: conversation.slice(0, -1),
          userMessage: text,
        }),
      });
      typingEl.remove();
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || `Error ${res.status}`);
      }
      const data = await res.json();
      const reply = data.reply || 'Disculpa, no pude responder.';
      addBubble('assistant', reply);
      conversation.push({ role: 'assistant', content: reply });
      saveHistory(conversation);
    } catch (err) {
      typingEl.remove();
      addBubble('assistant', `Disculpa, hubo un error: ${err.message}. Escríbenos a **kodaraservice@gmail.com** y te respondemos personalmente.`);
    } finally {
      sendBtn.disabled = false;
      input.disabled = false;
      input.focus();
    }
  }

  // ===== EVENTS =====
  fab.addEventListener('click', () => {
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) {
      const pulse = fab.querySelector('.pulse');
      if (pulse) pulse.style.display = 'none';
      if (body.children.length === 0) renderHistory();
      setTimeout(() => input.focus(), 300);
    }
  });
  closeBtn.addEventListener('click', () => panel.classList.remove('open'));
  resetBtn.addEventListener('click', () => {
    if (confirm('¿Empezar conversación nueva?')) {
      conversation = [];
      clearHistory();
      renderHistory();
    }
  });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    sendMessage(text);
  });
})();
