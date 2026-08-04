/**
 * Invio richieste di consulenza verso la Pages Function same-origin.
 * Non registra né invia dati personali ad analytics.
 */
(function () {
    'use strict';

    function value(formData, key) {
        return String(formData.get(key) || '').trim();
    }

    function setStatus(status, state, message) {
        status.dataset.state = state;
        status.textContent = message;
    }

    document.querySelectorAll('[data-consultation-form]').forEach(function (form) {
        const submit = form.querySelector('.consultation-submit');
        const status = form.querySelector('.consultation-form-status');
        if (!submit || !status) return;

        submit.disabled = false;

        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            if (!form.reportValidity()) return;

            const formData = new FormData(form);
            const payload = {
                firstName: value(formData, 'firstName'),
                lastName: value(formData, 'lastName'),
                company: value(formData, 'company'),
                email: value(formData, 'email'),
                topic: value(formData, 'topic'),
                seats: value(formData, 'seats'),
                message: value(formData, 'message'),
                privacy: formData.get('privacy') === 'on',
                website: value(formData, 'website'),
                locale: form.dataset.locale || document.documentElement.lang || 'it',
                sourcePath: window.location.pathname,
            };

            const originalLabel = submit.textContent;
            submit.disabled = true;
            submit.setAttribute('aria-busy', 'true');
            submit.textContent = form.dataset.sending || originalLabel;
            setStatus(status, 'pending', form.dataset.sending || originalLabel);

            try {
                const response = await fetch(form.action || '/api/consultation-request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const result = await response.json().catch(function () { return {}; });
                if (!response.ok || !result.ok) throw new Error('request_failed');

                const baseMessage = result.dryRun
                    ? (form.dataset.dryRun || form.dataset.success)
                    : form.dataset.success;
                const reference = result.reference
                    ? ` ${form.dataset.reference || 'Reference'}: ${result.reference}.`
                    : '';
                setStatus(status, 'success', `${baseMessage || ''}${reference}`.trim());
                form.reset();
            } catch (_) {
                setStatus(status, 'error', form.dataset.error || 'Unable to send the request.');
            } finally {
                submit.disabled = false;
                submit.removeAttribute('aria-busy');
                submit.textContent = originalLabel;
            }
        });
    });
})();
