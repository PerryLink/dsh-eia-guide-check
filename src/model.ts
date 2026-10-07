/**
 * dsh-eia-guide-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'eia_guide_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  guideNo: ['序号', '导则编号', '编号', 'guideNo'],
  element: ['评价要素', '环境要素', '要素', 'element'],
  guideName: ['导则名称', '适用导则', '标准名称', 'guideName'],
  guideCode: ['导则编号代码', '标准号', 'HJ 编号', 'guideCode'],
  guideStatus: ['导则状态', '是否现行', '状态', 'guideStatus'],
  appliedIn: ['应用章节', '报告章节', '应用位置', 'appliedIn'],
  method: ['评价方法', '预测方法', '方法', 'method'],
  baseline: ['现状监测', '现状调查', 'baseline'],
  scope: ['评价范围', '评价等级', 'scope'],
  factor: ['评价因子', '监测因子', 'factor'],
  standard: ['执行标准', '排放标准', 'standard'],
  checker: ['校核人', '复核人', 'checker'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'guides', '导则'],
  columns: COLUMNS,
  header: {
  project: ['project', '项目名称', '工程名称'],
  industry: ['industry', '行业类别', '项目类别'],
  reportType: ['reportType', '报告类型', '环评文件类型'],
  compiler: ['compiler', '编制单位', '环评单位'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '评价要素',
  'element',
  '导则名称',
  'guideName',
  '评价方法',
  'method',
  '执行标准',
  'standard',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
