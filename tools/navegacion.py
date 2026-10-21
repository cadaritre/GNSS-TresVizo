#!/usr/bin/env python3
"""Escribe la misma cabecera y el mismo pie en todas las páginas del sitio.

Cada página de docs/ lleva un <header class="topbar"> y un <footer class="foot">.
Este script los sustituye por los de las plantillas de abajo, con las rutas
relativas que tocan a cada página y la marca de la página actual en el menú.
Así, para agregar una página al menú se cambia una sola lista.

La guía rápida (docs/guia/) tiene su propia barra, con el selector de
iPhone / Android, y su pie lo escribe tools/importar_guia.py.

La página 404 se sirve desde cualquier ruta que no exista, así que sus enlaces
son absolutos y dependen del nombre del repositorio (BASE). Si el sitio pasa a
un dominio propio, cambia BASE por "/".

Uso:
    python3 tools/navegacion.py
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
BASE = "/GNSS-TresVizo/"

# (carpeta, rótulo en la barra de arriba)
TOPNAV = (
    ("guia/", "Guía rápida"),
    ("soporte/", "Soporte"),
    ("garantia/", "Garantía"),
    ("geoides/", "Geoides"),
)

# (carpeta, rótulo en el pie); "" es la portada.
FOOTNAV = (
    ("", "Inicio"),
    ("guia/", "Guía rápida"),
    ("soporte/", "Soporte"),
    ("garantia/", "Garantía"),
    ("seguridad/", "Batería y seguridad"),
    ("geoides/", "Geoides y sistemas"),
    ("licencia/", "Contrato de licencia"),
    ("privacidad/", "Política de privacidad"),
)

HEADER = """<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="{p}"><img src="{p}assets/img/tresvizo-marca.png" alt="" width="385" height="444"><span>TresVizo GNSS</span></a>
    <nav class="topnav" aria-label="Sitio">
{links}
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="foot">
  <div class="wrap foot-in">
    <img src="{p}assets/img/tresvizo-logo.png" alt="TresVizo" width="990" height="444">
    <nav aria-label="Documentos">
{links}
      <a href="https://www.tresvizo.com/">tresvizo.com</a>
    </nav>
    <p class="fine">© 2026 TresVizo. Receptores GNSS MeridianV y MeridianVI · TresVizo Field para iPhone y Android.</p>
  </div>
</footer>"""


def pages() -> list[tuple[pathlib.Path, str, str]]:
    """(archivo, prefijo de las rutas, carpeta de la página) de cada página."""
    found = [(DOCS / "index.html", "./", ""), (DOCS / "404.html", BASE, None)]
    for page in sorted(DOCS.glob("*/index.html")):
        folder = page.parent.name + "/"
        if folder in ("guia/", "assets/"):
            continue
        found.append((page, "../", folder))
    return found


def render(prefix: str, current: str | None) -> tuple[str, str]:
    def link(folder: str, label: str, indent: str) -> str:
        mark = ' aria-current="page"' if folder == current else ""
        return f'{indent}<a href="{prefix}{folder}"{mark}>{label}</a>'

    top = "\n".join(link(f, label, "      ") for f, label in TOPNAV)
    foot = "\n".join(link(f, label, "      ") for f, label in FOOTNAV)
    return HEADER.format(p=prefix, links=top), FOOTER.format(p=prefix, links=foot)


def main() -> None:
    for page, prefix, current in pages():
        text = page.read_text(encoding="utf-8")
        header, footer = render(prefix, current)
        new, n_head = re.subn(r'<header class="topbar">.*?</header>', lambda _: header, text, count=1, flags=re.S)
        new, n_foot = re.subn(r'<footer class="foot">.*?</footer>', lambda _: footer, new, count=1, flags=re.S)
        if n_head != 1 or n_foot != 1:
            sys.exit(f"{page.relative_to(REPO)}: falta <header class=\"topbar\"> o <footer class=\"foot\">")
        if new != text:
            page.write_text(new, encoding="utf-8")
        print(f"{page.relative_to(REPO)}: {'actualizada' if new != text else 'sin cambios'}")


if __name__ == "__main__":
    main()
