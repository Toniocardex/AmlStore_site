/**
 * home.js — logica esclusiva delle pagine index (tutte le lingue).
 * - FAQ: animazione smooth open/close su <details> con transizione height
 * - Trustpilot TrustBox: caricamento solo dopo consenso marketing (ad_storage)
 */
(function () {
  'use strict';

  var CONSENT_KEY = 'aml-consent-v2';
  var TRUSTPILOT_SCRIPT_ID = 'trustpilot-widget-script';
  var TRUSTPILOT_SCRIPT_SRC = 'https://widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js';

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

  /* ── Trustpilot — post-consenso marketing ────────────────── */
  function readMarketingConsent() {
    try {
      var raw = localStorage.getItem(CONSENT_KEY);
      if (!raw) return false;
      var parsed = JSON.parse(raw);
      var consent = parsed && parsed.consent;
      return consent && consent.ad_storage === 'granted';
    } catch (_) {
      return false;
    }
  }

  function getTrustpilotWidget() {
    return document.getElementById('trustpilot-widget') || document.querySelector('.trustpilot-widget');
  }

  function setWidgetActive(active) {
    var widget = getTrustpilotWidget();
    if (widget) widget.classList.toggle('trustpilot-widget--active', active);
  }

  function hideTrustpilotFallback() {
    var fallback = document.querySelector('.home-social-proof__fallback');
    if (fallback) fallback.hidden = true;
  }

  function loadTrustpilotWidget() {
    var widget = getTrustpilotWidget();
    if (!widget) return;

    var businessUnitId = (widget.getAttribute('data-businessunit-id') || '').trim();
    if (!businessUnitId) return;

    setWidgetActive(true);

    function bootstrapWidget() {
      if (window.Trustpilot && typeof window.Trustpilot.loadFromElement === 'function') {
        window.Trustpilot.loadFromElement(widget, true);
        hideTrustpilotFallback();
      }
    }

    if (document.getElementById(TRUSTPILOT_SCRIPT_ID)) {
      bootstrapWidget();
      return;
    }

    var script = document.createElement('script');
    script.id = TRUSTPILOT_SCRIPT_ID;
    script.src = TRUSTPILOT_SCRIPT_SRC;
    script.async = true;
    script.onload = bootstrapWidget;
    document.head.appendChild(script);
  }

  function initTrustpilot() {
    if (!readMarketingConsent()) {
      setWidgetActive(false);
      return;
    }
    loadTrustpilotWidget();
  }

  function onConsentUpdated(event) {
    var consent = event && event.detail;
    if (consent && consent.ad_storage === 'granted') {
      loadTrustpilotWidget();
    } else if (consent) {
      setWidgetActive(false);
    }
  }

  /* ── Init ────────────────────────────────────────────────── */
  function init() {
    initFaqAnimation();
    initTrustpilot();
    window.addEventListener('aml-consent-updated', onConsentUpdated);
    window.addEventListener('storage', function (e) {
      if (e.key === CONSENT_KEY && readMarketingConsent()) {
        loadTrustpilotWidget();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
