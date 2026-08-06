#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WIN_HOME = {
    "it": {
        "title": "Windows 11 Home per uso quotidiano",
        "gallery_aria": "Anteprima interfaccia",
        "bento_title": "Menu Start centrale",
    },
    "en": {
        "title": "Windows 11 Home for everyday use",
        "gallery_aria": "Interface preview",
        "bento_title": "Centred Start menu",
    },
    "fr": {
        "title": "Windows 11 Home pour un usage quotidien",
        "gallery_aria": "Aperçu de l'interface",
        "bento_title": "Menu Démarrer centré",
    },
    "de": {
        "title": "Windows 11 Home für den Alltag",
        "gallery_aria": "Oberflächenvorschau",
        "bento_title": "Zentriertes Startmenü",
    },
    "es": {
        "title": "Windows 11 Home para el uso diario",
        "gallery_aria": "Vista previa de la interfaz",
        "bento_title": "Menú Inicio centrado",
    },
}

PROJECT = {
    "en": (
        "Windows: at least 1.6 GHz dual-core. Mac: Intel or Apple Silicon compatible with a supported macOS (where the SKU is PC/Mac).",
        "At least 1.6 GHz dual-core processor (Windows).",
        "Windows 10/11; macOS versions supported by Microsoft for the indicated suite.",
        "Windows 10 or Windows 11.",
    ),
    "it": (
        "Windows: almeno 1,6 GHz dual‑core. Mac: Intel o Apple Silicon compatibili con macOS supportato (dove la scheda indica PC/Mac).",
        "Processore almeno 1,6 GHz dual-core (Windows).",
        "Windows 10/11; macOS nelle versioni supportate da Microsoft per la suite indicata.",
        "Windows 10 o Windows 11.",
    ),
    "fr": (
        "Windows : au moins 1,6 GHz dual-core. Mac : Intel ou Apple Silicon compatibles avec un macOS pris en charge (si la fiche indique PC/Mac).",
        "Processeur au moins 1,6 GHz dual-core (Windows).",
        "Windows 10/11 ; versions macOS prises en charge par Microsoft pour la suite indiquée.",
        "Windows 10 ou Windows 11.",
    ),
    "de": (
        "Windows: mindestens 1,6 GHz Dual-Core. Mac: Intel oder Apple Silicon mit unterstütztem macOS (wo PC/Mac angegeben).",
        "Mindestens 1,6 GHz Dual-Core-Prozessor (Windows).",
        "Windows 10/11; von Microsoft für die genannte Suite unterstützte macOS-Versionen.",
        "Windows 10 oder Windows 11.",
    ),
    "es": (
        "Windows: al menos 1,6 GHz dual-core. Mac: Intel o Apple Silicon con macOS compatible (si la ficha indica PC/Mac).",
        "Procesador de al menos 1,6 GHz dual-core (Windows).",
        "Windows 10/11; versiones de macOS admitidas por Microsoft para la suite indicada.",
        "Windows 10 o Windows 11.",
    ),
}


def fix_windows() -> None:
    for lang, r in WIN_HOME.items():
        p = ROOT / lang / "windows-11-home.html"
        t = p.read_text(encoding="utf-8")
        t = t.replace(
            '<h2 id="pdp-features-title" class="pdp-sec__title">None</h2>',
            f'<h2 id="pdp-features-title" class="pdp-sec__title">{r["title"]}</h2>',
            1,
        )
        t = t.replace('aria-label="None"', f'aria-label="{r["gallery_aria"]}"', 1)
        t = t.replace(
            '<h3 class="bento-title">None</h3>',
            f'<h3 class="bento-title">{r["bento_title"]}</h3>',
            1,
        )
        left = t.count(">None<") + t.count('aria-label="None"')
        p.write_text(t, encoding="utf-8", newline="\n")
        print(f"windows-11-home {lang}: remaining None={left}")


def fix_project() -> None:
    for lang, (old_cpu, new_cpu, old_os, new_os) in PROJECT.items():
        p = ROOT / lang / "project-standard-2024.html"
        t = p.read_text(encoding="utf-8")
        if old_cpu not in t:
            # IT may use special hyphen
            alt = old_cpu.replace("dual‑core", "dual-core").replace("dual-core", "dual‑core")
            if alt in t:
                old_cpu = alt
            else:
                print(f"project {lang}: CPU pattern MISSING")
                continue
        t = t.replace(old_cpu, new_cpu).replace(old_os, new_os)
        p.write_text(t, encoding="utf-8", newline="\n")
        leftover = "macOS" in t or "Mac:" in t or " Mac " in t
        print(f"project {lang}: {'LEFTOVER mac/Mac' if leftover else 'ok'}")


if __name__ == "__main__":
    fix_windows()
    fix_project()
