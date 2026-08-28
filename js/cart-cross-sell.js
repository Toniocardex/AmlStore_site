/**
 * Motore di cross-sell del carrello.
 *
 * Legge asset/cross-sell/{lang}.json (generato da scripts/build-cross-sell-index.py),
 * confronta il contenuto del carrello con una matrice di affinità fra famiglie di
 * prodotto e propone fino a 3 add-on complementari, uno per famiglia.
 *
 * Regole, in ordine di applicazione:
 *  1. esclusioni dure — già nel carrello, stessa famiglia di un articolo presente,
 *     bundle (contengono un secondo prodotto e si sovrappongono), fisici quando il
 *     carrello è tutto digitale (aggiungerebbero un indirizzo di spedizione);
 *  2. affinità — ogni articolo nel carrello vota le famiglie complementari;
 *  3. prezzo — un add-on costa meno dell'articolo più caro del carrello, altrimenti
 *     non è un add-on ma un secondo acquisto;
 *  4. dedup — un solo candidato per famiglia, i primi 3 per punteggio.
 *
 * Nessun candidato → il pannello resta nascosto: meglio niente che un consiglio a caso.
 */
(function (global) {
    'use strict';

    const EVT = 'aml-cart-changed';
    const TRACK_URL = '/api/track';
    const MAX_SUGGESTIONS = 3;

    /* ─── Regole di affinità ───────────────────────────────────────────────────── */

    /**
     * famiglia nel carrello → famiglie complementari, con peso.
     * Le famiglie sono assegnate dall'indice a partire dalla categoria di
     * catalog.json (vedi FAMILY_BY_CATEGORY nello script di build).
     * Nessun arco verso se stessa: un secondo antivirus non è un add-on.
     */
    const AFFINITY = {
        windows:    { antivirus: 1.00, office: 0.85, m365: 0.80, backup: 0.55, tools: 0.35 },
        server:     { antivirus: 0.70, backup: 0.75, tools: 0.45, office: 0.30 },
        office:     { antivirus: 1.00, tools: 0.60, backup: 0.50, windows: 0.30 },
        m365:       { antivirus: 1.00, tools: 0.55, backup: 0.50, windows: 0.30 },
        antivirus:  { office: 0.85, m365: 0.80, backup: 0.65, tools: 0.40, windows: 0.30 },
        backup:     { antivirus: 0.80, office: 0.45, m365: 0.45, tools: 0.35 },
        tools:      { office: 0.60, m365: 0.55, antivirus: 0.55, backup: 0.35 },
        multimedia: { tools: 0.55, antivirus: 0.45, backup: 0.40 },
    };

    /**
     * Peso di partenza per famiglia quando l'affinità non produce candidati
     * (carrello con famiglie sconosciute o tutte le complementari già dentro).
     * Vale come ordinamento di ripiego, non come raccomandazione forte.
     */
    const FALLBACK_WEIGHT = { antivirus: 0.30, office: 0.25, m365: 0.25, backup: 0.20, tools: 0.15 };

    /** Un add-on costa meno del pezzo forte del carrello: oltre, non è più un add-on. */
    function priceFactor(candidateMinor, maxCartUnitMinor) {
        if (!(maxCartUnitMinor > 0) || !(candidateMinor > 0)) return 1;
        const ratio = candidateMinor / maxCartUnitMinor;
        if (ratio <= 0.60) return 1.15;
        if (ratio <= 1.00) return 1.00;
        if (ratio <= 1.50) return 0.55;
        return 0.20;
    }

    /**
     * Calcola i suggerimenti. Funzione pura: nessun DOM, nessun fetch — così è
     * verificabile a parte (vedi scripts/test-cross-sell.mjs).
     * @param {Array<object>} catalog voci di asset/cross-sell/{lang}.json
     * @param {Array<object>} lines righe del carrello (AmlCart.getItems())
     * @param {number} [limit]
     * @returns {Array<object>} voci di catalogo, ordinate per rilevanza
     */
    function pickSuggestions(catalog, lines, limit) {
        const max = limit > 0 ? limit : MAX_SUGGESTIONS;
        if (!Array.isArray(catalog) || !catalog.length) return [];
        if (!Array.isArray(lines) || !lines.length) return [];

        const bySku = Object.create(null);
        catalog.forEach((p) => { if (p && p.sku) bySku[p.sku] = p; });

        const skusInCart = Object.create(null);
        const familiesInCart = Object.create(null);
        var cartHasPhysical = false;
        var maxCartUnitMinor = 0;

        lines.forEach((l) => {
            const sku = l && l.sku;
            if (!sku) return;
            skusInCart[sku] = true;
            if (l.physical) cartHasPhysical = true;
            const unit = Number(l.unitAmount) || 0;
            if (unit > maxCartUnitMinor) maxCartUnitMinor = unit;
            const known = bySku[sku];
            if (known && known.family) familiesInCart[known.family] = true;
        });

        // Voti di affinità: ogni articolo del carrello vota le famiglie complementari,
        // si tiene il voto più alto ricevuto (non la somma: due antivirus nel carrello
        // non rendono la suite office due volte più pertinente).
        const familyScore = Object.create(null);
        Object.keys(familiesInCart).forEach((fam) => {
            const targets = AFFINITY[fam];
            if (!targets) return;
            Object.keys(targets).forEach((target) => {
                if (familiesInCart[target]) return;
                if (!(familyScore[target] > targets[target])) familyScore[target] = targets[target];
            });
        });

        if (!Object.keys(familyScore).length) {
            Object.keys(FALLBACK_WEIGHT).forEach((fam) => {
                if (familiesInCart[fam]) return;
                familyScore[fam] = FALLBACK_WEIGHT[fam];
            });
        }

        const scored = [];
        catalog.forEach((p) => {
            if (!p || !p.sku) return;
            if (skusInCart[p.sku]) return;
            if (p.bundle) return;
            if (familiesInCart[p.family]) return;
            if (p.physical && !cartHasPhysical) return;
            const base = familyScore[p.family];
            if (!(base > 0)) return;

            var score = base * priceFactor(p.priceMinor, maxCartUnitMinor);
            // Piccola spinta a chi è in promozione: è l'offerta che rende
            // credibile un add-on proposto a carrello già pieno.
            if (p.compareAtMinor > p.priceMinor) score *= 1.08;
            scored.push({ product: p, score: score });
        });

        // Ordine deterministico: punteggio, poi prezzo crescente, poi sku.
        scored.sort((a, b) => (
            b.score - a.score
            || a.product.priceMinor - b.product.priceMinor
            || (a.product.sku < b.product.sku ? -1 : a.product.sku > b.product.sku ? 1 : 0)
        ));

        const out = [];
        const usedFamilies = Object.create(null);
        for (var i = 0; i < scored.length && out.length < max; i++) {
            const p = scored[i].product;
            if (usedFamilies[p.family]) continue;
            usedFamilies[p.family] = true;
            out.push(p);
        }
        return out;
    }

    // Esposto anche fuori dal browser per i test unitari.
    global.AmlCrossSell = { pickSuggestions: pickSuggestions, AFFINITY: AFFINITY };

    if (typeof document === 'undefined') return;

    /* ─── Rendering ────────────────────────────────────────────────────────────── */

    function trackEvent(eventName, extra) {
        try {
            fetch(TRACK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true,
                body: JSON.stringify(Object.assign({ event: eventName }, extra || {})),
            }).catch(() => {});
        } catch (_) { /* fetch non disponibile */ }
    }

    function initCrossSell() {
        const mount = document.getElementById('aml-cart-crosssell');
        if (!mount || mount.dataset.amlCrossSellInit) return;
        mount.dataset.amlCrossSellInit = '1';

        const listEl = mount.querySelector('.cart-crosssell__list');
        if (!listEl) return;

        const S = global.AmlSite;
        const loc = S ? S.parseLocalePath(global.location.pathname) : null;
        const lang = (loc && loc.langCode) || 'it';
        const pathPrefix = (loc && loc.pathPrefix) || '';
        const staticRoot = S ? S.staticRootFromScriptPath('/js/cart-cross-sell.js') : '';

        const addLabel = mount.getAttribute('data-label-add') || 'Add';
        const addedLabel = mount.getAttribute('data-label-added') || 'Added';
        const saveLabel = mount.getAttribute('data-label-save') || 'You save';

        var catalog = null;
        var addedFlashTimer = null;
        // Sospende il re-render mentre il pulsante mostra la conferma: AmlCart.add
        // emette `aml-cart-changed` in modo sincrono, quindi senza questo flag il
        // pannello si ridisegnerebbe prima ancora che la conferma sia visibile.
        var flashing = false;
        const viewedSkus = Object.create(null);
        var shownPicks = [];
        // Il pannello sta sotto la lista articoli — su mobile perfino sotto la CTA
        // di checkout — quindi "disegnato" non vuol dire "visto": senza questa
        // distinzione `cross_sell_view` scatterebbe su ogni caricamento con
        // carrello pieno e il rapporto add/view misurerebbe le pageview, non le
        // proposte davvero guardate.
        var panelSeen = false;

        /** Una impression per sku e per pagina, solo dopo che il pannello e' entrato nel viewport. */
        function flushImpressions() {
            if (!panelSeen) return;
            shownPicks.forEach((entry) => {
                if (viewedSkus[entry.sku]) return;
                viewedSkus[entry.sku] = true;
                trackEvent('cross_sell_view', { sku: entry.sku });
            });
        }

        /** Almeno il 40% del pannello (o del viewport, se il pannello e' piu' alto) a schermo. */
        function panelInViewport() {
            const r = mount.getBoundingClientRect();
            if (!r.height) return false; // ancora hidden: nessun box da misurare
            const vh = global.innerHeight || (document.documentElement || {}).clientHeight || 0;
            if (!vh) return false;
            const visible = Math.min(r.bottom, vh) - Math.max(r.top, 0);
            return visible > 0 && visible >= Math.min(r.height, vh) * 0.4;
        }

        var visibilityTick = null;
        var visibilityObserver = null;

        /** Idempotente: i due segnali di visibilita' convergono qui. */
        function markPanelSeen() {
            if (panelSeen) return;
            panelSeen = true;
            stopWatchingVisibility();
            flushImpressions();
        }

        function checkVisibility() {
            visibilityTick = null;
            if (panelSeen || mount.hidden || !panelInViewport()) return;
            markPanelSeen();
        }

        // Misura al massimo una volta per frame: `scroll` spara a raffica e
        // getBoundingClientRect() forza il layout.
        function scheduleVisibilityCheck() {
            if (panelSeen || visibilityTick !== null) return;
            if (typeof requestAnimationFrame === 'function') {
                visibilityTick = requestAnimationFrame(checkVisibility);
            } else {
                visibilityTick = setTimeout(checkVisibility, 100);
            }
        }

        function stopWatchingVisibility() {
            if (visibilityObserver) {
                visibilityObserver.disconnect();
                visibilityObserver = null;
            }
            global.removeEventListener('scroll', scheduleVisibilityCheck);
            global.removeEventListener('resize', scheduleVisibilityCheck);
        }

        /**
         * Due segnali, perche' nessuno dei due basta da solo.
         *
         * IntersectionObserver e' quello corretto e copre anche il caso che allo
         * scroll sfugge: il pannello che entra in vista per un reflow — un banner
         * chiuso sopra di lui, un'immagine che finisce di caricare — senza che
         * scatti nessun evento.
         *
         * Il controllo geometrico serve dove l'observer non consegna mai una
         * entry, nemmeno quella iniziale: succede nei contesti che non dipingono
         * la pagina (anteprime headless, browser incorporati), dove senza fallback
         * la metrica sparirebbe in silenzio. Perdere le impression e' peggio che
         * contarle male.
         */
        function watchVisibility() {
            if (typeof IntersectionObserver === 'function') {
                visibilityObserver = new IntersectionObserver(function (entries) {
                    if (entries.some((en) => en.isIntersecting)) markPanelSeen();
                }, { threshold: 0.4 });
                visibilityObserver.observe(mount);
            }
            global.addEventListener('scroll', scheduleVisibilityCheck, { passive: true });
            global.addEventListener('resize', scheduleVisibilityCheck, { passive: true });
            scheduleVisibilityCheck();
        }

        function productHref(entry) {
            return S ? S.localePageUrl(pathPrefix, lang, entry.slug) : '/' + lang + '/' + entry.slug;
        }

        function formatMoney(minor, currency) {
            return (global.AmlCart && global.AmlCart.formatMoney)
                ? global.AmlCart.formatMoney(minor, currency)
                : String(Math.round(minor) / 100);
        }

        function buildCard(entry) {
            const card = document.createElement('article');
            card.className = 'cart-crosssell__card';

            const link = document.createElement('a');
            link.className = 'cart-crosssell__link';
            link.href = productHref(entry);

            const media = document.createElement('span');
            media.className = 'cart-crosssell__media';
            const img = document.createElement('img');
            img.src = staticRoot + entry.image;
            img.alt = '';
            img.loading = 'lazy';
            img.decoding = 'async';
            img.width = 64;
            img.height = 64;
            media.appendChild(img);
            link.appendChild(media);

            const info = document.createElement('span');
            info.className = 'cart-crosssell__info';

            const name = document.createElement('span');
            name.className = 'cart-crosssell__name';
            name.textContent = entry.name;
            info.appendChild(name);

            if (entry.specs) {
                const specs = document.createElement('span');
                specs.className = 'cart-crosssell__specs';
                specs.textContent = entry.specs;
                info.appendChild(specs);
            }
            link.appendChild(info);
            card.appendChild(link);

            const foot = document.createElement('div');
            foot.className = 'cart-crosssell__foot';

            const priceBox = document.createElement('div');
            priceBox.className = 'cart-crosssell__prices';

            const price = document.createElement('span');
            price.className = 'cart-crosssell__price';
            price.textContent = formatMoney(entry.priceMinor, entry.currency);
            priceBox.appendChild(price);

            if (entry.compareAtMinor > entry.priceMinor) {
                const was = document.createElement('span');
                was.className = 'cart-crosssell__was';
                was.textContent = formatMoney(entry.compareAtMinor, entry.currency);
                priceBox.appendChild(was);

                const save = document.createElement('span');
                save.className = 'cart-crosssell__save';
                save.textContent = saveLabel + ' '
                    + formatMoney(entry.compareAtMinor - entry.priceMinor, entry.currency);
                priceBox.appendChild(save);
            }
            foot.appendChild(priceBox);

            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'cart-crosssell__add';
            btn.setAttribute('data-crosssell-sku', entry.sku);
            btn.textContent = addLabel;
            btn.setAttribute('aria-label', addLabel + ': ' + entry.name);
            foot.appendChild(btn);

            card.appendChild(foot);
            return card;
        }

        function render() {
            if (!catalog) return;
            const lines = (global.AmlCart && global.AmlCart.getItems) ? global.AmlCart.getItems() : [];
            const picks = pickSuggestions(catalog, lines, MAX_SUGGESTIONS);

            listEl.textContent = '';
            if (!picks.length) {
                mount.hidden = true;
                return;
            }
            mount.hidden = false;
            picks.forEach((entry) => listEl.appendChild(buildCard(entry)));

            shownPicks = picks;
            // Il pannello puo' essere gia' a schermo appena smette di essere
            // hidden (carrello con una riga sola, schermo alto): senza questo
            // controllo l'impression arriverebbe solo al primo scroll.
            scheduleVisibilityCheck();
            flushImpressions();
        }

        listEl.addEventListener('click', function (e) {
            const btn = e.target && e.target.closest ? e.target.closest('[data-crosssell-sku]') : null;
            if (!btn || !catalog) return;
            const sku = btn.getAttribute('data-crosssell-sku');
            const entry = catalog.find((p) => p.sku === sku);
            if (!entry || !global.AmlCart || !global.AmlCart.add) return;

            flashing = true;
            const added = global.AmlCart.add({
                sku: entry.sku,
                name: entry.name,
                currency: entry.currency,
                unitAmount: entry.priceMinor,
                quantity: 1,
                // staticRoot come per productHref(): sotto un deploy con prefisso
                // di path la riga di carrello deve puntare all'immagine prefissata,
                // altrimenti la miniatura e' rotta (l.image e' truthy, quindi il
                // fallback di cart.js non scatta).
                image: staticRoot + entry.image,
                productPath: productHref(entry),
                specs: entry.specs || '',
                physical: Boolean(entry.physical),
            });
            if (!added) {
                flashing = false;
                return;
            }

            trackEvent('cross_sell_add', { sku: entry.sku });
            // Conferma sul posto, poi il pannello si ridisegna: la card sparisce
            // perché lo sku è ormai nel carrello, che è la riga appena comparsa
            // nell'elenco qui sopra.
            btn.classList.add('is-added');
            btn.textContent = addedLabel;
            btn.disabled = true;
            clearTimeout(addedFlashTimer);
            addedFlashTimer = setTimeout(function () {
                addedFlashTimer = null;
                flashing = false;
                render();
            }, 900);
        });

        // Ridisegna a ogni modifica del carrello, ma non durante il flash di conferma.
        document.addEventListener(EVT, function () {
            if (flashing) return;
            render();
        });

        watchVisibility();

        fetch(staticRoot + '/asset/cross-sell/' + lang + '.json')
            .then((res) => { if (!res.ok) throw new Error('HTTP ' + res.status); return res.json(); })
            .then((data) => {
                catalog = Array.isArray(data) ? data : [];
                render();
            })
            .catch(() => { catalog = []; mount.hidden = true; });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCrossSell);
    } else {
        initCrossSell();
    }

})(typeof window !== 'undefined' ? window : globalThis);
