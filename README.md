# dsh-eia-guide-check — Environmental impact assessment guideline applicability sheet check

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-eia-guide-check` reads one guideline-applicability sheet for an environmental impact assessment — the project header plus one row per assessed element — and checks that sheet's own traceability: that every element names its applicable guideline, that the guideline number follows the published form, that the guideline's status comes from the vocabulary you configure, that an assessment method or an applicable standard is recorded, that no element is registered twice, that the header declares the project and the report type, and that no unreplaced template placeholder survives in the standard column.

## What it looks like

![Terminal demo of dsh-eia-guide-check: real output over its EG-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-eia-guide-check/main/docs/assets/dsh-eia-guide-check-demo.png)

Real output from this plugin over its own `EG-001` test fixture — not a mock-up. The rule pack ships no invented quotations, so a finding names both the clause it applied and the fact that the clause text was not obtained.

## What it answers

| You ask | What it answers |
|---|---|
| One element row leaves both the guideline name and the guideline number blank. Is that reported? | Yes. `EG-001` reports the row when `guideName` and `guideCode` are both empty, because the row has to name at least one of them. It checks only whether a guideline is named, never whether the named guideline is the right one for that element: the plugin holds no guideline catalogue and does not map an element onto a guideline. |
| The guideline number is written as `HJ 2.3`, with no year. Is that caught? | Yes. `EG-002` checks the form `HJ <number>—<four-digit year>`, as in `HJ 2.3—2018`, so a value without the four-digit year does not match and is reported row by row. It checks the form only: not whether the number exists, not whether it is current, and not whether it matches the name beside it. A blank `guideCode` cell is left alone — empty values stay outside this form check. |
| The status column says `现行`. Why was it never checked? | Because `EG-003`'s `values` list ships empty, meaning the status vocabulary is not configured yet: the rule reports itself in `skipped`, with the reason that this vocabulary is the institution's own, rather than passing silently. Once configured, it checks only whether the filled value is on that list — not whether the guideline is really in force. |
| The assessment method is filled in, but the standard column still reads `【待填】`. Is that caught? | `EG-004` requires only that one of `method` or `standard` is filled, so a filled method satisfies it; it does not judge whether the method applies or the standard is correct. The leftover placeholder is caught by `EG-007`, which reports the first configured term it finds in the standard column (`【`, `】`, `XXX`, `待填`, `TBD`, `示例` and similar). Those terms are adjustable, and a wholly empty standard cell is reported by neither rule. |
| `地表水` is registered twice, once for water quality and once for sediment. What happens? | `EG-005` reports the repeated `element` value and names the earlier row it matches, because a duplicate makes it impossible to tell which guideline governs that element. It compares the text with whitespace removed only, and the finding needs human confirmation: assessing one element by medium is normal, so write the sub-item into the element name instead of deleting the row. With no `element` column the rule reports that it could not run rather than passing silently. |
| The header carries no project name and no report type. What happens? | `EG-006` reports the header as missing `project` and `reportType`, because the report type (`报告书`／`报告表`／`登记表`) decides which set of requirements applies. It checks only that the header declares them; it does not judge whether the type was classified correctly. |

## Standards it follows

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a full assessment sheet use `ptc` |

## What it does

Registers the `eia_guide_check` tool. It reads one guideline-applicability sheet — the project header plus one row
per element — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `EG-001` | each element names its applicable guideline | warn | principle |
| `EG-002` | the guideline number follows its published form | warn | principle |
| `EG-003` | the guideline status comes from your vocabulary (off by default) | info | local |
| `EG-004` | a method or an applicable standard is recorded | warn | principle |
| `EG-005` | elements are not double-registered | warn | principle |
| `EG-006` | the sheet names its project and report type | warn | principle |
| `EG-007` | the standard column holds no unreplaced placeholder | warn | principle |

## Install

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `EG-002` `pattern` — the number's shape, `HJ 数字（可带小数）—四位年份` by default. Widen it if your
  register writes numbers another way.
- `EG-003` `values` — your status vocabulary, e.g. `[现行, 已废止, 被替代, 部分适用]`. Empty means no check;
  no current-version table is built in.
- `EG-007` `terms` — the placeholders to look for.

## Material format

The tool accepts JSON or YAML:

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

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the sheet's own column
names are kept, so a finding names the column it read.

## Rule sources

Rule data lives in `rules/eia-guide-check.yaml`. Its header explains that the plugin holds no guideline
catalogue, does no element-to-guideline mapping, and did not verify each guideline's current version. The
load-time guard still requires a document, clause, excerpt and source per rule, and still forbids a
principle-derived or locally configured check from being `error`.

## Troubleshooting

- **It did not flag the wrong guideline for an element.** By design: it has no catalogue and never maps an
  element to one. Confirm against the classification list and each guideline's scope yourself.
- **`EG-002` passes a number I know is withdrawn.** The check reads the number's form, never its validity or
  currency. Tracking versions is a different job.
- **`EG-002` fires on a number I wrote correctly.** The pattern wants the `HJ` prefix, the number, and a
  four-digit year separated by a dash or em dash. Adjust the pattern, or fix the cell.
- **`EG-003` never runs.** Its vocabulary is empty; fill it with the statuses your quality system uses.
- **`EG-005` fires on two rows for one element.** Assessing one element by medium (surface water quality and
  sediment, for instance) is legitimate — write the sub-item into the element name rather than deleting a row.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-eia-guide-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-eia-guide-check   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-eia-guide-check contributors.
