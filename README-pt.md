# dsh-eia-guide-check — Verificação da folha de aplicabilidade das diretrizes de avaliação de impacto ambiental

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-eia-guide-check` lê uma folha de aplicabilidade de diretrizes de uma avaliação de impacto ambiental —o cabeçalho do projeto mais uma linha por elemento avaliado— e verifica a rastreabilidade dessa própria folha: se cada elemento indica a diretriz que lhe é aplicável, se o número da diretriz segue a forma publicada, se o estado da diretriz vem do vocabulário que você configurar, se está registado um método de avaliação ou uma norma aplicável, se nenhum elemento está registado duas vezes, se o cabeçalho declara o projeto e o tipo de documento de avaliação, e se não resta nenhum marcador de modelo por substituir na coluna da norma aplicável.

## Como é a saída

![Terminal demo of dsh-eia-guide-check: real output over its EG-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-eia-guide-check/main/docs/assets/dsh-eia-guide-check-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `EG-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha de elemento deixa vazios o nome e o número da diretriz. Isso é reportado? | Sim. `EG-001` reporta essa linha quando `guideName` e `guideCode` estão ambos vazios, porque a linha tem de indicar pelo menos um deles. Verifica apenas se uma diretriz é indicada, nunca se é a correta para esse elemento: o plugin não inclui qualquer catálogo de diretrizes nem associa elementos a diretrizes. |
| O número da diretriz está escrito como `HJ 2.3`, sem ano. Isso é detetado? | Sim. `EG-002` verifica a forma «HJ número—ano de quatro dígitos», como em `HJ 2.3—2018`, pelo que um valor sem o ano de quatro dígitos não corresponde e é reportado linha a linha. Verifica apenas a forma: não que o número exista, não que esteja em vigor e não que corresponda ao nome ao lado. Uma célula `guideCode` vazia não é reportada aqui: os valores vazios ficam fora desta verificação de forma. |
| A coluna de estado diz `现行`. Porque é que nunca foi verificada? | Porque a lista `values` de `EG-003` vem vazia, ou seja, o vocabulário de estados ainda não está configurado: a regra reporta-se a si própria em `skipped`, com o motivo de que esse vocabulário é da instituição, em vez de passar em silêncio. Depois de configurado, verifica apenas se o valor preenchido consta da lista, não se a diretriz está realmente em vigor. |
| O método de avaliação está preenchido, mas a coluna da norma ainda diz `【待填】`. Isso é detetado? | `EG-004` exige apenas que um de `method` ou `standard` esteja preenchido, pelo que um método preenchido a satisfaz; não julga se o método é aplicável nem se a norma está correta. O marcador remanescente é reportado por `EG-007`, que procura na coluna da norma os termos configurados (`【`, `】`, `XXX`, `待填`, `TBD`, `示例` e semelhantes) e reporta o primeiro que encontra. Esses termos são ajustáveis, e uma célula de norma totalmente vazia não é reportada por nenhuma das duas regras. |
| O elemento `地表水` está registado duas vezes, uma para qualidade da água e outra para sedimentos. O que acontece? | `EG-005` reporta o valor repetido de `element` e indica com que linha anterior coincide, porque a repetição impede saber que diretriz rege esse elemento. Compara apenas o texto sem espaços e o resultado exige confirmação humana: avaliar um mesmo elemento por meio é normal, por isso escreva o subelemento no nome do elemento em vez de apagar a linha. Se a folha não tiver coluna `element`, a regra reporta que não pôde ser executada em vez de passar em silêncio. |
| O cabeçalho não traz o nome do projeto nem o tipo de documento de avaliação. O que acontece? | `EG-006` reporta que faltam ao cabeçalho `project` e `reportType`, porque o tipo de documento (`报告书`／`报告表`／`登记表`) determina que conjunto de requisitos se aplica. Verifica apenas que o cabeçalho os declare; não julga se a classificação do tipo está correta. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-eia-guide-check
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-eia-guide-check contributors.
