# dsh-eia-guide-check — Verificación de la hoja de aplicabilidad de directrices de evaluación de impacto ambiental

`dsh-eia-guide-check` lee una hoja de aplicabilidad de directrices de una evaluación de impacto ambiental —la cabecera del proyecto más una fila por elemento evaluado— y comprueba la trazabilidad de esa propia hoja: que cada elemento indique la directriz que le aplica, que el número de la directriz siga la forma publicada, que el estado de la directriz proceda del vocabulario que usted configure, que se registre un método de evaluación o una norma aplicable, que ningún elemento esté registrado dos veces, que la cabecera declare el proyecto y el tipo de documento de evaluación, y que no quede ningún marcador de plantilla sin sustituir en la columna de la norma aplicable.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila de elemento deja vacíos el nombre y el número de la directriz. ¿Se informa de ello? | Sí. `EG-001` informa de esa fila cuando `guideName` y `guideCode` están ambos vacíos, porque la fila debe indicar al menos uno de los dos. Solo comprueba que se indique una directriz, nunca si es la correcta para ese elemento: el plugin no incluye ningún catálogo de directrices ni asigna elementos a directrices. |
| El número de la directriz figura como `HJ 2.3`, sin año. ¿Se detecta? | Sí. `EG-002` comprueba la forma «HJ número—año de cuatro cifras», como en `HJ 2.3—2018`, así que un valor sin el año de cuatro cifras no coincide y se informa fila por fila. Solo comprueba la forma: no que el número exista, no que esté vigente y no que corresponda al nombre que figura al lado. Una celda `guideCode` vacía no se informa aquí: los valores vacíos quedan fuera de esta comprobación de forma. |
| La columna de estado dice `现行`. ¿Por qué no se ha comprobado nunca? | Porque la lista `values` de `EG-003` viene vacía, es decir, el vocabulario de estados aún no está configurado: la regla se declara a sí misma en `skipped`, con el motivo de que ese vocabulario es propio de la institución, en lugar de pasar en silencio. Una vez configurado, solo comprueba que el valor relleno figure en la lista, no que la directriz esté realmente vigente. |
| El método de evaluación está puesto, pero la columna de la norma aún dice `【待填】`. ¿Se detecta? | `EG-004` solo exige que esté relleno uno de los dos, `method` o `standard`, así que un método relleno la satisface; no juzga si el método es aplicable ni si la norma es correcta. El marcador que queda lo informa `EG-007`, que busca en la columna de la norma los términos configurados (`【`, `】`, `XXX`, `待填`, `TBD`, `示例` y similares) e informa del primero que encuentra. Esos términos son ajustables, y una celda de norma totalmente vacía no la informa ninguna de las dos reglas. |
| El elemento `地表水` está registrado dos veces, una por calidad del agua y otra por sedimentos. ¿Qué ocurre? | `EG-005` informa del valor repetido de `element` e indica con qué fila anterior coincide, porque la repetición impide saber qué directriz rige ese elemento. Compara solo el texto sin espacios y el hallazgo requiere confirmación humana: evaluar un mismo elemento por medio es habitual, así que escriba el subelemento en el nombre del elemento en vez de borrar la fila. Si la hoja no tiene columna `element`, la regla informa de que no pudo ejecutarse en lugar de pasar en silencio. |
| La cabecera no trae el nombre del proyecto ni el tipo de documento de evaluación. ¿Qué ocurre? | `EG-006` informa de que a la cabecera le faltan `project` y `reportType`, porque el tipo de documento (`报告书`／`报告表`／`登记表`) determina qué conjunto de requisitos se aplica. Solo comprueba que la cabecera los declare; no juzga si la clasificación del tipo es correcta. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| 《环境影响评价技术导则》系列 | 各导则现行版本号本次未逐一核实 | EG-001, EG-002 |
| 本机构环评质量管理口径（本机构配置） | 无统一标准（本条依据为本机构配置的状态口径） | EG-003 |
| 《环境影响评价技术导则 总纲》 | HJ 2.1（现行版本号与条号本次未核实） | EG-004, EG-005, EG-007 |
| 《建设项目环境影响评价分类管理名录》 | 现行版本与条号本次未核实 | EG-006 |

**Boundary:** this plugin checks an **环评导则适用性核对表** for traceability — that each environmental element
names its applicable guideline, that the guideline number follows its published form, that the guideline's status
comes from your vocabulary, that an assessment method or an applicable standard is recorded, that elements are
not double-registered, that the sheet names its project and report type, and that no placeholder survives. It does
**not** decide whether an environmental assessment is compliant, whether the assessment level is right, whether a
prediction model applies, or whether the conclusions hold.

> ### ⚠️ What this plugin deliberately cannot do
>
> **It does not contain the guideline catalogue, and it does not map an element onto the guideline that should
> govern it.** Because of that it **cannot find the most consequential error: using the wrong guideline for an
> element.** Choosing between HJ 2.2, HJ 2.3, HJ 2.4, HJ 964 and the rest turns on the project's category and the
> element in question, and confirming it means reading the classification list and each guideline's scope. This
> limit is stated in the pack's header, in `EG-001`'s note, and in the troubleshooting section below.
>
> The 适用导则 column is therefore the register's own statement. Everything here checks what can be checked
> mechanically: is it written down, does the number look like a guideline number, is the status one you
> recognise, is a method or standard recorded.
>
> **The plugin also ships no current-version table** — tracking which guidelines are in force and which have
> been superseded means following the ministry's announcements, and the status vocabulary is yours to configure.
> `EG-002` checks the *form* of a number (`HJ 2.3—2018`) and never whether that number exists, is current, or
> matches the name next to it.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained** — the
> verification pass did not retrieve the guidelines' verbatim text, nor verify each one's current version.
> When the texts are in hand, replace each `excerpt` with the real clause and raise `kind` to `direct`.

## Compatibility

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-eia-guide-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-eia-guide-check contributors.
