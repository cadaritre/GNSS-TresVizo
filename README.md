# GNSS-TresVizo

Sitio público y datos de los receptores GNSS **MeridianV** y **MeridianVI** de TresVizo y de la app
**TresVizo Field** para iPhone y Android.

Sitio: <https://cadaritre.github.io/GNSS-TresVizo/>

## Qué hay

El sitio se sirve con GitHub Pages desde la carpeta `docs/` de la rama `main`. Es HTML estático, sin
compilación: lo que está en `docs/` es lo que se publica, y solo si pasa `tools/comprobar_sitio.py`.

| Ruta | Página |
| --- | --- |
| `docs/index.html` | Portada |
| `docs/guia/` | Guía rápida del MeridianV, con sus capturas y los PDF para iPhone y para Android |
| `docs/soporte/` | Soporte técnico: cómo pedir ayuda, qué datos mandar, preguntas frecuentes y cómo actualizar el firmware |
| `docs/garantia/` | Garantía del receptor y reparaciones (borrador) |
| `docs/seguridad/` | Batería y seguridad: carga, uso en campo, almacenamiento y transporte |
| `docs/geoides/` | Geoides y sistemas de coordenadas, con su autoridad y su licencia |
| `docs/licencia/` | Contrato de licencia de uso del software, EULA (borrador) |
| `docs/privacidad/` | Política de privacidad (borrador) |
| `docs/404.html` | Página de «no encontrada» |
| `docs/assets/` | Hoja de estilos común y logotipos |
| `tools/importar_guia.py` | Copia la guía rápida desde el repositorio del firmware |
| `tools/navegacion.py` | Escribe la misma cabecera y el mismo pie en todas las páginas |
| `tools/comprobar_sitio.py` | Comprueba borradores, vigencia, recursos de terceros y enlaces; corre también en GitHub Actions |
| `fuentes.md` | La fuente de cada afirmación del sitio (no se publica) |

Las direcciones que piden las tiendas de apps son:

- Política de privacidad: <https://cadaritre.github.io/GNSS-TresVizo/privacidad/>
- Contrato de licencia: <https://cadaritre.github.io/GNSS-TresVizo/licencia/>
- Soporte: <https://cadaritre.github.io/GNSS-TresVizo/soporte/>

## Versiones (releases)

Las versiones de este repositorio llevan los **geoides y paquetes de sistemas de coordenadas** que la app
descarga, como archivos adjuntos; el repositorio en sí no los contiene.

- `datos-indice`: el índice firmado (`datos-index.json`) que leen las apps en esa dirección fija. No se
  borra.
- `datos-AAAA-MM-DD`: los archivos de cada publicación (hoy, `datos-2026-10-21`).

De fábrica, la app trae WGS 84, Mexico ITRF2008 con sus zonas UTM 11N a 16N y los geoides GGM25 y GGM10
del INEGI. Cada archivo publicado conserva la licencia de su autoridad, y se agrega a la página
`docs/geoides/` con su autoridad, su licencia y su crédito, el mismo día que se publica.

## Cómo se actualiza

**Guía rápida.** La guía se escribe en el repositorio del firmware, en `docs/guia-cliente/`. Allí se
regeneran los PDF con `build_pdf.py`, y después se importa:

```sh
python3 tools/importar_guia.py /ruta/a/MeridianV/docs/guia-cliente
```

El script arma la página completa a partir del fragmento `guia.html`, copia solo las imágenes que la página
usa y los dos PDF, y añade los enlaces del sitio.

**Documentos legales.** Se editan en su HTML. Al cambiar uno, sube la versión y la fecha de «Última
revisión». Mientras un documento no esté revisado por un abogado, conserva arriba el aviso «Borrador.
Pendiente de revisión legal.», que dice que el documento «no está vigente». Los datos pendientes van
marcados así, y se listan con:

```sh
grep -rnoE "\[(COMPLETAR|VERIFICAR)[^]]*\]" docs
```

**Fuentes.** Cada afirmación de una página pública lleva su fuente en `fuentes.md` (archivo, línea y commit,
o la ley con su artículo, o la decisión del propietario con su fecha). Lo que no tiene fuente no se
publica.

**Una página nueva.** Créala en `docs/<nombre>/index.html` con un `<header class="topbar">` y un
`<footer class="foot">` vacíos, agrégala a las listas de `tools/navegacion.py` y ejecútalo:

```sh
python3 tools/navegacion.py
```

**Comprobarlo antes de publicar.**

```sh
python3 tools/comprobar_sitio.py
```

Falla si una página con marcadores no lleva el recuadro de borrador, si una se declara vigente con
marcadores, si alguna carga algo de otro dominio (fuentes incluidas) o si hay un enlace interno roto. El
mismo script corre en GitHub Actions (`.github/workflows/comprobar-sitio.yml`) en cada cambio de `docs/` o
`tools/`.

**Verlo antes de publicar.**

```sh
cd docs && python3 -m http.server 8000
```

y abre <http://localhost:8000/>. La página 404 usa rutas absolutas (`/GNSS-TresVizo/…`) porque GitHub la
sirve desde cualquier dirección; en local solo se ve bien desde un servidor con esa ruta.

**Publicar.** Basta con subir a `main`: la Action `.github/workflows/comprobar-sitio.yml` corre la
comprobación y, solo si pasa, publica `docs/` en GitHub Pages (*Settings › Pages › Source: GitHub Actions*,
desde el 21-10-2026). Una página que no pasa la comprobación no se publica y el sitio sigue con la versión
anterior. El archivo `docs/.nojekyll` se conserva por si Pages vuelve a publicarse desde la rama.

## Derechos

© 2026 TresVizo. Los textos, las capturas y los logotipos de este repositorio son de TresVizo. Los geoides
y los demás datos de terceros son de sus autoridades y se distribuyen con su licencia, indicada en
`docs/geoides/` y en el contrato de licencia.
