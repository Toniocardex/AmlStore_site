/* Logica URL/locale condivisa: caricare prima di header.js e footer.js. */
(function (global) {
    'use strict';

    const LANGS = [
        { code: 'it', label: 'IT', flag: 'it' },
        { code: 'en', label: 'EN', flag: 'gb' },
        { code: 'fr', label: 'FR', flag: 'fr' },
        { code: 'de', label: 'DE', flag: 'de' },
        { code: 'es', label: 'ES', flag: 'es' },
    ];

    function isKnownLangCode(segment) {
        return LANGS.some((l) => l.code === segment);
    }

    function parseLocalePath(pathname) {
        const segments = String(pathname || '').split('/').filter(Boolean);
        const langCode = segments.find((seg) => isKnownLangCode(seg)) || 'it';
        const activeLang = LANGS.find((l) => l.code === langCode) || LANGS[0];
        const langSegIdx = segments.indexOf(activeLang.code);
        const pathPrefix = langSegIdx > 0 ? '/' + segments.slice(0, langSegIdx).join('/') : '';
        const pathAfterLang = langSegIdx >= 0 ? segments.slice(langSegIdx + 1).join('/') : '';
        return { segments, langCode, activeLang, langSegIdx, pathPrefix, pathAfterLang };
    }

    function homeHref(pathPrefix, langCode) {
        const middle = pathPrefix ? `${pathPrefix}/${langCode}` : `/${langCode}`;
        return `${middle}/`;
    }

    /** Path sotto la lingua, es. `cart.html` o `microsoft-365-family.html` (senza slash iniziale). */
    function localePageUrl(pathPrefix, langCode, pathAfterLang) {
        const middle = pathPrefix ? `${pathPrefix}/${langCode}` : `/${langCode}`;
        const tail = String(pathAfterLang || '').replace(/^\/+/, '');
        return tail ? `${middle}/${tail}` : `${middle}/`;
    }

    function hrefSwitchLocale(pathPrefix, langCode, pathAfterLang, search, hash) {
        const qsAndHash = (search || '') + (hash || '');
        const middle = pathPrefix ? `${pathPrefix}/${langCode}` : `/${langCode}`;
        const path = pathAfterLang ? `${middle}/${pathAfterLang}` : `${middle}/`;
        return path + qsAndHash;
    }

    function escapeHtmlAttr(text) {
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function staticRootFromScriptPath(needle) {
        const scripts = document.scripts;
        for (let i = 0; i < scripts.length; i++) {
            const raw = scripts[i].getAttribute('src');
            if (!raw) continue;
            let pathname;
            try {
                pathname = new URL(raw, global.location.href).pathname;
            } catch (_) {
                continue;
            }
            if (!pathname.endsWith(needle)) continue;
            return pathname.slice(0, -needle.length);
        }
        return '';
    }

    global.AmlSite = {
        LANGS,
        defaultLangCode: 'it',
        parseLocalePath,
        homeHref,
        localePageUrl,
        hrefSwitchLocale,
        escapeHtmlAttr,
        staticRootFromScriptPath,
    };
})(typeof window !== 'undefined' ? window : globalThis);
