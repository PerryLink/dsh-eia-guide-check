<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-eia-guide-check-hero-en-light.webp" width="100%" alt="dsh-eia-guide-check: la columna izquierda lleva el nombre del plugin, dos líneas de valor y la nota de que solo lee la hoja y no dicta cumplimiento; a la derecha están los niveles de evidencia del paquete de reglas incluido — direct: 0 reglas (no hay ningún texto literal en el paquete; cada excerpt lo indica), derived-from-principle: 6 reglas (EG-001, EG-002, EG-004, EG-005, EG-006, EG-007, techo warn), institutional-configuration: 1 regla (EG-003, techo info, con values: [] de fábrica, por lo que va a skipped); el pie muestra la ejecución de ejemplo: issues[] 1 (warn) y skipped[] 1.">
</picture>

# dsh-eia-guide-check

**Verifica la trazabilidad de una hoja de aplicabilidad de directrices de EIA: obtienes una lista de qué fila, qué columna y qué falta corregir; la conclusión queda en manos del revisor.**

Un plugin verificador de solo datos para DeepSeek Harness: lee una hoja de aplicabilidad de directrices (la cabecera del proyecto más una fila por elemento evaluado), aplica el paquete de reglas versionado que incluye (EG-001..EG-007) y solo enumera las diferencias que puede señalar dentro del material —nunca un veredicto de cumplimiento ni una atribución de responsabilidad.

[Instalar](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-eia-guide-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-eia-guide-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-eia-guide-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-eia-guide-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-eia-guide-check?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-eia-guide-check/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-eia-guide-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-eia-guide-check)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-eia-guide-check?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-eia-guide-check?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-eia-guide-check/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-eia-guide-check)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-eia-guide-check)

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
```

</div>

<sub>Plugin de la comunidad, no afiliado a DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-eia-guide-check> (Gitee es un espejo).</sub>

## Qué es

`dsh-eia-guide-check` lee una hoja de aplicabilidad de directrices de una evaluación de impacto ambiental —la cabecera del proyecto más una fila por elemento evaluado— y comprueba la trazabilidad de esa propia hoja: que cada elemento indique la directriz que le aplica (nombre o número, al menos uno), que el número de la directriz siga la forma publicada, que el estado de la directriz proceda del vocabulario que configure, que se registre un método de evaluación o una norma aplicable, que ningún elemento esté registrado dos veces, que la cabecera declare el proyecto y el tipo de documento de evaluación, y que no quede ningún marcador de plantilla sin sustituir en la columna de la norma aplicable.

No decide si la evaluación de impacto ambiental cumple la normativa, si el nivel de evaluación es correcto, si un modelo de predicción es aplicable ni si sus conclusiones se sostienen.

- **Para quién**: redactores de EIA y responsables ambientales; no hace falta línea de comandos —entrega el material en el chat.
- **Qué le das**: el material de origen sobre el que trabaja la comprobación (una tabla, un registro o un documento); el original nunca se modifica. Excel puede convertirse antes a JSON/YAML, en el chat si la plataforma lo admite.
- **Qué recibes**: una lista de «qué fila, qué columna, qué falta y cómo corregirlo»; cada comprobación que no pudo ejecutarse aparece en `skipped` con su motivo.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-eia-guide-check-flow-v5-light.svg" width="100%" alt="Estructura de dsh-eia-guide-check (tablero de conexión columna → regla): las 8 columnas canónicas de una hoja de aplicabilidad (JSON/YAML) se conectan con las 7 reglas que las leen — guideName y guideCode a EG-001, guideCode también a EG-002, guideStatus a EG-003, method y standard a EG-004, standard también a EG-007, element a EG-005, project y reportType a EG-006; cada regla lleva su techo de gravedad (warn en seis, info en una). Solo hay dos salidas: lo encontrado va a issues[] (el ejemplo: fila 1 con guideName y guideCode vacíos), lo que no pudo ejecutarse va a skipped[] con su motivo (EG-003, values sin configurar), y una regla que se ejecutó sin hallazgos no entra en ninguna; una lista vacía no es un aprobado y la conclusión queda en el revisor.">
</picture>

## Instalación en tres pasos

1. **Instala** (elige un canal):

   ```sh
   # canal git (último main; equivalente a git+https://github.com/PerryLink/dsh-eia-guide-check.git)
   dsh plugin --profile <name> add github:PerryLink/dsh-eia-guide-check
   # canal npm (versiones publicadas)
   dsh plugin --profile <name> add dsh-eia-guide-check
   # canal tarball: pnpm pack en este repo y luego
   dsh plugin --profile <name> add ./dsh-eia-guide-check-<version>.tgz
   ```

   El canal npm instala el `lib/` ya construido; el canal git lo construye al instalar mediante el script `prepare` (tsdown), sin compilación manual.

2. **Configuración mínima** (los valores por defecto ya funcionan; una fila de bundle sin `config` usa todos los valores por defecto, con la ruta del paquete de reglas apuntando al `rules/eia-guide-check.yaml` incluido):

   ```yaml
   - insert:
       - id: dsh-eia-guide-check
         name: dsh-eia-guide-check
   ```

3. **Verifica que se monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
   ```

   Luego entrégale una hoja. La salida esperada del ejemplo incluido (`samples/quickstart/expected/result.json`):

   ```json
   {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
   ```

   Puedes reejecutarlo en este repositorio (primero `pnpm run build` para producir `lib/`):

   ```sh
   node samples/quickstart/run.mjs --json
   ```

**Desinstalar**: `dsh plugin --profile <name> remove dsh-eia-guide-check` (o elimina la fila del patch del perfil).

<details>
<summary>Usarlo en WorkBuddy / Coze</summary>

Busca «Professional Document Check Suite» (el conjunto completo; esta comprobación es una de sus partes; disponibilidad según el mercado) en WorkBuddy / Coze para usar la misma capacidad de comprobación sin línea de comandos.

</details>

<details>
<summary>Instalar desde el mercado de DSH Desktop</summary>

Todos los plugins de PerryLink pueden explorarse en el mercado integrado de DSH Desktop: **Market → Sources → add source → pegar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ seleccionarlo**. La instalación sigue pasando por la verificación de identidad npm del mercado y tu confirmación.

</details>

## Capacidades clave

`dsh-eia-guide-check` registra la herramienta `eia_guide_check`: lee una hoja de aplicabilidad de directrices, aplica un paquete de reglas versionado y devuelve un informe.

- **Siete reglas en un paquete de datos** — el paquete de reglas es datos, no código (`rules/eia-guide-check.yaml`); sustituirlo cambia todo el conjunto de reglas sin tocar una línea de TypeScript.
- **Solo lectura sobre el material** — acepta JSON o YAML y nunca modifica el original; ESM puro, sin peticiones de red ni llamadas al modelo.
- **Sin citas inventadas** — cada regla lleva `document` / `number` / `clause` / `excerpt` / `kind` / `source`; este paquete no obtuvo en esta pasada el texto literal de ninguna directriz, así que cada `excerpt` lo dice explícitamente y queda marcado `derived-from-principle`: una descripción nunca se presenta como cita.
- **La gravedad sigue a la evidencia** — `derived-from-principle` tiene tope `warn`, la configuración institucional (`institutional-configuration`) tope `info`, y una prueba lo verifica.
- **Una lista de incidencias vacía nunca significa «no hay nada mal»** — cada comprobación que no pudo ejecutarse se informa en `skipped` con su motivo; una regla cuya lista requerida no está configurada se informa a sí misma en `skipped` en vez de pasar en silencio.
- **Sin catálogo de directrices** — no puede asignar un elemento a «la directriz que debería regirlo», así que no detecta el error más consecuente: usar la directriz equivocada para un elemento. Eso exige la lista de clasificación y el alcance de cada directriz.
- **Sin lenguaje que adjudique** — el informe enumera diferencias y nunca se pronuncia sobre cumplimiento, responsabilidad o corrección; un guardián de redacción lo impone y todo informe lleva el descargo de responsabilidad.

| Regla | Comprobación | Gravedad | Tipo de base |
|---|---|---|---|
| `EG-001` | cada elemento indica su directriz aplicable (nombre o número) | warn | principle |
| `EG-002` | el número de la directriz sigue la forma publicada | warn | principle |
| `EG-003` | el estado de la directriz procede de tu vocabulario (desactivada por defecto) | info | local |
| `EG-004` | se registra un método o una norma aplicable | warn | principle |
| `EG-005` | los elementos no están registrados dos veces | warn | principle |
| `EG-006` | la hoja declara su proyecto y tipo de documento | warn | principle |
| `EG-007` | la columna de la norma no contiene marcadores sin sustituir | warn | principle |

### Ejemplos

Son los puntos de entrada reales del plugin; instala una vez y llama a uno. La primera fila de la tabla siguiente es el caso detallado y las demás son casos breves.

**Ejemplo detallado** — herramienta `eia_guide_check`, entrada:

```json
{"rows":[{"序号":"1","评价要素":"环境空气","导则名称":"","导则编号代码":"", ...}]}
```

Salida:

```json
{
  "id": "dsh-eia-guide-check.EG-001.de09b5a6",
  "ruleId": "EG-001",
  "severity": "warn",
  "locator": {
    "row": 1,
    "field": "guideName"
  },
  "found": "第 1 行 guideName、guideCode 都为空",
  "expected": "guideName、guideCode 至少应填写一项",
  "fix": "补填适用导则名称与编号；本条只核对是否指明，不判断适用是否正确"
}
```

*Observed from `dsh-eia-guide-check/tests/fixtures/EG-001/EG-001-unsafe.json; dsh-eia-guide-check/tests/fixtures/EG-001/cases.json; dsh-eia-guide-check/rules/eia-guide-check.yaml; dsh-eia-guide-check/tests/index.test.ts`*

| Usted pregunta | Qué responde |
|---|---|
| Una fila de elemento deja vacíos el nombre y el número de la directriz. ¿Se informa de ello? | Sí. `EG-001` informa de esa fila cuando `guideName` y `guideCode` están ambos vacíos, porque la fila debe indicar al menos uno de los dos. Solo comprueba que se indique una directriz, nunca si es la correcta para ese elemento: el plugin no incluye ningún catálogo de directrices ni asigna elementos a directrices. |
| El número de la directriz figura como `HJ 2.3`, sin año. ¿Se detecta? | Sí. `EG-002` comprueba la forma «HJ número—año de cuatro cifras», como en `HJ 2.3—2018`, así que un valor sin el año de cuatro cifras no coincide y se informa fila por fila. Solo comprueba la forma: no que el número exista, no que esté vigente y no que corresponda al nombre que figura al lado. Una celda `guideCode` vacía no se informa aquí: los valores vacíos quedan fuera de esta comprobación de forma. |
| La columna de estado está rellena con un valor de nuestro propio vocabulario. ¿Por qué no se ha comprobado nunca? | Porque la lista `values` de `EG-003` viene vacía, es decir, el vocabulario de estados aún no está configurado: la regla se declara a sí misma en `skipped`, con el motivo de que ese vocabulario es propio de la institución, en lugar de pasar en silencio. Una vez configurado, solo comprueba que el valor relleno figure en la lista, no que la directriz esté realmente vigente. |
| El método de evaluación está puesto, pero la columna de la norma aún contiene un marcador de plantilla sin sustituir. ¿Se detecta? | `EG-004` solo exige que esté relleno uno de los dos, `method` o `standard`, así que un método relleno la satisface; no juzga si el método es aplicable ni si la norma es correcta. El marcador que queda lo informa `EG-007`, que busca en la columna de la norma el primer término configurado que encuentra (marcadores entre corchetes, `XXX`, `TBD` y similares). Esos términos son ajustables, y una celda de norma totalmente vacía no la informa ninguna de las dos reglas. |
| El elemento `地表水` está registrado dos veces, una por calidad del agua y otra por sedimentos. ¿Qué ocurre? | `EG-005` informa del valor repetido de `element` e indica con qué fila anterior coincide, porque la repetición impide saber qué directriz rige ese elemento. Compara solo el texto sin espacios y el hallazgo requiere confirmación humana: evaluar un mismo elemento por medio es habitual, así que escriba el subelemento en el nombre del elemento en vez de borrar la fila. Si la hoja no tiene columna `element`, la regla informa de que no pudo ejecutarse en lugar de pasar en silencio. |
| La cabecera no trae el nombre del proyecto ni el tipo de documento de evaluación. ¿Qué ocurre? | `EG-006` informa de que a la cabecera le faltan `project` y `reportType`, porque el tipo de documento (memoria, formulario o ficha de registro) determina qué conjunto de requisitos se aplica. Solo comprueba que la cabecera los declare; no juzga si la clasificación del tipo es correcta. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| Serie de Directrices Técnicas de Evaluación de Impacto Ambiental | versión vigente de cada directriz no verificada en esta pasada | EG-001, EG-002 |
| Criterio institucional de gestión de la calidad de EIA (configurado por su institución) | sin estándar unificado (la base es el vocabulario de estados configurado por la institución) | EG-003 |
| Directrices Técnicas de Evaluación de Impacto Ambiental — Programa General | HJ 2.1 (versión vigente y números de cláusula no verificados en esta pasada) | EG-004, EG-005, EG-007 |
| Catálogo para la Gestión de la Clasificación de la Evaluación de Impacto Ambiental de Proyectos de Construcción | versión vigente y números de cláusula no verificados en esta pasada | EG-006 |

**Límite:** este plugin comprueba la trazabilidad de una **hoja de aplicabilidad de directrices de EIA** —que cada elemento ambiental indique su directriz aplicable, que el número de la directriz siga la forma publicada, que el estado proceda de su vocabulario, que se registre un método de evaluación o una norma aplicable, que los elementos no estén duplicados, que la hoja declare su proyecto y tipo de documento, y que no quede ningún marcador. **No** decide si la evaluación de impacto ambiental cumple la normativa, si el nivel de evaluación es correcto, si un modelo de predicción es aplicable ni si las conclusiones se sostienen.

> ### ⚠️ Lea esto antes de fiarse de una cita del informe
>
> **El estado de `excerpt` es por regla, no uniforme.** Algunas reglas citan la cláusula literalmente (`kind: direct`), otras se derivan del principio de los artículos citados (`kind: derived-from-principle`, tope `warn`) y otras usan umbrales que configura su institución (`kind: institutional-configuration`, tope `info`). El paquete nunca parafrasea una cita: cuando el texto no se obtuvo, el campo `excerpt` lo dice y el razonamiento vive en `note`; una prueba exige que ninguna regla afirme una cita que no tiene. **Para toda regla aún marcada como no obtenida, sustituya el `excerpt` por la cláusula real y eleve `kind` a `direct` cuando tenga el texto.**
>
> La conclusión es del revisor: este plugin enumera diferencias que puede señalar en el material y no decide hechos ni cumplimiento.

## Configuración

Todas las opciones son campos Schemastery `Config` de `src/config.ts` (modificables desde cordis.yml); los umbrales por regla viven en el paquete de reglas bajo `rules/`. Una sobrescritura por id reemplaza la fila entera: repita cada clave que necesite.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

Parámetros por regla que conviene conocer:

- `EG-002` `pattern` — la forma del número, por defecto «HJ número (decimal opcional) — año de cuatro cifras». Amplíela si su registro escribe los números de otra manera.
- `EG-003` `values` — su vocabulario de estados, p. ej. `[vigente, derogada, sustituida, parcialmente aplicable]`. Vacío significa sin comprobación; no hay tabla de versiones vigentes incorporada.
- `EG-007` `terms` — los marcadores que hay que buscar.

Ejemplo de sobrescritura en su patch de perfil:

```yaml
- insert:
    - id: dsh-eia-guide-check
      name: dsh-eia-guide-check
      config:
        disabledRules: [EG-003]
        timeoutMs: 180000
```

## Formato del material

La herramienta acepta JSON o YAML:

```yaml
project: 某某建设项目
industry: 某某行业
reportType: 报告书
compiler: 某某环评单位
rows:
  - { 序号: '1', 评价要素: 环境空气, 导则名称: 环境影响评价技术导则 大气环境,
      导则编号代码: HJ 2.2—2018, 导则状态: 现行, 应用章节: 第 5 章 大气环境影响预测与评价,
      评价方法: AERMOD 预测模式, 评价范围: 二级评价，边长 5 km 矩形,
      评价因子: PM10、PM2.5、SO2、NOx, 执行标准: GB 3095—2012 环境空气质量标准 }
```

Los nombres de columna se comparan sin distinguir mayúsculas y ignorando espacios, guiones bajos y guiones; se conservan los nombres de columna de la hoja, así que un hallazgo nombra la columna que leyó. Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una hoja parcialmente exportada produce hallazgos de «falta un elemento» en vez de un fallo.

## Fuentes de las reglas

Los datos de las reglas viven en `rules/eia-guide-check.yaml`, separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. La cabecera del paquete declara por completo que el plugin no incluye catálogo de directrices, no asigna elementos a directrices y no verificó la versión vigente de cada una; la `note` de cada regla repite la parte que le concierne. El guardián de carga exige `document` / `clause` / `excerpt` / `source` y prohíbe que una comprobación derivada de principios o configurada localmente se marque como `error`. `check:citations` audita los extractos: un segmento que se presenta como cita literal debe poder rastrearse hasta el texto de origen obtenido, mientras que las reglas que declaran no haber obtenido el texto cuentan como marcadores; `rules/citations-baseline.json` solo puede encogerse. Un paquete que exagere su base falla al cargar en lugar de producir un informe que parezca sólido.

## FAQ

<details>
<summary>¿Nos dirá que un elemento usa la directriz equivocada?</summary>

No: es el límite más importante del plugin. No incluye catálogo de directrices ni asigna un elemento a la directriz que debería regirlo; la columna de la directriz es la declaración de la propia hoja, y el plugin solo comprueba que esté escrita, que la forma del número se sostenga y que el estado esté entre los valores que usted configuró. Decidir entre HJ 2.2 y HJ 2.3 exige la lista de clasificación y el alcance de cada directriz; esa conclusión queda en manos del ingeniero de EIA.

</details>

<details>
<summary>La columna de estado está rellena, así que ¿por qué `EG-003` nunca informa?</summary>

Porque la lista `values` de `EG-003` viene vacía, es decir, el vocabulario de estados no está configurado: la regla se declara a sí misma en `skipped` con el motivo de que ese vocabulario es de la institución, en lugar de pasar en silencio. Una vez configurado, sigue comprobando solo si el valor relleno está en la lista, no si la directriz está realmente vigente; eso exige seguir los anuncios de publicación y derogación del ministerio, y no hay tabla de versiones incorporada.

</details>

<details>
<summary>¿Puede leerse una lista `issues` vacía como «no hay nada mal»?</summary>

No. Cada comprobación que no pudo ejecutarse aparece en `skipped` con su motivo (un vocabulario sin configurar, una columna `element` ausente, etc.). Lea `issues` y `skipped` juntos antes de sacar cualquier conclusión; `skippedCount` solo cuenta las reglas que de verdad no se ejecutaron, no las que se ejecutaron limpias.

</details>

<details>
<summary>Mi hoja es un archivo Excel. ¿Puedo usarlo directamente?</summary>

Sí: conviértalo antes a JSON o YAML; en el chat la plataforma puede hacer la conversión si lo admite. La herramienta solo lee el material y nunca modifica el original.

</details>

<details>
<summary>¿Aguantará una hoja completa o un directorio entero a la vez?</summary>

La herramienta funciona en los modos `native` y `ptc`; para trabajo por lotes (un conjunto de hojas de EIA o un directorio completo) use `ptc`, donde el coste del esquema se paga una sola vez. Las comprobaciones son coincidencia local de columnas, sin peticiones de red ni llamadas al modelo; `timeoutMs` (120 s por defecto) es el presupuesto de tiempo de espera cooperativo.

</details>

## Solución de problemas

- **No señaló la directriz equivocada de un elemento.** Es por diseño: no tiene catálogo y nunca asigna un elemento a una directriz. Confírmelo con la lista de clasificación y el alcance de cada directriz.
- **`EG-002` acepta un número que sé que está derogado.** La comprobación lee la forma del número, nunca su validez ni su vigencia. Seguir las versiones es otro trabajo.
- **`EG-002` se dispara con un número que escribí bien.** El patrón exige el prefijo `HJ`, el número y un año de cuatro cifras separados por guion o raya. Ajuste el patrón o corrija la celda.
- **`EG-003` nunca se ejecuta.** Su vocabulario está vacío; rellénelo con los estados que usa su sistema de calidad.
- **`EG-005` se dispara con dos filas del mismo elemento.** Evaluar un mismo elemento por medio (calidad del agua superficial y sedimentos, por ejemplo) es legítimo: escriba el subelemento en el nombre del elemento en vez de borrar una fila.
- **El plugin se instala pero la herramienta no aparece.** Compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` incorrecto hace que el cargador omita la entrada en silencio.
- **`dsh plugin add` rechaza el paquete por incompatibilidad.** El rango de peers cubre `0.1.x` y `0.2.x`; si su runtime está fuera, conceda una exención explícita: `dsh plugin --profile <name> allow-version dsh-eia-guide-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como fallo.** El comprobador estático compara con un rango de peers codificado que es anterior a la línea 0.2. El runtime aplica la compatibilidad de peers al instalar, así que el rango declarado es el correcto; es un problema conocido de `dsh-plugin-dev`.

## Compatibilidad

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` se declara como `>=0.2.1-0 <0.3.0` y el host lo aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native` y `ptc`; para una hoja de evaluación completa use `ptc` |

## Ecosistema y calidad

- [Espejo de Gitee](https://gitee.com/perrylink/dsh-eia-guide-check) (espejo sincronizado; GitHub es el canónico)
- [Página del plugin en dshfind](https://dshfind.com/plugins/PerryLink/dsh-eia-guide-check) (instalaciones y ranking)
- [Informe de OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-eia-guide-check) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listado)
- **Canal de la tienda 1024**: `npm i -g dsh1024` una vez y luego `dsh1024 plugin --profile <name> add dsh-eia-guide-check` (cuenta para el ranking de instalaciones de [deepseek1024.com](https://deepseek1024.com))
- [Base de conocimiento del ecosistema](https://perrylink.github.io/dsh-plugin-guide/) — guía de desarrollo de plugins · datos de selección medidos · criterios de mantenimiento

## Desarrollo

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: suite compartida de plugins de tabla + fixtures emparejados
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # las specs de dependencias se resuelven desde el registry
pnpm run check:lockfile                             # comprobación de deriva del lockfile
pnpm run check:readmes                              # consistencia de los README en cinco idiomas
pnpm run check:citations                            # línea base de citas del paquete de reglas
node ../scripts/sync-shared.mjs dsh-eia-guide-check   # refrescar src/shared desde ../_shared
pnpm pack                                           # el tarball publicado
```

El plugin es **solo datos**: `src/model.ts` declara la forma de la tabla, el kit compartido aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación. Ejecución local del ejemplo (requiere `pnpm run build` antes para producir `lib/`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
```

La entrada del ejemplo está en `samples/quickstart/input/`, la salida esperada en `samples/quickstart/expected/result.json` y una captura en `docs/assets/quickstart.png`. Las imágenes del README se generan programáticamente con [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) y se pueden reejecutar sin riesgo; el diagrama de flujo de una sola piel y las imágenes de demostración antiguas permanecen en `docs/assets/` para enlaces externos, mientras que los README solo referencian el nuevo par claro/oscuro.

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `eia`, `guide`

## Familia y agradecimientos

Este proyecto forma parte de la familia de plugins de DeepSeek Harness de [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Índice completo de la familia: [elegir un verificador por material](https://perrylink.github.io/zh/checkers/choose/) y [todos los plugins](https://github.com/PerryLink). Si te resulta útil, **una estrella ayuda a que la siguiente persona lo encuentre** — no hay nada bloqueado tras ella.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: el paquete de reglas de solo datos (EG-001..EG-007), la herramienta `eia_guide_check`, la línea base de citas y la documentación en cinco idiomas.

<details>
<summary>Desplegar todos los plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRADO (repo archivado) |

</details>

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-eia-guide-check contributors

<p align="center"><sub>Apache-2.0 · Plugin de la comunidad, no afiliado a DeepSeek.</sub></p>
