/**
 * home.js — logica esclusiva delle pagine index (tutte le lingue).
 * - FAQ: animazione smooth open/close su <details> con transizione height
 * - Scroll progress: barra fissa in cima che avanza con lo scroll
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

  /* ── Scroll progress bar ─────────────────────────────────── */
  function initScrollProgress() {
    var bar = document.querySelector('.scroll-progress');
    if (!bar) return;

    var pending = false;
    function update() {
      var scrolled = window.scrollY;
      var total    = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (total > 0 ? scrolled / total : 0) + ')';
      pending = false;
    }

    window.addEventListener('scroll', function () {
      if (!pending) {
        pending = true;
        requestAnimationFrame(update);
      }
    }, { passive: true });
  }

  /* ── Init ────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initFaqAnimation();
      initScrollProgress();
    });
  } else {
    initFaqAnimation();
    initScrollProgress();
  }
}());
