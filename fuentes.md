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

## Geoides y sistemas (`docs/geoides/`)

| Afirmación | Fuente |
| --- | --- |
| De fábrica: WGS 84 (EPSG:4326), WGS 84 / UTM 11N–16N (EPSG:32611–32616), Mexico ITRF2008 geográficas (EPSG:6365, ITRF2008 época 2010.0) y sus UTM 11N–16N (EPSG:6366–6371), GGM25 y GGM10 | `iOS-CORE:Geodesy/CRSCatalog.swift:77`, `:102`, `:112-114`, `:141-143` (las UTM de México son `6355 + zona`); `AND:core/domain/src/main/kotlin/com/tresvizo/field/core/domain/geodesy/CrsCatalog.kt:158`, `:224-226`; `iOS-APP:Session/DataLibrary.swift:10`; `iOS-APP:UI/Data/DataLibraryView.swift:29-30`; `AND:feature/settings/src/main/res/values/strings.xml:85` |
| Lo demás se baja en «Cuenta › Sistemas y geoides», solo cuando tú lo pides, y se queda en el teléfono | `iOS-APP:UI/Account/AccountTab.swift:162-168`; `iOS-APP:UI/Data/DataLibraryView.swift:229-233`, `:365`; `iOS-APP:Session/DataLibrary.swift:13-16`, `:167-174`; `AND:feature/settings/src/main/kotlin/com/tresvizo/field/feature/settings/AccountScreen.kt:298`; `AND:feature/settings/src/main/kotlin/com/tresvizo/field/feature/settings/DataLibraryScreen.kt:106`, `:305-307` |
| Catálogo firmado en las versiones de este repositorio | `iOS-APP:Data/DataRepository.swift:15-17`; `AND:app/src/main/kotlin/com/tresvizo/field/data/DataRepository.kt:19-21`; firma Ed25519 en `datos-index.json` (`"algorithm": "Ed25519"`); `DATOS:` `datos-indice` |
| La app trae una copia del catálogo y busca uno nuevo al abrirse, como mucho cada 12 h | `iOS-APP:Session/DataLibrary.swift:63-64`, `:77-82`, `:94-96`; `AND:core/domain/src/main/kotlin/com/tresvizo/field/core/domain/data/DataLibrary.kt:189-193`, `:645`; `AND:app/src/main/kotlin/com/tresvizo/field/data/DataRepository.kt:23-24`. El catálogo incluido en las dos apps es idéntico al publicado (SHA-256 `510e27f8…6b92`, secuencia 3, el 21-10-2026) |
| Comprueba la firma, el tamaño y el SHA-256 antes de instalar | `iOS-APP:Session/DataLibrary.swift:17-18`, `:80`, `:143`, `:227`; `AND:core/domain/src/main/kotlin/com/tresvizo/field/core/domain/data/DataLibrary.kt:114`, `:198`, `:488-492` |
| GGM25 y GGM10: autoridad, situación, malla, referencia, exactitud, licencia y crédito | Sin cambios desde la versión del 20-10-2026 del sitio (`618775f`). |
| EGM2008, EGM96, MAPGEO2015 y QGeoidCOL2023: autoridad, situación (`isHistoric`), malla (`gridStepArcMinutes`), referencia (`frame`, `frameEpoch`, `verticalDatum`, `heightKind`), exactitud (`declaredAccuracyMeters`), licencia (`license`, `licenseURL`), fuente (`sourceURL`), crédito (`attribution` + `transformationNotice`) y tamaño (`file.bytes`) | Carga firmada de `datos-index.json`, secuencia 3, publicada `2026-10-21T07:25:30Z` (`DATOS:` `datos-indice`; copia en `iOS-APP:Resources/Datos/datos-index.json`, commit `ccc4bf9`). Los créditos se copian tal cual. |
| Paquetes de sistemas y su número de sistemas (Mundo 116, México complementos 14, Argentina 30, Brasil 41, Chile 20, Colombia 17, Costa Rica 6, El Salvador 2, Perú 10); «Parámetros del registro EPSG de IOGP, v12.029»; términos de uso de IOGP | La misma carga firmada (`crsPackage.systems`, `attribution`, `license`, `licenseURL`); archivos `crs-*-r1.json` en `DATOS:` `datos-2026-10-21` |
| La app muestra el crédito de cada modelo | `iOS-APP:UI/Data/DataLibraryView.swift:265`; `AND:feature/settings/src/main/kotlin/com/tresvizo/field/feature/settings/AccountScreen.kt:940-943` |
| CC BY 4.0 pide citar, enlazar la licencia e indicar los cambios | Licencia CC BY 4.0, sección 3(a), <https://creativecommons.org/licenses/by/4.0/legalcode> |

## Batería y seguridad (`docs/seguridad/`)

| Afirmación | Fuente |
| --- | --- |
| Los receptores están en validación; no hay ninguna cifra medida (protección, caídas, temperatura) | `MV:docs/validacion/README.md:1-6` (el plan cubre MeridianV y MeridianVI), `:54`; `MV:docs/validacion/registros/ensayos.csv` sin ningún ensayo |
| El MeridianV no tiene protección contra el agua ni el polvo: desagüe y uniones sin junta; no exponerlo a la lluvia ni dejarlo sobre suelo mojado | `MV:docs/validacion/ficha-tecnica-meridianv.md:105`, `:124-125`; `MV:docs/validacion/README.md:54` |
| El MeridianVI no tiene ningún grado de protección verificado | `MV:docs/validacion/README.md:54` (AMB-3 y AMB-4 pendientes); su «IP67» es objetivo de diseño sin ensayo (`MV:docs/professional-audit-2026-10-21/07-product-docs-release.md`, DOC2-15) |
| Sin ensayo de caída; tras un golpe, a servicio, porque la calibración de la IMU es de fábrica | `MV:docs/validacion/ficha-tecnica-meridianv.md:106`, `:126-127` |
| Antena del MeridianV sin calibración de centro de fase: «NONE» en posproceso | `MV:docs/validacion/ficha-tecnica-meridianv.md:128-129` |
| Lo que no está medido no se garantiza; las cifras van en la ficha con su ensayo | `MV:docs/validacion/ficha-tecnica-meridianv.md:5-7`, `:130` |
| Batería del MeridianV: Li-ion, 1S2P con dos 18650, con circuito de protección (BMS) | `MV:firmware/esp32/include/board_profile_v03.h:97`, `:127`; `MV:docs/validacion/ficha-tecnica-meridianv.md:87`. La capacidad (5600 mAh) es «según el anuncio; sin medir» (`board_profile_v03.h:98`) y no se publica. Ojo: `MV:hardware/bom.md:21` y `MV:hardware/wiring.md:88` todavía describen la batería anterior (LiPo 3000 mAh) |
| Energía en Wh sin medir | `MV:docs/validacion/ficha-tecnica-meridianv.md:88` (estado «pendiente», ENE-5) |
| Temperatura de carga y de trabajo sin medir | `MV:docs/validacion/ficha-tecnica-meridianv.md:95` («de diseño, no medido»), `:102` («pendiente») |
| UN 38.3 y Wh todavía no disponibles | `MV:docs/validacion/README.md:56-58` |
| Sin homologación de los radios ni certificaciones NOM | `MV:docs/validacion/README.md:56-58`; `MV:docs/validacion/ficha-tecnica-meridianv.md:118` (LoRa «sin homologar») |
