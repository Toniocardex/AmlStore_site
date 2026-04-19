import pathlib, re

ROOT = pathlib.Path(r"C:\Users\Antonio\Desktop\Aml-Store_Site")

# ── HTML ─────────────────────────────────────────────────────────────────────
html_path = ROOT / "it" / "microsoft-365-family.html"
html = html_path.read_text(encoding="utf-8")

NEW_HERO = (
    '        <section class="product-hero" aria-label="Prodotto e acquisto">\n'
    '            <div class="product-hero__left">\n'
    '                <header class="product-header">\n'
    '                    <div class="product-badges">\n'
    '                        <span class="badge bestseller">Bestseller</span>\n'
    '                        <span class="badge popular">\u26a1 Oltre 200 acquisti</span>\n'
    '                        <span class="badge digital">Consegna digitale</span>\n'
    '                    </div>\n'
    '                    <h1 class="product-title">Microsoft 365 Family \u2014 Abbonamento 12 mesi</h1>\n'
    '                    <p class="product-desc-short">\n'
    "                        L'abbonamento ideale per tutta la famiglia: fino a 6 persone, app Office premium, 6 TB su OneDrive (1 TB a persona) e sicurezza avanzata sui dispositivi.\n"
    '                    </p>\n'
    '                </header>\n'
    '                <div class="product-feature-pills" aria-label="Caratteristiche principali">\n'
    '                    <span class="product-feature-pill">\n'
    '                        <img src="../asset/icon/img-aml-store_Teams-Icon-FY26.svg" width="18" height="18" alt="" loading="lazy" decoding="async">\n'
    '                        Fino a 6 utenti\n'
    '                    </span>\n'
    '                    <span class="product-feature-pill">\n'
    '                        <img src="../asset/icon/img-aml-store_OneDrive-Icon-FY26.svg" width="18" height="18" alt="" loading="lazy" decoding="async">\n'
    '                        1 TB per utente\n'
    '                    </span>\n'
    '                    <span class="product-feature-pill">\n'
    '                        <img src="../asset/icon/img-aml-store_Copilot-Icon-FY26.svg" width="18" height="18" alt="" loading="lazy" decoding="async">\n'
    '                        Include Copilot\n'
    '                    </span>\n'
    '                </div>\n'
    '                <div\n'
    '                    id="product-pricing"\n'
    '                    class="pricing-card"\n'
    '                    data-stripe-currency="eur"\n'
    '                    data-stripe-unit-amount="9900"\n'
    '                    data-stripe-compare-at-amount="12900"\n'
    '                    data-stripe-product-sku="microsoft-365-family-12m"\n'
    '                    data-discount-percent="23"\n'
    '                >\n'
    '                    <div class="price-section">\n'
    "                        <div class=\"price-block\" role=\"group\" aria-label=\"Prezzi dell'offerta\">\n"
    '                            <div class="price-block__row price-block__row--original">\n'
    '                                <span class="price-block__label">Prezzo originale</span>\n'
    '                                <span class="price-block__msrp">\u20ac 129,00</span>\n'
    '                            </div>\n'
    '                            <div class="price-block__row price-block__row--offer">\n'
    '                                <span class="price-block__label">Il nostro prezzo</span>\n'
    '                                <div class="price-block__offer-line">\n'
    '                                    <span class="price-block__sale">\u20ac 99,00</span>\n'
    '                                    <span class="price-block__save" title="Risparmio rispetto al prezzo originale">\u221223%</span>\n'
    '                                </div>\n'
    '                            </div>\n'
    '                        </div>\n'
    '                        <div class="tax-info">Tasse incluse. Nessun costo di spedizione.</div>\n'
    '                        <div class="price-compare" aria-label="Confronto prezzo">\n'
    '                            <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" width="14" height="14"><path d="M13 5H3l1-3h8l1 3zM3 5l2 8h6l2-8" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M6 9h4M8 7v4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>\n'
    '                            Risparmi <strong>\u20ac\u00a030</strong> rispetto al prezzo Microsoft Store ufficiale (\u20ac\u00a0129,00).\n'
    '                        </div>\n'
    '                    </div>\n'
    '                    <div class="action-buttons">\n'
    '                        <button type="button" id="product-primary-cta" class="btn-primary" data-cart-add data-cart-source="product-pricing">\n'
    '                            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>\n'
    '                            Aggiungi al carrello\n'
    '                        </button>\n'
    '                    </div>\n'
    '                    <div class="payment-methods" aria-label="Metodi di pagamento accettati">\n'
    '                        <span class="payment-methods__logo" title="Visa"><img src="../asset/payments_logo/img-aml-store_Visa_logo.svg" width="56" height="18" alt="Visa" loading="lazy" decoding="async"></span>\n'
    '                        <span class="payment-methods__logo" title="Mastercard"><img src="../asset/payments_logo/img-aml-store_Mastercard_logo.svg" width="40" height="18" alt="Mastercard" loading="lazy" decoding="async"></span>\n'
    '                        <span class="payment-methods__logo" title="PayPal"><img src="../asset/payments_logo/img-aml-store_PayPal-logo.svg" width="72" height="18" alt="PayPal" loading="lazy" decoding="async"></span>\n'
    '                        <span class="payment-methods__logo" title="Apple Pay"><img src="../asset/payments_logo/img-aml-store_Apple_Pay_logo.svg" width="48" height="18" alt="Apple Pay" loading="lazy" decoding="async"></span>\n'
    '                        <span class="payment-methods__logo" title="Google Pay"><img src="../asset/payments_logo/img-aml-store_Google_Pay_Logo.svg" width="52" height="18" alt="Google Pay" loading="lazy" decoding="async"></span>\n'
    '                        <span class="payment-methods__logo" title="Stripe"><img src="../asset/payments_logo/img-aml-store_Stripe_Logo.svg" width="56" height="18" alt="Stripe" loading="lazy" decoding="async"></span>\n'
    '                    </div>\n'
    '                    <div class="trust-list">\n'
    '                        <div class="trust-item">\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>\n'
    '                            Licenza originale al 100%\n'
    '                        </div>\n'
    '                        <div class="trust-item">\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>\n'
    '                            Consegna via email in pochi minuti\n'
    '                        </div>\n'
    '                        <div class="trust-item">\n'
    '                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>\n'
    '                            Garanzia rimborso\n'
    '                        </div>\n'
    '                    </div>\n'
    '                </div>\n'
    '            </div>\n'
    '            <div class="product-hero__right">\n'
    '                <img\n'
    '                    class="product-cover-img"\n'
    '                    src="../asset/media/microsoft-365-family.webp"\n'
    '                    width="400"\n'
    '                    height="400"\n'
    '                    alt="Microsoft 365 Family \u2014 grafica del prodotto"\n'
    '                    fetchpriority="high"\n'
    '                    decoding="async"\n'
    '                />\n'
    '            </div>\n'
    '        </section>'
)

NEW_FEATURE_GRID = (
    '        <section class="product-feature-grid" aria-labelledby="feature-grid-title">\n'
    '            <h2 id="feature-grid-title" class="product-section-eyebrow">Perch\u00e9 scegliere Microsoft 365 Family</h2>\n'
    '            <div class="product-feature-grid__items">\n'
    '                <div class="product-feature-grid__item">\n'
    '                    <svg class="product-feature-grid__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20H7a5 5 0 01-5-5v-1a5 5 0 015-5h1m2-3a4 4 0 118 0 4 4 0 01-8 0zm6 3h1a5 5 0 015 5v1a5 5 0 01-5 5h-1"/></svg>\n'
    '                    <h3>Per te e altre 5 persone</h3>\n'
    '                    <p>Da 1 a 6 persone nello stesso piano Family, ciascuna con account Microsoft separato e impostazioni personali.</p>\n'
    '                </div>\n'
    '                <div class="product-feature-grid__item">\n'
    '                    <svg class="product-feature-grid__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>\n'
    '                    <h3>Fino a 6 TB di spazio cloud</h3>\n'
    '                    <p>Ogni persona riceve 1 TB su OneDrive. Salva, sincronizza e accedi ai tuoi file da qualsiasi dispositivo.</p>\n'
    '                </div>\n'
    '                <div class="product-feature-grid__item">\n'
    '                    <svg class="product-feature-grid__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>\n'
    '                    <h3>Sicurezza avanzata per tutti</h3>\n'
    '                    <p>Microsoft Defender incluso sulle piattaforme supportate per proteggere tutti i dispositivi della famiglia.</p>\n'
    '                </div>\n'
    '                <div class="product-feature-grid__item">\n'
    '                    <svg class="product-feature-grid__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>\n'
    '                    <h3>App sempre aggiornate</h3>\n'
    '                    <p>Word, Excel, PowerPoint, Outlook e tutte le app incluse ricevono aggiornamenti continui senza costi extra.</p>\n'
    '                </div>\n'
    '            </div>\n'
    '        </section>'
)

# Use marker-based replacement: find header start → hero section end
HERO_START = '        <header class="product-header">'
HERO_END = '        </section>'  # closing tag of product-hero

# Find the hero section boundaries
start_idx = html.find(HERO_START)
assert start_idx != -1, "Could not find product-header start"

# Find the closing </section> of product-hero (after the start)
hero_section_start = html.find('<section class="product-hero"', start_idx)
assert hero_section_start != -1, "Could not find product-hero section"
end_idx = html.find(HERO_END, hero_section_start) + len(HERO_END)
assert end_idx > start_idx, "Could not find hero section end"

html = html[:start_idx] + NEW_HERO + '\n' + html[end_idx:]
print(f"Hero replaced (chars {start_idx}–{end_idx})")

# Replace product-inline-benefits with feature grid
BENEFITS_START = '        <section class="product-inline-benefits"'
BENEFITS_END = '        </section>'
b_start = html.find(BENEFITS_START)
assert b_start != -1, "Could not find inline-benefits"
b_end = html.find(BENEFITS_END, b_start) + len(BENEFITS_END)
html = html[:b_start] + NEW_FEATURE_GRID + '\n' + html[b_end:]
print("Feature grid replaced")

html_path.write_text(html, encoding="utf-8")
print("HTML ok")

# ── CSS ──────────────────────────────────────────────────────────────────────
css_path = ROOT / "css" / "product.css"
css = css_path.read_text(encoding="utf-8")

# 1. Simplify product-header (already updated check)
old_ph = ".product-page .product-header {\n    position: relative;\n    z-index: 1;\n    max-width: 100%;\n    margin-bottom: 2.5rem;\n    display: flex;\n    flex-direction: column;\n    gap: 1.25rem;\n}"
new_ph = ".product-page .product-header {\n    display: flex;\n    flex-direction: column;\n    gap: 1.25rem;\n}"
if old_ph in css:
    css = css.replace(old_ph, new_ph)
    print("product-header CSS updated")

# 2. Restructure product-hero grid
OLD_HERO_GRID = (
    ".product-page .product-hero {\n"
    "    position: relative;\n"
    "    z-index: 1;\n"
    "    display: grid;\n"
    "    grid-template-columns: 1fr;\n"
    "    gap: clamp(1.5rem, 3vw, 3rem);\n"
    "    padding: 0 0 3rem;\n"
    "    align-items: stretch;\n"
    "}\n"
    "\n"
    "@container pp (min-width: 720px) {\n"
    "    .product-page .product-hero {\n"
    "        grid-template-columns: minmax(0, 1.35fr) minmax(min(100%, 300px), 0.95fr);\n"
    "        gap: clamp(2rem, 4vw, 5rem);\n"
    "    }\n"
    "}"
)
NEW_HERO_GRID = (
    ".product-page .product-hero {\n"
    "    position: relative;\n"
    "    z-index: 1;\n"
    "    display: grid;\n"
    "    grid-template-columns: 1fr;\n"
    "    gap: clamp(1.5rem, 3vw, 2.5rem);\n"
    "    padding: 0 0 3rem;\n"
    "    align-items: start;\n"
    "}\n"
    "\n"
    "@container pp (min-width: 720px) {\n"
    "    .product-page .product-hero {\n"
    "        grid-template-columns: minmax(0, 1fr) minmax(260px, 380px);\n"
    "        gap: clamp(2rem, 4vw, 4rem);\n"
    "    }\n"
    "}\n"
    "\n"
    ".product-page .product-hero__left {\n"
    "    display: flex;\n"
    "    flex-direction: column;\n"
    "    gap: 1.5rem;\n"
    "}\n"
    "\n"
    ".product-page .product-hero__right {\n"
    "    display: flex;\n"
    "    justify-content: center;\n"
    "    align-items: flex-start;\n"
    "}"
)
if OLD_HERO_GRID in css:
    css = css.replace(OLD_HERO_GRID, NEW_HERO_GRID)
    print("Hero grid CSS updated")
elif ".product-hero__left" not in css:
    # Try alternate version already partially updated
    alt = (
        "    gap: clamp(1.5rem, 3vw, 2.5rem);\n"
        "    padding: 0 0 3rem;\n"
        "    align-items: start;\n"
    )
    if alt in css:
        # Insert the left/right wrappers after the @container block
        insert_after = "        gap: clamp(2rem, 4vw, 4rem);\n    }\n}"
        pos = css.find(insert_after)
        if pos != -1:
            css = css[:pos+len(insert_after)] + (
                "\n\n.product-page .product-hero__left {\n"
                "    display: flex;\n"
                "    flex-direction: column;\n"
                "    gap: 1.5rem;\n"
                "}\n"
                "\n"
                ".product-page .product-hero__right {\n"
                "    display: flex;\n"
                "    justify-content: center;\n"
                "    align-items: flex-start;\n"
                "}"
            ) + css[pos+len(insert_after):]
            print("Added hero left/right wrappers")

# 3. Replace gallery/tiles CSS with pills + cover-img
if ".product-page .product-feature-pills {" not in css:
    gallery_start = css.find(".product-page .product-gallery {")
    cover_end_marker = "    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.28);\n}"
    cover_end = css.find(cover_end_marker, gallery_start)
    if gallery_start != -1 and cover_end != -1:
        end_pos = cover_end + len(cover_end_marker)
        NEW_PILLS_CSS = (
            ".product-page .product-feature-pills {\n"
            "    display: flex;\n"
            "    flex-wrap: wrap;\n"
            "    gap: 0.5rem;\n"
            "}\n"
            "\n"
            ".product-page .product-feature-pill {\n"
            "    display: inline-flex;\n"
            "    align-items: center;\n"
            "    gap: 0.45rem;\n"
            "    padding: 0.4rem 0.75rem;\n"
            "    background: color-mix(in srgb, var(--page-accent) 10%, transparent);\n"
            "    border: 1px solid color-mix(in srgb, var(--page-accent) 25%, transparent);\n"
            "    border-radius: 99px;\n"
            "    font-size: 0.8rem;\n"
            "    font-weight: 600;\n"
            "    color: var(--page-text-secondary);\n"
            "}\n"
            "\n"
            ".product-page .product-feature-pill img {\n"
            "    width: 18px;\n"
            "    height: 18px;\n"
            "    flex-shrink: 0;\n"
            "    object-fit: contain;\n"
            "}\n"
            "\n"
            ".product-page .product-cover-img {\n"
            "    width: 100%;\n"
            "    height: auto;\n"
            "    aspect-ratio: 1 / 1;\n"
            "    object-fit: contain;\n"
            "    display: block;\n"
            "    border-radius: 20px;\n"
            "    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.3);\n"
            "}"
        )
        css = css[:gallery_start] + NEW_PILLS_CSS + css[end_pos:]
        print("Gallery CSS replaced with pills")
    else:
        print(f"WARN: gallery CSS not found (gallery_start={gallery_start}, cover_end={cover_end})")

# 4. Fix pricing-card height:100%
css = css.replace(
    "    justify-content: center;\n    gap: 1.75rem;\n    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);\n    height: 100%;\n}",
    "    justify-content: flex-start;\n    gap: 1.75rem;\n    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);\n}"
)

# 5. Add feature-grid CSS before light-theme block
if ".product-feature-grid {" not in css:
    FEATURE_GRID_CSS = (
        "\n/* Feature grid 2x2 */\n"
        ".product-page .product-feature-grid {\n"
        "    padding: clamp(2rem, 4vw, 3.5rem) 0;\n"
        "    border-top: 1px solid var(--page-border);\n"
        "}\n\n"
        ".product-page .product-feature-grid .product-section-eyebrow {\n"
        "    margin-bottom: 2rem;\n"
        "}\n\n"
        ".product-page .product-feature-grid__items {\n"
        "    display: grid;\n"
        "    grid-template-columns: 1fr;\n"
        "    gap: 1.5rem 2.5rem;\n"
        "}\n\n"
        "@container pp (min-width: 600px) {\n"
        "    .product-page .product-feature-grid__items {\n"
        "        grid-template-columns: repeat(2, 1fr);\n"
        "    }\n"
        "}\n\n"
        ".product-page .product-feature-grid__item {\n"
        "    display: flex;\n"
        "    flex-direction: column;\n"
        "    gap: 0.6rem;\n"
        "}\n\n"
        ".product-page .product-feature-grid__icon {\n"
        "    width: 32px;\n"
        "    height: 32px;\n"
        "    color: var(--page-accent);\n"
        "    flex-shrink: 0;\n"
        "}\n\n"
        ".product-page .product-feature-grid__item h3 {\n"
        "    font-size: 1.05rem;\n"
        "    font-weight: 700;\n"
        "    color: var(--page-text);\n"
        "    margin: 0;\n"
        "}\n\n"
        ".product-page .product-feature-grid__item p {\n"
        "    font-size: 0.9rem;\n"
        "    line-height: 1.6;\n"
        "    color: var(--page-text-secondary);\n"
        "    margin: 0;\n"
        "}\n"
    )
    css = css.replace(
        "/* Tema chiaro: superfici e bordi prodotto */",
        FEATURE_GRID_CSS + "/* Tema chiaro: superfici e bordi prodotto */"
    )
    print("Feature grid CSS added")

# 6. Clean up stale light-theme overrides
css = css.replace(
    "html[data-theme='light'] .product-page .product-feature-tile {\n    background: rgba(0, 0, 0, 0.03);\n}\n",
    ""
)
css = css.replace(
    "html[data-theme='light'] .product-page .product-gallery {\n    background: #ffffff;\n    background-image: linear-gradient(rgba(0, 0, 0, 0.04) 1px, transparent 1px),\n        linear-gradient(90deg, rgba(0, 0, 0, 0.04) 1px, transparent 1px);\n    border-color: rgba(0, 0, 0, 0.08);\n}",
    ""
)

# 7. Clean mobile: remove old gallery rules if present
old_mobile_gallery = "    .product-page .product-gallery {"
if old_mobile_gallery in css:
    m_start = css.find(old_mobile_gallery)
    m_end = css.find("    .product-page .software-mockup", m_start)
    if m_end != -1:
        css = css[:m_start] + "    .product-page .product-cover-img {\n        max-width: 300px;\n        margin: 0 auto;\n    }\n\n" + css[m_end:]
        print("Mobile gallery rules cleaned")

css_path.write_text(css, encoding="utf-8")
print("CSS ok — done!")
