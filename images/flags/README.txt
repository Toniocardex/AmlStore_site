Icone bandiera in SVG, servite in locale al posto di CDN esterne.
Codici file: it, fr, de, es, pt, nl, gb (EN -> gb come nel selettore lingua).

Vengono mostrate sempre ritagliate a cerchio (border-radius:50% +
object-fit:cover) a 20px nel selettore lingua, 18px nelle voci del menu e
20px nel banner <aml-lang-suggest>. Conta quindi solo il quadrato centrale
di ogni bandiera: gli emblemi di es e pt cadono dentro il ritaglio, ma
spostarli o ingrandirli li porterebbe fuori.

Ogni file usa il viewBox del rapporto ufficiale (3:2, tranne de 5:3 e
gb 1:2) e non ha width/height: le dimensioni le detta il CSS.

Se si modifica un file, rilanciare `python scripts/bump-asset-version.py`:
le pagine referenziano le bandiere con ?v=<hash> e senza il bump i browser
servirebbero la versione in cache (vedi /images/flags/*.svg in _headers).
