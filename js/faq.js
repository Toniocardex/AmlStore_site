/** Shared FAQ accordion behavior for homepage and product pages. */
(function () {
    'use strict';

    function initFaqAnimation() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        document.querySelectorAll('.home-faq-item').forEach(function (details) {
            var summary = details.querySelector('summary');
            var body = details.querySelector('.home-faq-body');
            if (!summary || !body || details.dataset.faqReady === 'true') return;

            details.dataset.faqReady = 'true';
            summary.addEventListener('click', function (event) {
                event.preventDefault();

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
                    return;
                }

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
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFaqAnimation);
    } else {
        initFaqAnimation();
    }
}());
