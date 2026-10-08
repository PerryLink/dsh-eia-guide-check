# dsh-eia-guide-check

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
