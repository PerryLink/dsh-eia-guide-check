# dsh-eia-guide-check — 环评导则适用性核对

`dsh-eia-guide-check` 读取一份环境影响评价的导则适用性核对表——表头、加上每条评价要素一行——并核对这份核对表自身是否可追溯：每条要素是否指明适用导则、导则编号是否写成通用形式、导则状态是否取自本机构配置的取值、是否填写了评价方法或执行标准、要素是否重复登记、表头是否声明项目与环评文件类型、执行标准栏是否残留未替换的模板占位符。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某条要素行的适用导则名称与编号都是空的，会被报出吗？ | 会。`guideName` 与 `guideCode` 都为空时，`EG-001` 报出该行，因为这一行至少要指明其中一项。它只核对是否指明了导则，**不核对指明得对不对**：本插件不内置导则清单，也不做要素到导则的映射。 |
| 导则编号写成 `HJ 2.3`，没有年份，会被报出吗？ | 会。`EG-002` 按「HJ 数字—四位年份」的形式核对（如 `HJ 2.3—2018`），没有四位年份就匹配不上，会逐行报出。它只核对形式：不核对编号是否真实存在、是否现行有效，也不核对是否与旁边的名称对应。`guideCode` 栏为空时本条不报——空值不参与这项形式核对。 |
| 状态栏填的是 `现行`，为什么没查？ | 因为 `EG-003` 的 `values` 出厂为空，表示状态口径尚未配置：本条在 `skipped` 中报告自己不执行，并说明这一取值口径由本机构规定，而不是静默通过。配置之后，它也只核对所填值是否在册，不判断该导则是否真的现行有效。 |
| 评价方法填了，但执行标准栏还写着 `【待填】`，能查出来吗？ | `EG-004` 只要求 `method` 与 `standard` 至少填了一个，方法填了它就通过；它不判断方法是否适用、标准是否正确。残留的占位符由 `EG-007` 报出：它在执行标准栏里找配置的占位符词（`【`、`】`、`XXX`、`待填`、`TBD`、`示例` 等），报出命中的那一个。这些词可按本机构模板调整；执行标准栏整个为空时，这两条都不报。 |
| 同一要素 `地表水` 登记了两次，一次水质、一次底泥，会怎样？ | `EG-005` 报出重复的 `element` 值，并指出与哪一行重复，因为重复会让人无法判断该要素按哪一本导则评价。它只比对去掉空白后的字面值，且命中需要人工确认：同一要素分环境介质评价是常见情形，应在要素名称里写清子项，而不是简单删行。材料没有 `element` 栏时，本条报告无法执行，而不是静默通过。 |
| 表头没有项目名称，也没写环评文件类型，会怎样？ | `EG-006` 报出表头缺少 `project`、`reportType`，因为环评文件类型（`报告书`／`报告表`／`登记表`）决定了适用哪一套要求。它只核对表头是否声明，不判断该类型划分是否正确。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-eia-guide-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-eia-guide-check contributors.
