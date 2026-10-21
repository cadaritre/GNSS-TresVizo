# Fuentes de lo que dice el sitio

Regla: **cada afirmación de una página pública lleva aquí su fuente comprobada**, como
`archivo:línea@commit`, una ley con su artículo y su última reforma, o una decisión del propietario con su
fecha. Lo que no tiene fuente no se publica: se queda como marcador `[COMPLETAR: …]` o `[VERIFICAR: …]`
en una página en borrador (lo exige `tools/comprobar_sitio.py`).

Al cambiar una página, se vuelve a comprobar su sección de este archivo contra el código del día y se
actualizan los commits.

Este archivo **no se publica** en el sitio (está fuera de `docs/`). Las rutas son de los repositorios de
ingeniería, que son privados.

## Repositorios y commits leídos

| Prefijo | Repositorio | Commit leído |
| --- | --- | --- |
| `MV:` | MeridianV (firmware, documentación y validación) | `7808cd1` (21-10-2026) |
| `VI:` | MeridianVI | `bf02d09` (21-10-2026) |
| `iOS:` | TresVizo Field para iPhone; `iOS-APP:` = `TresVizo Field/TresVizo Field/`, `iOS-CORE:` = `TresVizo Field/Packages/MeridianVCore/Sources/MeridianVCore/` | `d9a9dcc` (21-10-2026) |
| `AND:` | TresVizo Field para Android; rutas desde `android/` | `f8a3c526` (21-10-2026) |
| `DATOS:` | Versiones (releases) de este repositorio: `datos-indice` (publicada 2026-10-21 07:28:56 UTC) y `datos-2026-10-21` (07:28:47 UTC) | `gh release view`, 21-10-2026 |

Siempre se leyó lo commiteado (`git show <commit>:<ruta>`), no el árbol de trabajo.

Leyes, leídas el 21-10-2026 en el portal de la Cámara de Diputados:

| Prefijo | Ley | Versión |
| --- | --- | --- |
| `LFPC` | Ley Federal de Protección al Consumidor, <https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPC.pdf> | Última reforma DOF 12-12-2025 |
| `LFPDPPP` | Ley Federal de Protección de Datos Personales en Posesión de los Particulares, <https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf> | Nueva ley DOF 20-03-2025, última reforma DOF 14-11-2025 |

Decisiones del propietario:

| Prefijo | Qué | Dónde consta |
| --- | --- | --- |
| `PROP-21` | Titular: Carlos Daniel Rivera Trevizo, como desarrollador (persona física), con la marca TresVizo. Soporte y privacidad: `ingenieria@3vizo.com`. | `MV:docs/professional-audit-2026-10-21.md:127`, `:129` |
| `PROP-21` | Horario: lunes a viernes, 9 a 18 h, hora del centro de México; respuesta en un día hábil. Sin WhatsApp. Garantía: receptor 12 meses, batería 6 meses. No hay clientes ni unidades armadas. | Decisión del 21-10-2026, recibida por el coordinador de la auditoría 2 |
| `PROP-21D` | Domicilio del titular: J. Domínguez de Mendoza 1704, colonia San Felipe, C.P. 31203, Chihuahua, Chihuahua, México. Jurisdicción: tribunales de Chihuahua, Chihuahua. El RFC todavía no. | Decisión del 21-10-2026, recibida por el coordinador de la auditoría 2 |
| `PROP-TONOS` | Con el teléfono en silencio no suena nada. | Decisión del 21-10-2026 (AND2-10). El sitio no dice lo contrario en ninguna página (búsqueda de «silencio», «tono», «sonido» el 21-10-2026). |

## Soporte (`docs/soporte/`)

| Afirmación | Fuente |
| --- | --- |
| Correo `ingenieria@3vizo.com`, horario y respuesta en un día hábil | `PROP-21` |
| La versión del firmware sale al encender, a la derecha de «Iniciando...», y en la página «RECEPTOR», línea «Firmware» | `MV:firmware/esp32/include/display_model.h:529-539`, `:770-773` |
| Una pulsación corta del botón cambia de página | `MV:firmware/esp32/include/power_sequence.h:58`, `:65-66` |
| iPhone: iOS 26.2 o posterior | `iOS:TresVizo Field/TresVizo Field.xcodeproj/project.pbxproj:197`, `:255` (`IPHONEOS_DEPLOYMENT_TARGET = 26.2`). El mínimo no está decidido (`iOS:docs/publicacion/README.md:16`): si cambia, cambia aquí. |
| Android: 8.0 o posterior, con Bluetooth LE | `AND:app/build.gradle.kts:183` (`minSdk = 26`, Android 8.0); `AND:app/src/main/AndroidManifest.xml:72` (`bluetooth_le` obligatorio) |
| Recuadro y viñetas de «Calidad de la posición» | Texto idéntico al de `docs/licencia/index.html`, sección 6 (`#exactitud`) |
| De fábrica: WGS 84, Mexico ITRF2008 con UTM 11N–16N, GGM10 y GGM25 | `iOS-CORE:Geodesy/CRSCatalog.swift:102`, `:141-143`; `iOS-APP:UI/Data/DataLibraryView.swift:29-30`; `AND:core/domain/src/main/kotlin/com/tresvizo/field/core/domain/geodesy/CrsCatalog.kt:158`, `:224-226`; `AND:feature/settings/src/main/res/values/strings.xml:85` |
| Lo demás se baja en «Cuenta › Sistemas y geoides» y queda en el teléfono | `iOS-APP:UI/Account/AccountTab.swift:162-168`; `iOS-APP:Session/DataLibrary.swift:13-16`; `AND:feature/settings/src/main/kotlin/com/tresvizo/field/feature/settings/AccountScreen.kt:298`; `AND:feature/settings/src/main/res/values/strings.xml:83-85` |
| «Hay una versión nueva del firmware del receptor» | `iOS-CORE:Transfers/FirmwareCatalog.swift:367`; `AND:core/domain/src/main/kotlin/com/tresvizo/field/core/domain/transfers/IncludedFirmware.kt:20` |
| Todavía no se ha publicado ninguna versión del firmware dentro de la app | `iOS:TresVizo Field/Firmware/index.json:1` y `AND:app/src/main/assets/firmware/index.json:1`: `{"format": 1, "images": []}`; `MV:CHANGELOG.md:5-12` (1.0.0 «sin publicar») |
