#!/usr/bin/env python3
"""Comprueba el sitio (docs/) antes de publicarlo. Sale con error si algo falla.

1. **Borradores.** Una página con un marcador [COMPLETAR…] o [VERIFICAR…] tiene
   que llevar arriba el recuadro de borrador (<div class="draft"> con
   «Borrador») y ese recuadro tiene que decir que el documento «no está
   vigente».
2. **Vigencia.** Una página con marcadores no puede declararse vigente: ni
   «Vigente desde:» con una fecha (solo con un marcador), ni «está vigente»,
   «es vigente», «entra en vigor» o «queda vigente» sin un «no» delante.
3. **Nada de terceros al cargar.** Ninguna página pide hojas de estilo,
   fuentes ni scripts a otro dominio (Google Fonts incluido): el sitio usa las
   fuentes del sistema y la política de privacidad lo dice (§13).
4. **Enlaces internos.** Cada href y src relativo (o absoluto con /GNSS-TresVizo/)
   lleva a un archivo de docs/, y cada #ancla existe en su página.

Lo que no es error pero conviene saber sale como «aviso».

Uso:
    python3 tools/comprobar_sitio.py
"""

from __future__ import annotations

import html
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
BASE = "/GNSS-TresVizo/"

MARKER = re.compile(r"\[(COMPLETAR|VERIFICAR)\b")
# «Vigente desde:» seguido de algo que no sea un marcador.
VIGENTE_DESDE = re.compile(r"Vigente desde:\s*(?!\[(?:COMPLETAR|VERIFICAR))\S", re.I)
# Una declaración de vigencia sin «no» delante.
# Lo que una hoja de estilos manda cargar: @import "…", @import url(…) y url(…).
CSS_URL = re.compile(r"""(?:@import\s+(?:url\(\s*)?|url\(\s*)['"]?([^'")\s]+)""")
DECLARA_VIGENCIA = re.compile(r"(?<!\bno )\b(?:está|es|queda|entra|entró) (?:vigente|en vigor)\b", re.I)

# Páginas que todavía cargan algo de terceros, con su motivo. Salen como aviso,
# no como error, y la política de privacidad lo dice. Se quitan de aquí en
# cuanto dejan de hacerlo.
EXTERNAL_ALLOWED = {
    "docs/guia/index.html": (
        "la guía publicada carga sus fuentes de Google Fonts hasta que se vuelva a importar "
        "con tools/importar_guia.py, que ya las quita (se rehace con el firmware 1.0.0)"
    ),
}


class Page(HTMLParser):
    """Lo que hace falta de una página: su texto, sus ids, sus enlaces y lo que carga."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[int, str]] = []
        self.loads: list[tuple[int, str]] = []
        self.text: list[str] = []
        self.draft_depth = 0
        self.depth = 0
        self.draft_text: list[str] = []
        self.styles: list[tuple[int, str]] = []
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        if tag in ("a", "area") and "href" in a:
            self.links.append((line, a["href"]))
        if tag == "link" and "href" in a:
            rel = a.get("rel", "").lower()
            if any(r in rel for r in ("stylesheet", "preconnect", "preload", "dns-prefetch", "icon", "manifest")):
                self.loads.append((line, a["href"]))
            else:
                self.links.append((line, a["href"]))
        for key in ("src", "srcset", "poster", "data"):
            if key in a and tag in ("img", "script", "iframe", "source", "video", "audio", "embed", "object", "track"):
                value = a[key].split(",")[0].split()[0] if key == "srcset" and a[key].strip() else a[key]
                self.loads.append((line, value))
        if tag == "style":
            self._in_style = True
        if tag not in ("br", "img", "meta", "link", "input", "hr", "source", "wbr", "col", "area", "base", "track", "embed", "param"):
            self.depth += 1
            if self.draft_depth == 0 and tag == "div" and "draft" in a.get("class", "").split():
                self.draft_depth = self.depth

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False
        if tag in ("br", "img", "meta", "link", "input", "hr", "source", "wbr", "col", "area", "base", "track", "embed", "param"):
            return
        if self.draft_depth and self.depth == self.draft_depth:
            self.draft_depth = -1  # cerrado: solo cuenta el primer recuadro
        self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.styles.append((self.getpos()[0], data))
            return
        self.text.append(data)
        if self.draft_depth > 0:
            self.draft_text.append(data)


def parse(path: pathlib.Path) -> Page:
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    page.close()
    return page


def is_external(url: str) -> bool:
    parts = urlsplit(url)
    return bool(parts.scheme in ("http", "https") or url.startswith("//"))


def resolve(page: pathlib.Path, url: str) -> tuple[pathlib.Path | None, str]:
    """El archivo de docs/ al que lleva un enlace interno, y su ancla."""
    parts = urlsplit(url)
    path = unquote(parts.path)
    if path.startswith(BASE):
        target = DOCS / path[len(BASE):]
    elif path.startswith("/"):
        return None, parts.fragment
    elif path == "":
        target = page
    else:
        target = (page.parent / path).resolve()
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, unquote(parts.fragment)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    pages = sorted(DOCS.rglob("*.html"))
    parsed = {p: parse(p) for p in pages}

    for path, page in parsed.items():
        rel = path.relative_to(REPO).as_posix()
        text = " ".join(" ".join(page.text).split())
        markers = len(MARKER.findall(text))

        # 1 y 2. Borradores y vigencia.
        if markers:
            draft = " ".join(" ".join(page.draft_text).split())
            if not draft:
                errors.append(f"{rel}: tiene {markers} marcadores [COMPLETAR/VERIFICAR] y no lleva el recuadro de borrador (<div class=\"draft\">)")
            else:
                if "Borrador" not in draft:
                    errors.append(f"{rel}: el recuadro de borrador no dice «Borrador»")
                if not re.search(r"\bno est[áa] vigente\b", draft, re.I):
                    errors.append(f"{rel}: el recuadro de borrador no dice que el documento «no está vigente»")
            for found in VIGENTE_DESDE.finditer(text):
                errors.append(f"{rel}: tiene marcadores y dice «{text[found.start():found.end() + 20].strip()}…»: no puede declararse vigente")
            for found in DECLARA_VIGENCIA.finditer(text):
                around = text[max(0, found.start() - 40):found.end() + 20].strip()
                errors.append(f"{rel}: tiene marcadores y se declara vigente: «…{around}…»")

        # 3. Nada de terceros al cargar.
        external = [(line, url) for line, url in page.loads if is_external(url)]
        for line, css in page.styles:
            external += [(line + css[:found.start()].count("\n"), found.group(1)) for found in CSS_URL.finditer(css)
                         if is_external(found.group(1))]
        for line, url in external:
            if rel in EXTERNAL_ALLOWED:
                warnings.append(f"{rel}:{line}: carga {url} ({EXTERNAL_ALLOWED[rel]})")
            else:
                errors.append(f"{rel}:{line}: carga un recurso de otro dominio: {url}")

        # 4. Enlaces internos.
        for line, url in page.links + page.loads:
            url = html.unescape(url).strip()
            if not url or is_external(url) or url.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            target, anchor = resolve(path, url)
            if target is None:
                errors.append(f"{rel}:{line}: enlace absoluto fuera del sitio: {url}")
                continue
            try:
                target.relative_to(DOCS)
            except ValueError:
                errors.append(f"{rel}:{line}: el enlace sale de docs/: {url}")
                continue
            if not target.is_file():
                errors.append(f"{rel}:{line}: enlace roto: {url}")
                continue
            if anchor and target.suffix == ".html":
                ids = parsed[target].ids if target in parsed else parse(target).ids
                if anchor not in ids:
                    errors.append(f"{rel}:{line}: el ancla #{anchor} no existe en {target.relative_to(REPO).as_posix()}")

    # Lo mismo en las hojas de estilo del sitio.
    for css_path in sorted(DOCS.rglob("*.css")):
        rel = css_path.relative_to(REPO).as_posix()
        css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css_path.read_text(encoding="utf-8"), flags=re.S)
        for found in CSS_URL.finditer(css):
            if is_external(found.group(1)):
                errors.append(f"{rel}:{css[:found.start()].count(chr(10)) + 1}: carga un recurso de otro dominio: {found.group(1)}")

    for message in warnings:
        print(f"aviso: {message}")
    for message in errors:
        print(f"error: {message}")
    drafts = sum(1 for p in parsed.values() if MARKER.search(" ".join(p.text)))
    print(f"{len(pages)} páginas, {drafts} en borrador con marcadores: "
          f"{len(errors)} errores, {len(warnings)} avisos")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
