# GNSS-TresVizo

Sitio público y datos de los receptores GNSS **MeridianV** y **MeridianVI** de TresVizo y de la app
**TresVizo Field** para iPhone y Android.

Sitio: <https://cadaritre.github.io/GNSS-TresVizo/>

## Qué hay

El sitio se sirve con GitHub Pages desde la carpeta `docs/` de la rama `main`. Es HTML estático, sin
compilación: lo que está en `docs/` es lo que se publica.

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

Las direcciones que piden las tiendas de apps son:

- Política de privacidad: <https://cadaritre.github.io/GNSS-TresVizo/privacidad/>
- Contrato de licencia: <https://cadaritre.github.io/GNSS-TresVizo/licencia/>
- Soporte: <https://cadaritre.github.io/GNSS-TresVizo/soporte/>

## Versiones (releases)

Las versiones de este repositorio llevarán los **paquetes de geoides y sistemas de coordenadas** que la
app descarga. Se suben aparte, como archivos adjuntos de cada versión; el repositorio en sí no los
contiene.

Hoy la app trae incluidos los geoides de México, GGM25 y GGM10 del INEGI. Cada paquete nuevo conserva la
licencia de su autoridad, y se agrega a la página `docs/geoides/` con su autoridad, su licencia y su
crédito.

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
Pendiente de revisión legal.». Los datos pendientes van marcados así, y se listan con:

```sh
grep -rnoE "\[(COMPLETAR|VERIFICAR)[^]]*\]" docs
```

**Una página nueva.** Créala en `docs/<nombre>/index.html` con un `<header class="topbar">` y un
`<footer class="foot">` vacíos, agrégala a las listas de `tools/navegacion.py` y ejecútalo:

```sh
python3 tools/navegacion.py
```

**Verlo antes de publicar.**

```sh
cd docs && python3 -m http.server 8000
```

y abre <http://localhost:8000/>. La página 404 usa rutas absolutas (`/GNSS-TresVizo/…`) porque GitHub la
sirve desde cualquier dirección; en local solo se ve bien desde un servidor con esa ruta.

**Publicar.** En GitHub, *Settings › Pages*: *Deploy from a branch*, rama `main`, carpeta `/docs`. El
archivo `docs/.nojekyll` hace que GitHub publique los archivos tal cual.

## Derechos

© 2026 TresVizo. Los textos, las capturas y los logotipos de este repositorio son de TresVizo. Los geoides
y los demás datos de terceros son de sus autoridades y se distribuyen con su licencia, indicada en
`docs/geoides/` y en el contrato de licencia.
