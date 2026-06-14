/**
 * Kodarase i18n — Inglés por defecto + botón ES/EN.
 * - index.html ya tiene su propio sistema data-es/data-en: esta engine NO lo toca.
 * - El resto de páginas se traducen con el diccionario KODARA_DICT (ES -> EN).
 * - El idioma se recuerda en localStorage('kodara_lang') y se aplica en TODAS las páginas.
 * Default: 'en' (inglés).
 */
(function () {
  'use strict';
  var LS = 'kodara_lang';
  var lang = (function () { try { return localStorage.getItem(LS) || 'en'; } catch (e) { return 'en'; } })();

  // Diccionario Español -> Inglés (texto EXACTO, ya recortado).
  var DICT = window.KODARA_DICT || {};

  // ---- Si la página ya trae el sistema authored (index.html), no interferir ----
  // (index gestiona su propio toggle y persistencia con la misma clave localStorage)
  var AUTHORED = !!document.querySelector('[data-es]');

  // ---------- utilidades de traducción por diccionario ----------
  function translate(original) {
    var key = original.trim();
    if (!key) return null;
    var en = DICT[key];
    if (en === undefined) return null;
    // conserva espacios/altos de línea alrededor del texto
    return original.replace(key, en);
  }

  function shouldSkip(node) {
    var p = node.parentNode;
    if (!p) return true;
    var name = p.nodeName;
    if (name === 'SCRIPT' || name === 'STYLE' || name === 'NOSCRIPT' || name === 'TEXTAREA') return true;
    // no tocar lo que ya está traducido por data-es (por si acaso)
    if (p.closest && p.closest('[data-es]')) return true;
    if (p.closest && p.closest('.kd-lang-toggle')) return true;
    return false;
  }

  function applyToTextNodes(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var batch = [];
    var n;
    while ((n = walker.nextNode())) {
      if (!n.nodeValue || !n.nodeValue.trim()) continue;
      if (shouldSkip(n)) continue;
      batch.push(n);
    }
    batch.forEach(function (node) {
      if (node.__kdEs === undefined) node.__kdEs = node.nodeValue; // cachea original ES
      if (lang === 'en') {
        var tr = translate(node.__kdEs);
        if (tr !== null) node.nodeValue = tr;
      } else {
        node.nodeValue = node.__kdEs; // restaura ES
      }
    });
  }

  function applyToAttrs(root) {
    // placeholders
    var els = root.querySelectorAll ? root.querySelectorAll('[placeholder]') : [];
    Array.prototype.forEach.call(els, function (el) {
      if (el.closest('[data-es]')) return;
      if (el.__kdPhEs === undefined) el.__kdPhEs = el.getAttribute('placeholder') || '';
      if (lang === 'en') {
        var tr = translate(el.__kdPhEs);
        if (tr !== null) el.setAttribute('placeholder', tr);
      } else {
        el.setAttribute('placeholder', el.__kdPhEs);
      }
    });
    // botones tipo input value
    var ins = root.querySelectorAll ? root.querySelectorAll('input[type="submit"],input[type="button"]') : [];
    Array.prototype.forEach.call(ins, function (el) {
      if (el.closest('[data-es]')) return;
      if (el.__kdValEs === undefined) el.__kdValEs = el.getAttribute('value') || '';
      if (lang === 'en') {
        var tr = translate(el.__kdValEs);
        if (tr !== null) el.setAttribute('value', tr);
      } else {
        el.setAttribute('value', el.__kdValEs);
      }
    });
  }

  function applyAll(root) {
    root = root || document.body;
    if (!root) return;
    applyToTextNodes(root);
    applyToAttrs(root);
    document.documentElement.lang = lang;
  }

  // ---------- botón flotante ES/EN ----------
  function injectToggle() {
    if (document.querySelector('.lang-toggle') || document.querySelector('.kd-lang-toggle')) return; // index ya tiene
    var css = '' +
      '.kd-lang-toggle{position:fixed;right:14px;bottom:14px;z-index:99996;display:flex;background:rgba(255,248,236,0.96);' +
      'border:1px solid rgba(60,50,40,0.18);border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,0.16);overflow:hidden;' +
      "font-family:'Inter',system-ui,sans-serif;backdrop-filter:blur(8px)}" +
      '.kd-lang-toggle button{border:none;background:transparent;cursor:pointer;font-size:13px;font-weight:800;letter-spacing:0.5px;' +
      'color:#8A7864;padding:9px 15px;transition:all .2s;line-height:1}' +
      '.kd-lang-toggle button.active{background:linear-gradient(135deg,#C15431,#B58850);color:#fff}' +
      '@media(max-width:600px){.kd-lang-toggle{right:10px;bottom:10px}.kd-lang-toggle button{padding:8px 13px;font-size:12px}}';
    var st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);

    var box = document.createElement('div');
    box.className = 'kd-lang-toggle';
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', 'Language');
    box.innerHTML =
      '<button type="button" data-l="en" aria-label="English">EN</button>' +
      '<button type="button" data-l="es" aria-label="Español">ES</button>';
    box.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-l')); });
    });

    function place() {
      if (document.body) document.body.appendChild(box);
      else document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(box); });
    }
    place();
    refreshToggle();
  }

  function refreshToggle() {
    var btns = document.querySelectorAll('.kd-lang-toggle button');
    btns.forEach(function (b) { b.classList.toggle('active', b.getAttribute('data-l') === lang); });
  }

  // ---------- API pública ----------
  function setLang(l) {
    lang = (l === 'es') ? 'es' : 'en';
    try { localStorage.setItem(LS, lang); } catch (e) {}
    window.kodaraLang = lang;
    applyAll(document.body);
    refreshToggle();
    if (typeof window.onKodaraLangChange === 'function') {
      try { window.onKodaraLangChange(lang); } catch (e) {}
    }
  }
  window.kodaraSetLang = setLang;
  window.kodaraLang = lang;

  // ---------- arranque ----------
  if (AUTHORED) {
    // index.html: su propio script gestiona idioma + toggle. No hacemos nada aquí.
    return;
  }

  function start() {
    applyAll(document.body);
    injectToggle();
    // observa contenido dinámico (carrito, banner, modales) para traducirlo también
    try {
      var mo = new MutationObserver(function (muts) {
        muts.forEach(function (m) {
          Array.prototype.forEach.call(m.addedNodes, function (node) {
            if (node.nodeType === 1) { applyToTextNodes(node); applyToAttrs(node); }
            else if (node.nodeType === 3 && node.parentNode) { applyToTextNodes(node.parentNode); }
          });
        });
      });
      mo.observe(document.body, { childList: true, subtree: true });
    } catch (e) {}
  }

  if (document.body) start();
  else document.addEventListener('DOMContentLoaded', start);
})();
