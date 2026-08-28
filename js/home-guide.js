/**
 * home-guide.js — "Guida all'acquisto" della home.
 *
 * Il file gestisce DUE schemi di markup, scelti in automatico:
 *
 *  1. WIZARD (prototipo /it, 2026-08-28) — albero decisionale a profondita'
 *     variabile. Ogni pannello e' un [data-guide-step] con un id; i bottoni
 *     [data-guide-option] o proseguono (data-guide-next="id-passo") oppure
 *     chiudono il percorso con una raccomandazione (data-result-*). Le domande
 *     sono sulla situazione del cliente, non sulla categoria di prodotto, e il
 *     risultato porta il "perche'", un eventuale caveat e le alternative.
 *
 *  2. LEGACY (en, fr, de, es, nl, pt) — le due domande a cascata originali:
 *     step 1 categoria, step 2 opzioni della categoria. Resta finche' il
 *     prototipo non viene promosso e tradotto.
 *
 * Il contenuto delle raccomandazioni non e' nel JS ma negli attributi data-
 * del markup, cosi' resta tradotto insieme alla pagina e non serve un
 * dizionario per lingua qui dentro.
 */
(function () {
    'use strict';

    var IMG_BASE = '../asset/media/products/';
    var IMG_FALLBACK = '../asset/media/product-cover-fallback.webp';

    /* ── Wizard ─────────────────────────────────────────────────────────── */

    function initWizard(root) {
        var steps = {};
        root.querySelectorAll('[data-guide-step]').forEach(function (el) {
            steps[el.getAttribute('data-guide-step')] = el;
        });
        if (!steps.root) return;

        var trail = root.querySelector('[data-guide-trail]');
        var bar = root.querySelector('[data-guide-progress]');
        var barLabel = root.querySelector('[data-guide-progress-label]');
        var resetBtn = root.querySelector('[data-guide-reset]');
        var result = root.querySelector('[data-guide-result]');
        var intro = root.querySelector('[data-guide-intro]');
        var card = root.querySelector('[data-guide-card]');
        var image = root.querySelector('[data-guide-image]');
        var title = root.querySelector('[data-guide-title]');
        var why = root.querySelector('[data-guide-why]');
        var note = root.querySelector('[data-guide-note]');
        var link = root.querySelector('[data-guide-link]');
        var altLink = root.querySelector('[data-guide-alt]');
        var compareLink = root.querySelector('[data-guide-compare]');
        if (!result || !card || !title || !why || !link) return;

        /* Percorso corrente: un elemento per domanda gia' risposta, con il
           passo in cui e' stata posta e il bottone scelto. Serve sia al
           filo di Arianna sia al "torna indietro". */
        var path = [];
        var current = 'root';

        /* Quanti passi mancano al piu' lungo finale raggiungibile da qui.
           Il totale mostrato nel progresso non e' fisso perche' i rami hanno
           profondita' diverse: il ramo "supporto fisico" di Windows si chiude
           al secondo passo, quello Office arriva al terzo. Il risultato viene
           memorizzato: l'albero non cambia dopo il caricamento. */
        var depthCache = {};
        function depthFrom(id, seen) {
            if (depthCache[id] !== undefined) return depthCache[id];
            var step = steps[id];
            if (!step) return 0;
            seen = seen || {};
            if (seen[id]) return 0; /* guardia contro un albero mal scritto */
            seen[id] = true;
            var deepest = 0;
            step.querySelectorAll('[data-guide-option]').forEach(function (btn) {
                var next = btn.getAttribute('data-guide-next');
                var d = next ? depthFrom(next, seen) : 0;
                if (d > deepest) deepest = d;
            });
            depthCache[id] = 1 + deepest;
            return depthCache[id];
        }

        function paintProgress(done) {
            if (!bar) return;
            var segs = bar.querySelectorAll('.home-guide__progress-seg');
            var index = path.length;                       /* passi conclusi */
            var total = done ? index : index + depthFrom(current);
            if (total < 1) total = 1;

            segs.forEach(function (seg, i) {
                seg.classList.toggle('is-on', done ? true : i <= index);
                seg.classList.toggle('is-done', i < index);
                /* I segmenti oltre la profondita' del ramo scelto non
                   servono: sparirebbe il senso di "3 di 3" su un ramo da 2. */
                seg.hidden = i >= Math.max(total, 1);
            });
            if (barLabel) {
                barLabel.textContent = done
                    ? 'Fatto'
                    : 'Passo ' + (index + 1) + ' di ' + total;
            }
        }

        function paintTrail() {
            if (!trail) return;
            trail.textContent = '';
            trail.hidden = path.length === 0;
            path.forEach(function (entry, i) {
                var li = document.createElement('li');
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'home-guide__crumb';
                btn.textContent = entry.chip;
                btn.title = 'Torna a questa domanda';
                btn.addEventListener('click', function () {
                    rewindTo(i);
                });
                li.appendChild(btn);
                trail.appendChild(li);
            });
        }

        function clearSelection(stepId) {
            var step = steps[stepId];
            if (!step) return;
            step.querySelectorAll('[data-guide-option]').forEach(function (b) {
                b.classList.remove('is-selected');
                b.setAttribute('aria-pressed', 'false');
            });
        }

        function showStep(id, focus) {
            current = id;
            Object.keys(steps).forEach(function (key) {
                steps[key].hidden = key !== id;
            });
            result.classList.add('is-empty');
            if (intro) intro.hidden = false;
            card.hidden = true;
            paintProgress(false);
            if (focus) {
                var q = steps[id].querySelector('.home-guide__question');
                if (q) q.focus();
            }
        }

        function rewindTo(index) {
            /* Le scelte da questo punto in poi non valgono piu': vanno tolte
               anche dai pannelli, altrimenti tornando avanti si troverebbero
               ancora evidenziate. */
            var target = path[index];
            path.slice(index).forEach(function (entry) {
                clearSelection(entry.stepId);
            });
            path = path.slice(0, index);
            paintTrail();
            if (resetBtn) resetBtn.hidden = path.length === 0;
            showStep(target.stepId, true);
        }

        function reset() {
            path.slice().forEach(function (entry) {
                clearSelection(entry.stepId);
            });
            clearSelection('root');
            path = [];
            paintTrail();
            if (resetBtn) resetBtn.hidden = true;
            showStep('root', true);
        }

        function text(el, value) {
            if (!el) return;
            el.textContent = value || '';
            el.hidden = !value;
        }

        function anchor(el, href, label) {
            if (!el) return;
            if (href && label) {
                el.setAttribute('href', href);
                el.textContent = label;
                el.hidden = false;
            } else {
                el.hidden = true;
            }
        }

        function showResult(btn) {
            var slug = btn.getAttribute('data-result-href');
            title.textContent = btn.getAttribute('data-result-title') || '';
            why.textContent = btn.getAttribute('data-result-why') || '';
            text(note, btn.getAttribute('data-result-note'));
            if (slug) link.setAttribute('href', slug);

            if (image && slug) {
                /* Il nome file immagine coincide sempre con lo slug prodotto,
                   come per le card di tutto il sito: non serve un attributo
                   dati separato solo per l'immagine. L'onerror va riagganciato
                   a ogni cambio perche' il gestore si disattiva da solo dopo
                   il primo fallimento, per non entrare in ciclo. */
                image.onerror = function () {
                    image.onerror = null;
                    image.src = IMG_FALLBACK;
                };
                /* Il lazy loading ha senso finche' il pannello e' fermo sul
                   testo introduttivo, sotto la piega. Da qui in poi no: il
                   cliente sta gia' guardando il risultato, e l'immagine che
                   compare in ritardo si vedrebbe entrare. */
                image.removeAttribute('loading');
                image.src = IMG_BASE + slug + '.webp';
            }

            anchor(altLink, btn.getAttribute('data-result-alt-href'), btn.getAttribute('data-result-alt-label'));
            anchor(compareLink, btn.getAttribute('data-result-compare-href'), btn.getAttribute('data-result-compare-label'));

            if (intro) intro.hidden = true;
            card.hidden = false;
            result.classList.remove('is-empty');
            paintProgress(true);

            /* Il focus porta l'annuncio allo screen reader, lo scroll porta il
               pannello sotto gli occhi di tutti gli altri: su mobile le due
               colonne diventano una sola e il risultato nasce sotto la piega,
               quindi senza questo il cliente vedrebbe solo l'opzione premuta.
               preventScroll evita che i due meccanismi si accavallino. */
            title.focus({ preventScroll: true });
            var box = card.getBoundingClientRect();
            if (box.top < 0 || box.bottom > window.innerHeight) {
                var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
                card.scrollIntoView({ block: 'nearest', behavior: still ? 'auto' : 'smooth' });
            }
        }

        root.querySelectorAll('[data-guide-option]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var step = btn.closest('[data-guide-step]');
                if (!step) return;
                var stepId = step.getAttribute('data-guide-step');

                /* Rispondere di nuovo a una domanda gia' risposta (via filo di
                   Arianna) invalida tutto quello che veniva dopo. */
                var already = -1;
                path.forEach(function (entry, i) {
                    if (entry.stepId === stepId && already < 0) already = i;
                });
                if (already >= 0) {
                    path.slice(already).forEach(function (entry) {
                        clearSelection(entry.stepId);
                    });
                    path = path.slice(0, already);
                }

                clearSelection(stepId);
                btn.classList.add('is-selected');
                btn.setAttribute('aria-pressed', 'true');

                path.push({
                    stepId: stepId,
                    chip: btn.getAttribute('data-guide-chip') || btn.textContent.trim()
                });
                paintTrail();
                if (resetBtn) resetBtn.hidden = false;

                var next = btn.getAttribute('data-guide-next');
                if (next && steps[next]) showStep(next, true);
                else showResult(btn);
            });
        });

        if (resetBtn) resetBtn.addEventListener('click', reset);

        showStep('root', false);
        if (resetBtn) resetBtn.hidden = true;
    }

    /* ── Legacy: due domande a cascata ──────────────────────────────────── */

    function initLegacy(root) {
        var categories = root.querySelectorAll('[data-guide-category]');
        var groups = root.querySelectorAll('[data-guide-group]');
        var title = root.querySelector('[data-guide-title]');
        var body = root.querySelector('[data-guide-body]');
        var link = root.querySelector('[data-guide-link]');
        var image = root.querySelector('[data-guide-image]');
        if (!categories.length || !groups.length || !title || !body || !link) return;

        function showResult(btn) {
            var group = btn.closest('[data-guide-group]');
            if (group) {
                group.querySelectorAll('[data-guide-option]').forEach(function (b) {
                    var on = b === btn;
                    b.classList.toggle('is-selected', on);
                    b.setAttribute('aria-pressed', on ? 'true' : 'false');
                });
            }
            title.textContent = btn.getAttribute('data-guide-title-value') || title.textContent;
            body.textContent = btn.getAttribute('data-guide-body-value') || body.textContent;
            var href = btn.getAttribute('data-guide-href');
            if (href) {
                link.setAttribute('href', href);
                if (image) image.src = IMG_BASE + href + '.webp';
            }
        }

        function selectCategory(btn) {
            var key = btn.getAttribute('data-guide-category');

            categories.forEach(function (b) {
                var on = b === btn;
                b.classList.toggle('is-selected', on);
                b.setAttribute('aria-pressed', on ? 'true' : 'false');
            });

            groups.forEach(function (group) {
                var on = group.getAttribute('data-guide-group') === key;
                group.hidden = !on;
                /* Cambiando categoria il consiglio mostrato apparterrebbe ancora
                   a quella precedente: si riparte dalla prima opzione del nuovo
                   gruppo, cosi' il pannello resta coerente con la scelta. */
                if (on) {
                    var first = group.querySelector('[data-guide-option]');
                    if (first) showResult(first);
                }
            });
        }

        categories.forEach(function (btn) {
            btn.addEventListener('click', function () {
                selectCategory(btn);
            });
        });

        root.querySelectorAll('[data-guide-option]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                showResult(btn);
            });
        });
    }

    function init() {
        var root = document.querySelector('[data-home-guide]');
        if (!root) return;
        if (root.querySelector('[data-guide-step]')) initWizard(root);
        else initLegacy(root);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
