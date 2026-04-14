/**
 * La Cassaforte — logica UI admin (Vanilla ES6+)
 *
 * SICUREZZA (pre-produzione): proteggere l’intera cartella /admin/ con
 * Cloudflare Zero Trust (Access) oltre a qualsiasi controllo applicativo
 * sulle API. Il token salvato in sessionStorage è solo un comodo per chiamare
 * le funzioni `/api/admin/*`: chiunque con XSS potrebbe leggerlo, quindi
 * Access + hardening CSP restano la barriera principale in produzione.
 */

(function () {
  'use strict';

  const TOKEN_KEY = 'aml_cassaforte_admin_secret';
  const API_BASE = '/api/admin';

  /**
   * @param {string} s
   */
  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /**
   * @param {unknown} raw
   * @returns {number} centesimi arrotondati, o NaN se non valido
   */
  function parseEurosToCents(raw) {
    const s = String(raw ?? '')
      .trim()
      .replace(/\s/g, '')
      .replace(',', '.');
    if (!s) return NaN;
    const n = Number.parseFloat(s);
    if (!Number.isFinite(n) || n < 0) return NaN;
    return Math.round(n * 100);
  }

  function getToken() {
    try {
      return sessionStorage.getItem(TOKEN_KEY) || '';
    } catch {
      return '';
    }
  }

  function setToken(value) {
    try {
      sessionStorage.setItem(TOKEN_KEY, value.trim());
    } catch {
      /* ignore */
    }
  }

  function clearToken() {
    try {
      sessionStorage.removeItem(TOKEN_KEY);
    } catch {
      /* ignore */
    }
  }

  /**
   * @param {string} path
   * @param {RequestInit} [init]
   */
  async function adminFetch(path, init) {
    const token = getToken();
    const headers = new Headers(init?.headers);
    headers.set('Accept', 'application/json');
    if (token) headers.set('Authorization', `Bearer ${token}`);
    return fetch(`${API_BASE}${path}`, { ...init, headers });
  }

  /**
   * @param {number} cents
   * @param {string} currency
   */
  function formatMoney(cents, currency) {
    const c = typeof cents === 'number' && Number.isFinite(cents) ? cents : 0;
    try {
      return new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: currency || 'EUR',
      }).format(c / 100);
    } catch {
      return `${(c / 100).toFixed(2)} ${currency || 'EUR'}`;
    }
  }

  /**
   * @param {string} iso
   */
  function formatDate(iso) {
    const d = new Date(String(iso || ''));
    if (Number.isNaN(d.getTime())) return String(iso || '—');
    return new Intl.DateTimeFormat('it-IT', {
      dateStyle: 'short',
      timeStyle: 'short',
    }).format(d);
  }

  /**
   * @param {string} status
   */
  function orderStatusBadge(status) {
    const s = String(status || '');
    const map = [
      { re: /paid|completed|succeeded/i, cls: 'cassaforte__badge--ok', label: 'Pagato / OK' },
      { re: /pending_checkout|draft|open/i, cls: 'cassaforte__badge--pending', label: 'In checkout' },
      { re: /await|bank|wire|bonific/i, cls: 'cassaforte__badge--pending', label: 'In attesa' },
      { re: /fail|cancel|void|refund/i, cls: 'cassaforte__badge--err', label: 'Annullato / errore' },
    ];
    const hit = map.find((m) => m.re.test(s));
    if (hit) {
      return `<span class="cassaforte__badge ${hit.cls}">${escapeHtml(hit.label)}</span>`;
    }
    return `<span class="cassaforte__badge">${escapeHtml(s || '—')}</span>`;
  }

  /**
   * @param {HTMLElement | null} el
   * @param {string} message
   * @param {'ok'|'err'|'muted'} kind
   */
  function setStatus(el, message, kind) {
    if (!el) return;
    el.textContent = message;
    el.dataset.kind = kind;
    el.hidden = !message;
  }

  async function refreshOrders() {
    const tbody = document.querySelector('[data-orders-tbody]');
    const status = document.querySelector('[data-api-status]');
    if (!tbody) return;

    if (!getToken()) {
      tbody.innerHTML = '';
      setStatus(status, 'Inserisci il secret API nella barra laterale per caricare gli ordini da D1.', 'muted');
      return;
    }

    setStatus(status, 'Caricamento ordini…', 'muted');
    try {
      const res = await adminFetch('/orders?limit=50', { method: 'GET' });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg =
          typeof data.message === 'string'
            ? data.message
            : typeof data.error === 'string'
              ? data.error
              : `HTTP ${res.status}`;
        setStatus(status, `Ordini: ${msg}`, 'err');
        tbody.innerHTML = '';
        return;
      }

      const orders = Array.isArray(data.orders) ? data.orders : [];
      if (orders.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="5" class="cassaforte__muted">Nessun ordine trovato.</td></tr>';
      } else {
        tbody.innerHTML = orders
          .map((o) => {
            const id = escapeHtml(String(o.id ?? ''));
            const email = escapeHtml(String(o.customer_email ?? '—'));
            const createdRaw = String(o.created_at ?? '');
            const total = formatMoney(
              typeof o.total_cents === 'number' ? o.total_cents : Number(o.total_cents),
              String(o.currency ?? 'EUR')
            );
            const badge = orderStatusBadge(String(o.status ?? ''));
            return `
            <tr>
              <td><code class="cassaforte__muted">${id}</code></td>
              <td>${email}</td>
              <td class="cassaforte__muted">${escapeHtml(formatDate(createdRaw))}</td>
              <td>${escapeHtml(total)}</td>
              <td>${badge}</td>
            </tr>`;
          })
          .join('');
      }
      setStatus(status, `Ordini aggiornati (${orders.length}).`, 'ok');
    } catch (e) {
      setStatus(status, e instanceof Error ? e.message : 'Errete di rete', 'err');
      tbody.innerHTML = '';
    }
  }

  async function refreshProducts() {
    const tbody = document.querySelector('[data-products-tbody]');
    const status = document.querySelector('[data-api-status]');
    if (!tbody) return;

    if (!getToken()) {
      tbody.innerHTML = '';
      setStatus(status, 'Inserisci il secret API per caricare il catalogo da D1.', 'muted');
      return;
    }

    setStatus(status, 'Caricamento prodotti…', 'muted');
    try {
      const res = await adminFetch('/products', { method: 'GET' });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg =
          typeof data.message === 'string'
            ? data.message
            : typeof data.error === 'string'
              ? data.error
              : `HTTP ${res.status}`;
        setStatus(status, `Prodotti: ${msg}`, 'err');
        tbody.innerHTML = '';
        return;
      }

      const products = Array.isArray(data.products) ? data.products : [];
      if (products.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="5" class="cassaforte__muted">Nessun prodotto nel database.</td></tr>';
      } else {
        tbody.innerHTML = products
          .map((p) => {
            const id = Number(p.id);
            const active = Number(p.active) === 1;
            const badge = active
              ? '<span class="cassaforte__badge cassaforte__badge--ok">Attivo</span>'
              : '<span class="cassaforte__badge cassaforte__badge--err">Disattivo</span>';
            const r2 = p.r2_key
              ? `<span class="cassaforte__muted" title="${escapeHtml(String(p.r2_key))}">R2 ✓</span>`
              : '<span class="cassaforte__muted">—</span>';
            return `
            <tr>
              <td><code class="cassaforte__muted">${escapeHtml(String(p.id ?? ''))}</code></td>
              <td>
                <div><strong>${escapeHtml(String(p.title_it ?? ''))}</strong></div>
                <div class="cassaforte__muted" style="font-size:0.75rem;margin-top:0.15rem">${escapeHtml(
                  String(p.slug ?? '')
                )}</div>
                <div class="cassaforte__muted" style="font-size:0.75rem;margin-top:0.15rem">${escapeHtml(
                  String(p.title_en ?? '')
                )}</div>
              </td>
              <td>${escapeHtml(formatMoney(Number(p.price_cents), String(p.currency ?? 'EUR')))}</td>
              <td>${badge}<div style="margin-top:0.35rem">${r2}</div></td>
              <td>
                <button type="button" class="cassaforte__btn" data-toggle-active data-product-id="${escapeHtml(
                  String(id)
                )}" data-active="${active ? '1' : '0'}">
                  ${active ? 'Disattiva' : 'Attiva'}
                </button>
              </td>
            </tr>`;
          })
          .join('');
      }
      setStatus(status, `Prodotti aggiornati (${products.length}).`, 'ok');
    } catch (e) {
      setStatus(status, e instanceof Error ? e.message : 'Errore di rete', 'err');
      tbody.innerHTML = '';
    }
  }

  function wireAuthPanel() {
    const input = document.querySelector('[data-admin-token-input]');
    const save = document.querySelector('[data-admin-token-save]');
    const clear = document.querySelector('[data-admin-token-clear]');
    const reload = document.querySelector('[data-admin-reload]');

    save?.addEventListener('click', () => {
      if (!(input instanceof HTMLInputElement)) return;
      setToken(input.value);
      void refreshOrders();
      void refreshProducts();
    });

    clear?.addEventListener('click', () => {
      clearToken();
      if (input instanceof HTMLInputElement) input.value = '';
      void refreshOrders();
      void refreshProducts();
    });

    reload?.addEventListener('click', () => {
      void refreshOrders();
      void refreshProducts();
    });

    if (input instanceof HTMLInputElement && getToken()) {
      input.value = getToken();
    }
  }

  function wireProductTableActions() {
    document.addEventListener('click', async (e) => {
      const t = e.target;
      if (!(t instanceof Element)) return;
      const btn = t.closest('[data-toggle-active]');
      if (!(btn instanceof HTMLButtonElement)) return;

      const id = btn.getAttribute('data-product-id');
      if (!id) return;
      const cur = btn.getAttribute('data-active') === '1';
      if (!getToken()) {
        alert('Salva prima il secret API nella sidebar.');
        return;
      }

      btn.disabled = true;
      try {
        const res = await adminFetch(`/products/${encodeURIComponent(id)}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ active: !cur }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          const msg = typeof data.message === 'string' ? data.message : data.error || `HTTP ${res.status}`;
          alert(msg);
          return;
        }
        await refreshProducts();
      } finally {
        btn.disabled = false;
      }
    });
  }

  function wireProductDialog() {
    const dialog = document.querySelector('[data-product-dialog]');
    const openBtn = document.querySelector('[data-open-product-dialog]');
    const closeEls = document.querySelectorAll('[data-close-product-dialog]');
    const form = document.querySelector('[data-product-create-form]');
    const toast = document.querySelector('[data-product-json-preview]');
    const toastPre = toast?.querySelector('pre');

    if (!(dialog instanceof HTMLDialogElement)) return;

    openBtn?.addEventListener('click', () => {
      dialog.showModal();
      const first = dialog.querySelector('input, textarea, button');
      if (first instanceof HTMLElement) first.focus();
    });

    closeEls.forEach((el) => {
      el.addEventListener('click', () => dialog.close());
    });

    dialog.addEventListener('cancel', (e) => {
      e.preventDefault();
      dialog.close();
    });

    if (!(form instanceof HTMLFormElement)) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (!getToken()) {
        alert('Salva il secret API nella sidebar prima di inviare dati a D1.');
        return;
      }

      const fd = new FormData(form);
      const priceCents = parseEurosToCents(fd.get('price_eur'));
      const slug = String(fd.get('slug') ?? '').trim();
      const fulfillmentRaw = String(fd.get('fulfillment') ?? 'digital').toLowerCase();
      const fulfillment = fulfillmentRaw === 'physical' ? 'physical' : 'digital';

      const file = fd.get('digital_file');
      const hasFile = file instanceof File && file.size > 0;

      const coverTrim = String(fd.get('cover_image') ?? '').trim();
      const cover_image = coverTrim || undefined;

      if (!Number.isFinite(priceCents)) {
        alert('Prezzo non valido: inserisci un importo in euro (es. 19,90).');
        return;
      }

      const payload = {
        slug: slug || undefined,
        title_it: String(fd.get('name_it') ?? '').trim(),
        title_en: String(fd.get('name_en') ?? '').trim(),
        title_fr: String(fd.get('name_fr') ?? '').trim(),
        title_de: String(fd.get('name_de') ?? '').trim(),
        title_es: String(fd.get('name_es') ?? '').trim(),
        description: String(fd.get('description') ?? '').trim(),
        price_cents: priceCents,
        fulfillment,
        active: true,
        ...(cover_image ? { cover_image } : {}),
      };

      if (toastPre) {
        toastPre.textContent = JSON.stringify({ ...payload, digital_file: hasFile ? '(upload separato)' : null }, null, 2);
      }
      toast?.classList.add('is-visible');

      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn instanceof HTMLButtonElement) submitBtn.disabled = true;

      try {
        const res = await adminFetch('/products', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          const msg = typeof data.message === 'string' ? data.message : data.error || `HTTP ${res.status}`;
          if (toastPre) toastPre.textContent = JSON.stringify({ error: msg, details: data }, null, 2);
          return;
        }

        const product = data.product && typeof data.product === 'object' ? data.product : null;
        const newId = product && product.id != null ? Number(product.id) : NaN;

        if (hasFile && Number.isFinite(newId)) {
          const up = new FormData();
          up.set('file', file);
          const upRes = await adminFetch(`/products/${encodeURIComponent(String(newId))}/upload`, {
            method: 'POST',
            body: up,
          });
          const upData = await upRes.json().catch(() => ({}));
          if (!upRes.ok) {
            const msg =
              typeof upData.message === 'string' ? upData.message : upData.error || `HTTP ${upRes.status}`;
            if (toastPre) {
              toastPre.textContent = JSON.stringify(
                { warning: 'Prodotto creato ma upload fallito', upload: upData, product },
                null,
                2
              );
            }
            alert(`Prodotto creato (id ${newId}), upload: ${msg}`);
          } else if (toastPre) {
            toastPre.textContent = JSON.stringify({ created: data, upload: upData }, null, 2);
          }
        } else if (toastPre) {
          toastPre.textContent = JSON.stringify(data, null, 2);
        }

        form.reset();
        dialog.close();
        await refreshProducts();
      } catch (err) {
        if (toastPre) {
          toastPre.textContent = JSON.stringify(
            { error: err instanceof Error ? err.message : 'network' },
            null,
            2
          );
        }
      } finally {
        if (submitBtn instanceof HTMLButtonElement) submitBtn.disabled = false;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    wireAuthPanel();
    wireProductDialog();
    wireProductTableActions();
    void refreshOrders();
    void refreshProducts();
  });
})();
