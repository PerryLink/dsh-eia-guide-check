<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-eia-guide-check-hero-en-light.webp" width="100%" alt="dsh-eia-guide-check: the left column carries the plugin name, two value lines and the note that it reads the sheet only and never rules on compliance; the right side is the bundled rule pack's evidence tiers — direct: 0 rules (no verbatim clause in the pack; every excerpt says so), derived-from-principle: 6 rules (EG-001, EG-002, EG-004, EG-005, EG-006, EG-007, ceiling warn), institutional-configuration: 1 rule (EG-003, ceiling info, shipped with values: [] so it lands in skipped); the footer shows the sample run's issues[] 1 (warn) and skipped[] 1.">
</picture>

# dsh-eia-guide-check

**Check an EIA guideline-applicability sheet for traceability — you get a list of which row, which column, and what to fix; the verdict stays with the reviewer.**

A data-only checker plugin for DeepSeek Harness: it reads one guideline-applicability sheet (the project header plus one row per assessed element), applies the versioned rule pack it ships (EG-001..EG-007), and lists only the differences it can point to inside the material — never a compliance verdict, never a liability finding.

[Install](#three-step-setup) · [Configuration](#configuration) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibility)
[![npm](https://img.shields.io/npm/v/dsh-eia-guide-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-eia-guide-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-eia-guide-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-eia-guide-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibility)

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

<sub>Community plugin, not affiliated with DeepSeek. Canonical repository: <https://github.com/PerryLink/dsh-eia-guide-check> (Gitee is a mirror).</sub>

## What it is

`dsh-eia-guide-check` reads one guideline-applicability sheet for an environmental impact assessment — the project header plus one row per assessed element — and checks that sheet's own traceability: that every element names its applicable guideline (name or number, at least one), that the guideline number follows the published form, that the guideline's status comes from the vocabulary you configure, that an assessment method or an applicable standard is recorded, that no element is registered twice, that the header declares the project and the report type, and that no unreplaced template placeholder survives in the standard column.

It does not decide whether an environmental assessment is compliant, whether the assessment level is right, whether a prediction model applies, or whether the conclusions hold.

- **Who it is for**: EIA preparers and environmental officers; no command line required — hand the material over in chat.
- **What you give it**: the source material the check works on (a table, register, or document); the original is never modified. Excel can be converted to JSON/YAML first, in chat if the platform supports it.
- **What you get back**: a list of "which row, which column, what is missing, how to fix it"; every check that could not run is listed in `skipped` with its reason.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-eia-guide-check-flow-v5-light.svg" width="100%" alt="dsh-eia-guide-check structure (column → rule wiring board): the 8 canonical columns of one applicability sheet (JSON/YAML) are wired to the 7 rules that read them — guideName and guideCode into EG-001, guideCode also into EG-002, guideStatus into EG-003, method and standard into EG-004, standard also into EG-007, element into EG-005, project and reportType into EG-006; every rule carries its severity ceiling (warn on six, info on one). There are only two exits: a finding enters issues[] (the sample: row 1 with guideName and guideCode blank), a rule that cannot run enters skipped[] with its reason (EG-003, values unset), and a rule that ran clean enters neither; an empty issue list is not a pass and the verdict stays with the reviewer.">
</picture>

## Three-step setup

1. **Install** (pick one channel):

   ```sh
   # git channel (latest main; equivalent to git+https://github.com/PerryLink/dsh-eia-guide-check.git)
   dsh plugin --profile <name> add github:PerryLink/dsh-eia-guide-check
   # npm channel (published releases)
   dsh plugin --profile <name> add dsh-eia-guide-check
   # tarball channel: pnpm pack in this repo, then
   dsh plugin --profile <name> add ./dsh-eia-guide-check-<version>.tgz
   ```

   The npm channel ships the built `lib/`; the git channel builds it at install time through the `prepare` script (tsdown), so no manual build is needed.

2. **Minimal config** (sane defaults; a bundle row without `config` uses every default, with the rule-pack path pointing at the bundled `rules/eia-guide-check.yaml`):

   ```yaml
   - insert:
       - id: dsh-eia-guide-check
         name: dsh-eia-guide-check
   ```

3. **Verify it mounts**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
   ```

   Then hand it a sheet. The bundled sample's expected output (`samples/quickstart/expected/result.json`):

   ```json
   {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
   ```

   Re-run it in this repository (build `lib/` first with `pnpm run build`):

   ```sh
   node samples/quickstart/run.mjs --json
   ```

**Uninstall**: `dsh plugin --profile <name> remove dsh-eia-guide-check` (or remove the row from the profile patch).

<details>
<summary>Use it in WorkBuddy / Coze</summary>

Search "Professional Document Check Suite" in WorkBuddy / Coze (the full set; this check is one part of it; availability as listed) to call the same checking capability without a command line.

</details>

<details>
<summary>Install from the DSH Desktop market</summary>

Every PerryLink plugin is listed in the built-in DSH Desktop market: **Market → Sources → Add source → paste** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ select**. Installation still requires the market's npm identity check and your confirmation.

</details>

## Core capabilities

`dsh-eia-guide-check` registers the `eia_guide_check` tool: it reads one guideline-applicability sheet, applies a versioned rule pack, and returns a report.

- **Seven rules in one data pack** — the rule pack is data, not code (`rules/eia-guide-check.yaml`); replacing it switches the whole rule set without touching a line of TypeScript.
- **Read-only on the material** — accepts JSON or YAML and never modifies the original; pure ESM, no network requests, no model calls.
- **No fabricated citations** — every rule carries `document` / `number` / `clause` / `excerpt` / `kind` / `source`; this pack obtained no guideline's verbatim clause text this pass, so every `excerpt` says so explicitly and stays marked `derived-from-principle`: a description is never dressed up as a quotation.
- **Severity follows the evidence** — `derived-from-principle` is capped at `warn`, institutional configuration (`institutional-configuration`) at `info`, and a test asserts it.
- **An empty issue list is never "nothing is wrong"** — every check that could not run is reported in `skipped` with its reason; a rule whose required list is unset reports itself in `skipped` rather than passing silently.
- **No guideline catalogue** — it has no way to map an element onto "the guideline that should govern it", so it cannot find the most consequential error: using the wrong guideline for an element. That takes the classification list and each guideline's scope.
- **No adjudicating wording** — the report lists differences and never pronounces on compliance, liability, or correctness; a wording guard enforces this and every report carries the disclaimer.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `EG-001` | each element names its applicable guideline (name or number) | warn | principle |
| `EG-002` | the guideline number follows its published form | warn | principle |
| `EG-003` | the guideline status comes from your vocabulary (off by default) | info | local |
| `EG-004` | a method or an applicable standard is recorded | warn | principle |
| `EG-005` | elements are not double-registered | warn | principle |
| `EG-006` | the sheet names its project and report type | warn | principle |
| `EG-007` | the standard column holds no unreplaced placeholder | warn | principle |

### Examples

These are the plugin's real entry points; install once, then call one. The first row of the table below is the detailed walkthrough, the remaining rows are short cases.

**Detailed example** — tool `eia_guide_check`, input:

```json
{"rows":[{"序号":"1","评价要素":"环境空气","导则名称":"","导则编号代码":"", ...}]}
```

Output:

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

| You ask | What it answers |
|---|---|
| One element row leaves both the guideline name and the guideline number blank. Is that reported? | Yes. `EG-001` reports the row when `guideName` and `guideCode` are both empty, because the row has to name at least one of them. It checks only whether a guideline is named, never whether the named guideline is the right one for that element: the plugin holds no guideline catalogue and does not map an element onto a guideline. |
| The guideline number is written as `HJ 2.3`, with no year. Is that caught? | Yes. `EG-002` checks the form `HJ <number>—<four-digit year>`, as in `HJ 2.3—2018`, so a value without the four-digit year does not match and is reported row by row. It checks the form only: not whether the number exists, not whether it is current, and not whether it matches the name beside it. A blank `guideCode` cell is left alone — empty values stay outside this form check. |
| The status column is filled with a value from our own status vocabulary. Why was it never checked? | Because `EG-003`'s `values` list ships empty, meaning the status vocabulary is not configured yet: the rule reports itself in `skipped`, with the reason that this vocabulary is the institution's own, rather than passing silently. Once configured, it checks only whether the filled value is on that list — not whether the guideline is really in force. |
| The assessment method is filled in, but the standard column still holds a leftover template placeholder. Is that caught? | `EG-004` requires only that one of `method` or `standard` is filled, so a filled method satisfies it; it does not judge whether the method applies or the standard is correct. The leftover placeholder is caught by `EG-007`, which reports the first configured term it finds in the standard column (bracketed markers, `XXX`, `TBD`, and similar). Those terms are adjustable, and a wholly empty standard cell is reported by neither rule. |
| `Surface water` is registered twice, once for water quality and once for sediment. What happens? | `EG-005` reports the repeated `element` value and names the earlier row it matches, because a duplicate makes it impossible to tell which guideline governs that element. It compares the text with whitespace removed only, and the finding needs human confirmation: assessing one element by medium is normal, so write the sub-item into the element name instead of deleting the row. With no `element` column the rule reports that it could not run rather than passing silently. |
| The header carries no project name and no report type. What happens? | `EG-006` reports the header as missing `project` and `reportType`, because the report type (report, form, or registration sheet) decides which set of requirements applies. It checks only that the header declares them; it does not judge whether the type was classified correctly. |

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| Environmental Impact Assessment Technical Guidelines series | current version of each guideline not verified this pass | EG-001, EG-002 |
| Institutional EIA quality-management vocabulary (configured by your institution) | no unified standard (the basis is the institution's configured status vocabulary) | EG-003 |
| Environmental Impact Assessment Technical Guidelines — General Programme | HJ 2.1 (current version and clause numbers not verified this pass) | EG-004, EG-005, EG-007 |
| Catalogue for the Classification Management of Environmental Impact Assessment of Construction Projects | current version and clause numbers not verified this pass | EG-006 |

**Boundary:** this plugin checks an **EIA guideline-applicability sheet** for traceability — that each environmental element names its applicable guideline, that the guideline number follows its published form, that the guideline's status comes from your vocabulary, that an assessment method or an applicable standard is recorded, that elements are not double-registered, that the sheet names its project and report type, and that no placeholder survives. It does **not** decide whether an environmental assessment is compliant, whether the assessment level is right, whether a prediction model applies, or whether the conclusions hold.

> ### ⚠️ Read this before trusting a citation in the report
>
> **`excerpt` status is per rule, not uniform.** Some rules quote the clause verbatim (`kind: direct`), some are derived from the principle of the cited articles (`kind: derived-from-principle`, capped at `warn`), and some use thresholds your institution configures (`kind: institutional-configuration`, capped at `info`). The pack never paraphrases a quotation: when the text was not obtained, the `excerpt` field says so and the reasoning lives in `note`; a test asserts that no rule claims a quotation it does not have. **For any rule still marked as not obtained, replace the `excerpt` with the real clause and raise `kind` to `direct` once the text is in hand.**
>
> The conclusion is the reviewer's: this plugin lists differences it can point to in the material and does not decide facts or compliance.

## Configuration

All tunables are Schemastery `Config` fields in `src/config.ts` (changeable from cordis.yml); the per-rule thresholds live in the rule pack under `rules/`. An id-targeted override replaces the whole row — restate every key you need.

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `EG-002` `pattern` — the number's shape, `HJ <number> (optional decimal) — <four-digit year>` by default. Widen it if your register writes numbers another way.
- `EG-003` `values` — your status vocabulary, e.g. `[in force, repealed, superseded, partly applicable]`. Empty means no check; no current-version table is built in.
- `EG-007` `terms` — the placeholders to look for.

Example override in your profile patch:

```yaml
- insert:
    - id: dsh-eia-guide-check
      name: dsh-eia-guide-check
      config:
        disabledRules: [EG-003]
        timeoutMs: 180000
```

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

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the sheet's own column names are kept, so a finding names the column it read. Fields are optional at the reader layer and validated by the check engine, so a partially exported sheet produces "missing item" findings instead of a crash.

## Rule sources

Rule data lives in `rules/eia-guide-check.yaml`, separated from the code: every rule carries document, number, clause in the source's own numbering, a verbatim excerpt, and a source URL. The pack's header states in full that the plugin holds no guideline catalogue, does no element-to-guideline mapping, and did not verify each guideline's current version; each rule's `note` repeats the part that matters for that rule. The load-time guard requires `document` / `clause` / `excerpt` / `source` and forbids a principle-derived or locally configured check from being `error`. `check:citations` audits the excerpts: a segment that claims to be a verbatim quotation must be traceable to obtained source text, while rules that state the text was not obtained count as placeholders; `rules/citations-baseline.json` can only shrink. A pack that overstates its basis fails at load time instead of producing a confident-looking report.

## FAQ

<details>
<summary>Will it tell us that an element uses the wrong guideline?</summary>

No — this is the plugin's most important boundary. It holds no guideline catalogue and does not map an element onto the guideline that should govern it; the guideline column is the register's own statement, and the plugin checks only that it is written, that the number's form holds, and that the status is one of your configured values. Deciding between HJ 2.2 and HJ 2.3 takes the classification list and each guideline's scope; that conclusion stays with the EIA engineer.

</details>

<details>
<summary>The status column is filled in, so why does `EG-003` never report?</summary>

Because `EG-003`'s `values` list ships empty, meaning the status vocabulary is not configured: the rule reports itself in `skipped` with the reason that this vocabulary is the institution's own, rather than passing silently. Once `values` is set, it still checks only whether the filled value is on the list, not whether the guideline is really in force — that takes tracking the ministry's publication and repeal notices, and no version table is built in.

</details>

<details>
<summary>Can an empty `issues` list be read as "nothing is wrong"?</summary>

No. Every check that could not run is listed in `skipped` with its reason (an unset vocabulary, a missing `element` column, and so on). Read `issues` and `skipped` together before drawing any conclusion from a report; `skippedCount` counts only rules that genuinely did not run, not rules that ran clean.

</details>

<details>
<summary>My sheet is an Excel file. Can I use it directly?</summary>

Yes — convert it to JSON or YAML first; in chat the platform can do the conversion for you if supported. The tool only reads the material and never modifies the original.

</details>

<details>
<summary>Will it cope with a full sheet or a whole directory at once?</summary>

The tool works in both `native` and `ptc` modes; for batch work (a set of EIA sheets or a whole directory) use `ptc`, where the schema cost is paid once. The checks themselves are local column matching — no network requests, no model calls; `timeoutMs` (default 120 s) is the cooperative timeout budget.

</details>

## Troubleshooting

- **It did not flag the wrong guideline for an element.** By design: it has no catalogue and never maps an element to one. Confirm against the classification list and each guideline's scope yourself.
- **`EG-002` passes a number I know is withdrawn.** The check reads the number's form, never its validity or currency. Tracking versions is a different job.
- **`EG-002` fires on a number I wrote correctly.** The pattern wants the `HJ` prefix, the number, and a four-digit year separated by a dash or em dash. Adjust the pattern, or fix the cell.
- **`EG-003` never runs.** Its vocabulary is empty; fill it with the statuses your quality system uses.
- **`EG-005` fires on two rows for one element.** Assessing one element by medium (surface water quality and sediment, for instance) is legitimate — write the sub-item into the element name rather than deleting a row.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if your runtime sits outside it, grant an explicit exemption: `dsh plugin --profile <name> allow-version dsh-eia-guide-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a full assessment sheet use `ptc` |

## Ecosystem & quality

- [Gitee mirror](https://gitee.com/perrylink/dsh-eia-guide-check) (sync mirror; GitHub is canonical)
- [dshfind plugin page](https://dshfind.com/plugins/PerryLink/dsh-eia-guide-check) (installs and ranking)
- [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-eia-guide-check) (driven by [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listed)
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile <name> add dsh-eia-guide-check` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking)
- [Ecosystem knowledge base](https://perrylink.github.io/dsh-plugin-guide/) — plugin development guide · measured selection data · maintenance criteria

## Development

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: shared table-plugin suite + paired fixtures
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # dependency specs resolve from the registry
pnpm run check:lockfile                             # lockfile drift check
pnpm run check:readmes                              # five-language README consistency
pnpm run check:citations                            # rule-pack citation baseline
node ../scripts/sync-shared.mjs dsh-eia-guide-check   # refresh src/shared from ../_shared
pnpm pack                                           # the published tarball
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and the check engine, and the rule pack declares every check. Local sample run (needs `pnpm run build` first to produce `lib/`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
```

The sample input lives in `samples/quickstart/input/`, the expected output in `samples/quickstart/expected/result.json`, and a screenshot in `docs/assets/quickstart.png`. The README images are generated programmatically by [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) and are safe to re-run; the older single-skin flow diagram and demo images stay in `docs/assets/` for external deep links, while the READMEs reference only the new light/dark pair.

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `eia`, `guide`

## Family & thanks

This project is part of the DeepSeek Harness plugin family from [PerryLink](https://github.com/PerryLink) (all Apache-2.0). Full family index: [choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) and [all plugins](https://github.com/PerryLink). If it is useful, **a star helps the next person find it** — nothing is gated behind it.

- [@PerryLink](https://github.com/PerryLink) — creator and maintainer: the data-only rule pack (EG-001..EG-007), the `eia_guide_check` tool, the citation baseline, and the five-language docs.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 FROZEN — see the repo README |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 FROZEN — see the repo README |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRED (repo archived) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 FROZEN — see the repo README |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRED (repo archived) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED (repo archived) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED (repo archived) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED (repo archived) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-eia-guide-check contributors

<p align="center"><sub>Apache-2.0 · Community plugin, not affiliated with DeepSeek.</sub></p>
