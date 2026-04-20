/**
 * home.js — logica esclusiva delle pagine index (tutte le lingue).
 * - FAQ: animazione smooth open/close su <details> con transizione height
 * (La barra scroll in cima è in js/scroll-progress.js + .scroll-progress in page.css.)
 */
(function () {
  'use strict';

  /* ── FAQ — smooth open / close ───────────────────────────── */
  function initFaqAnimation() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    document.querySelectorAll('.home-faq-item').forEach(function (details) {
      var summary = details.querySelector('summary');
      var body    = details.querySelector('.home-faq-body');
      if (!summary || !body) return;

      summary.addEventListener('click', function (e) {
        e.preventDefault();

        if (details.open) {
          /* ── chiusura ── */
          body.style.height = body.scrollHeight + 'px';
          requestAnimationFrame(function () {
            requestAnimationFrame(function () {
              body.style.height = '0';
              body.addEventListener('transitionend', function onClose() {
                body.removeEventListener('transitionend', onClose);
                details.removeAttribute('open');
                body.style.height = '';
              });
            });
          });
        } else {
          /* ── apertura ── */
          details.setAttribute('open', '');
          var target = body.scrollHeight;
          body.style.height = '0';
          requestAnimationFrame(function () {
            requestAnimationFrame(function () {
              body.style.height = target + 'px';
              body.addEventListener('transitionend', function onOpen() {
                body.removeEventListener('transitionend', onOpen);
                body.style.height = '';
              });
            });
          });
        }
      });
    });
  }

  /* ── Init ────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initFaqAnimation();
    });
  } else {
    initFaqAnimation();
  }
}());
