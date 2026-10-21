#!/usr/bin/env python3
"""Copia la guía rápida del cliente al sitio (docs/guia/).

La guía se escribe en el repositorio del firmware, en docs/guia-cliente/. Allí,
guia.html es un fragmento: empieza con <title> y <style> y no lleva <!doctype>,
<html>, <head> ni <body>. Este script arma la página completa alrededor del
fragmento, como hace build_pdf.py para los PDF, y le añade lo propio del sitio:

- el icono de la pestaña y la descripción para buscadores;
- los enlaces a los dos PDF, debajo del título;
- un aviso con el enlace a Batería y seguridad, al final del capítulo de la
  batería, y otro a Soporte y Garantía, al final de los problemas frecuentes;
- la navegación del sitio en el pie de página;
- las fuentes del sistema en lugar de las de Google Fonts: quita el @import de
  fonts.googleapis.com del fragmento y redefine las variables de tipografía con
  las mismas pilas que docs/assets/sitio.css, para que la página no pida nada a
  terceros (política de privacidad, §13). Los PDF no cambian: llevan sus
  fuentes incrustadas y no las piden a nadie.

Copia también las imágenes que la página usa (img/) y los dos PDF. Para
regenerar los PDF, usa build_pdf.py en el repositorio de origen antes de
importar.

Uso:
    python3 tools/importar_guia.py /ruta/a/MeridianV/docs/guia-cliente
"""

from __future__ import annotations

import pathlib
import re
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEST = REPO / "docs" / "guia"

PDFS = ("guia-meridianv-iphone.pdf", "guia-meridianv-android.pdf")

SITE_CSS = REPO / "docs" / "assets" / "sitio.css"

# El @import de Google Fonts que trae el fragmento de la guía.
GOOGLE_FONTS_IMPORT = re.compile(r'@import url\("https://fonts\.(?:googleapis|gstatic)\.com/[^"]*"\);\n?')

DESCRIPTION = (
    "Guía rápida del receptor GNSS MeridianV con la app TresVizo Field para "
    "iPhone y Android: conectar, altura de antena, IMU, correcciones, medir, "
    "batería, firmware y posproceso."
)

PAGE = """<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="img/tresvizo-marca.png">
{head}
<style>
/* Añadido por el sitio: página completa sin margen, descargas bajo el título y navegación en el pie */
/* Fuentes del sistema, las mismas de docs/assets/sitio.css: la página no carga tipografías de terceros */
:root {{
  --f-display: {f_display};
  --f-body: {f_body};
  --f-mono: {f_mono};
  --f-oled: {f_mono};
}}
body {{ margin: 0; }}
.downloads {{ margin-top: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem 0.75rem; align-items: center; font-size: var(--t-s); }}
.downloads span {{ color: var(--ink-2); }}
.downloads a {{ display: inline-flex; align-items: center; min-height: 40px; padding: 0.35rem 0.9rem; border: 1px solid var(--action); border-radius: 999px; font-weight: 600; text-decoration: none; }}
.downloads a:hover {{ background: var(--action-soft); }}
.site-nav {{ display: flex; flex-wrap: wrap; gap: 0.25rem 1.25rem; width: 100%; }}
.site-nav a {{ display: inline-block; padding-block: 0.35rem; text-decoration: none; }}
.site-nav a:hover {{ text-decoration: underline; }}
@media print {{ .downloads, .site-nav {{ display: none !important; }} }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

DOWNLOADS = """
    <p class="downloads"><span>Para imprimir:</span><a href="guia-meridianv-iphone.pdf" download>PDF para iPhone</a><a href="guia-meridianv-android.pdf" download>PDF para Android</a></p>"""

SITE_NAV = """  <nav class="site-nav" aria-label="Sitio">
    <a href="../">Inicio</a>
    <a href="../soporte/">Soporte</a>
    <a href="../garantia/">Garantía</a>
    <a href="../seguridad/">Batería y seguridad</a>
    <a href="../geoides/">Geoides y sistemas</a>
    <a href="../licencia/">Contrato de licencia</a>
    <a href="../privacidad/">Política de privacidad</a>
  </nav>
"""

# Al final del capítulo de batería: los avisos de seguridad.
BATTERY_NOTE = """  <div class="note" style="margin-top:1.75rem">
    <p class="note-title">Cuida la batería</p>
    <p>Cómo cargar, guardar y transportar el receptor y su batería de litio, y qué hacer si se daña: <a href="../seguridad/">Batería y seguridad</a>.</p>
  </div>
"""

# Al final de los problemas frecuentes: soporte y garantía.
HELP_NOTE = """  <div class="note" style="margin-top:1rem">
    <p class="note-title">¿No se resolvió?</p>
    <p>Escríbenos con los datos que pide la página de <a href="../soporte/">Soporte</a>. Si el receptor necesita reparación, lee la <a href="../garantia/">Garantía</a>.</p>
  </div>
"""


def site_fonts() -> dict[str, str]:
    """Las pilas de fuentes del sistema de docs/assets/sitio.css (--f-display, --f-body, --f-mono)."""
    css = SITE_CSS.read_text(encoding="utf-8")
    fonts = {}
    for name in ("display", "body", "mono"):
        found = re.search(rf"--f-{name}:\s*([^;]+);", css)
        if not found:
            sys.exit(f"No encuentro --f-{name} en {SITE_CSS.relative_to(REPO)}.")
        fonts[f"f_{name}"] = found.group(1).strip()
    return fonts


def split_fragment(text: str) -> tuple[str, str]:
    """Separa lo que va en <head> (el <title> y el primer <style>) del cuerpo.

    A diferencia de build_pdf.py, el <script> del selector iPhone / Android se
    queda: en la web sí hace falta.
    """
    end_style = text.find("</style>")
    if not text.lstrip().startswith("<title>") or end_style < 0:
        sys.exit("guia.html debe empezar con <title> y llevar un <style>.")
    end_style += len("</style>")
    return text[:end_style], text[end_style:]


def insert_once(text: str, anchor: str, addition: str, *, before: bool = False) -> str:
    """Inserta `addition` junto a la única aparición de `anchor`."""
    if text.count(anchor) != 1:
        sys.exit(f"No encuentro una sola vez «{anchor}» en guia.html: revisa el script.")
    replacement = addition + anchor if before else anchor + addition
    return text.replace(anchor, replacement, 1)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1]).expanduser().resolve()
    fragment = src / "guia.html"
    if not fragment.is_file():
        sys.exit(f"No existe {fragment}")

    head, body = split_fragment(fragment.read_text(encoding="utf-8"))
    # Sin tipografías de terceros: fuera el @import de Google Fonts.
    head = GOOGLE_FONTS_IMPORT.sub("", head)
    if "fonts.googleapis.com" in head or "fonts.gstatic.com" in head:
        sys.exit("guia.html pide fuentes a Google de una forma que este script no reconoce: revísalo.")

    # Los PDF, debajo de la nota del selector de teléfono.
    hint_start = body.find('<p class="os-hint">')
    if hint_start < 0:
        sys.exit('No encuentro <p class="os-hint"> en guia.html: revisa el script.')
    hint_end = body.find("</p>", hint_start) + len("</p>")
    body = body[:hint_end] + DOWNLOADS + body[hint_end:]

    # Avisos de batería y la ayuda, al final de sus capítulos.
    body = insert_once(body, "</section>\n\n<!-- 8 · Firmware -->", BATTERY_NOTE, before=True)
    body = insert_once(body, "</section>\n\n</main>", HELP_NOTE, before=True)

    # La navegación del sitio, al final del pie.
    body = insert_once(body, "</footer>", SITE_NAV, before=True)

    page = PAGE.format(description=DESCRIPTION, head=head.strip(), body=body.strip(), **site_fonts())

    # Solo las imágenes que la página usa: una captura que la guía dejó de
    # enseñar no se publica.
    images = sorted(set(re.findall(r'src="(img/[^"]+)"', page)))
    missing = [name for name in images if not (src / name).is_file()]
    if missing:
        sys.exit("Faltan imágenes en el origen: " + ", ".join(missing))

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    (DEST / "index.html").write_text(page, encoding="utf-8")
    for name in images:
        (DEST / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / name, DEST / name)
    for name in PDFS:
        shutil.copy2(src / name, DEST / name)

    files = sorted(p for p in DEST.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in files) / 1024 / 1024
    print(f"docs/guia/: {len(files)} archivos, {size:.1f} MB")


if __name__ == "__main__":
    main()
