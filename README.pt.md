<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-eia-guide-check-hero-en-light.webp" width="100%" alt="dsh-eia-guide-check: a coluna esquerda traz o nome do plugin, duas linhas de valor e a nota de que apenas lê a folha e não julga conformidade; à direita estão os níveis de evidência do pacote de regras incluído — direct: 0 regras (não há texto literal no pacote; cada excerpt indica-o), derived-from-principle: 6 regras (EG-001, EG-002, EG-004, EG-005, EG-006, EG-007, teto warn), institutional-configuration: 1 regra (EG-003, teto info, com values: [] de fábrica, por isso vai para skipped); o rodapé mostra a execução de exemplo: issues[] 1 (warn) e skipped[] 1.">
</picture>

# dsh-eia-guide-check

**Verifique a rastreabilidade de uma folha de aplicabilidade das diretrizes de AIA: você recebe uma lista de qual linha, qual coluna e o que corrigir; a conclusão fica com o revisor.**

Um plugin verificador somente de dados para o DeepSeek Harness: lê uma folha de aplicabilidade das diretrizes (o cabeçalho do projeto mais uma linha por elemento avaliado), aplica o pacote de regras versionado que acompanha (EG-001..EG-007) e lista apenas as divergências que consegue apontar dentro do material — nunca um veredicto de conformidade nem uma atribuição de responsabilidade.

[Instalar](#instalação-em-três-passos) · [Configuração](#configuração) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidade)
[![npm](https://img.shields.io/npm/v/dsh-eia-guide-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-eia-guide-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-eia-guide-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-eia-guide-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidade)

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

<sub>Plugin da comunidade, sem afiliação com a DeepSeek. Repositório canônico: <https://github.com/PerryLink/dsh-eia-guide-check> (o Gitee é um espelho).</sub>

## O que é

`dsh-eia-guide-check` lê uma folha de aplicabilidade de diretrizes de uma avaliação de impacto ambiental —o cabeçalho do projeto mais uma linha por elemento avaliado— e verifica a rastreabilidade dessa própria folha: se cada elemento indica a diretriz que lhe é aplicável (nome ou número, pelo menos um), se o número da diretriz segue a forma publicada, se o estado da diretriz vem do vocabulário que você configurar, se está registado um método de avaliação ou uma norma aplicável, se nenhum elemento está registado duas vezes, se o cabeçalho declara o projeto e o tipo de documento de avaliação, e se não resta nenhum marcador de modelo por substituir na coluna da norma aplicável.

Não decide se a avaliação de impacto ambiental está em conformidade, se o nível de avaliação é o correto, se um modelo de previsão se aplica nem se as suas conclusões se sustentam.

- **Para quem**: elaboradores de AIA e responsáveis ambientais; não é preciso linha de comando — entregue o material no chat.
- **O que você entrega**: o material de origem sobre o qual a verificação trabalha (uma tabela, um registo ou um documento); o original nunca é alterado. O Excel pode ser convertido antes para JSON/YAML, no chat se a plataforma permitir.
- **O que você recebe**: uma lista de «qual linha, qual coluna, o que falta e como corrigir»; cada verificação que não pôde ser executada aparece em `skipped` com o motivo.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-eia-guide-check-flow-v5-light.svg" width="100%" alt="Estrutura do dsh-eia-guide-check (placa de ligação coluna → regra): as 8 colunas canónicas de uma folha de aplicabilidade (JSON/YAML) ligam-se às 7 regras que as leem — guideName e guideCode para EG-001, guideCode também para EG-002, guideStatus para EG-003, method e standard para EG-004, standard também para EG-007, element para EG-005, project e reportType para EG-006; cada regra leva o seu teto de gravidade (warn em seis, info numa). Há apenas duas saídas: o que foi encontrado vai para issues[] (o exemplo: linha 1 com guideName e guideCode vazios), o que não pôde correr vai para skipped[] com o motivo (EG-003, values por configurar), e uma regra que correu sem achados não entra em nenhuma; uma lista vazia não é uma aprovação e a conclusão fica com o revisor.">
</picture>

## Instalação em três passos

1. **Instale** (escolha um canal):

   ```sh
   # canal git (último main; equivalente a git+https://github.com/PerryLink/dsh-eia-guide-check.git)
   dsh plugin --profile <name> add github:PerryLink/dsh-eia-guide-check
   # canal npm (versões publicadas)
   dsh plugin --profile <name> add dsh-eia-guide-check
   # canal tarball: pnpm pack neste repositório e depois
   dsh plugin --profile <name> add ./dsh-eia-guide-check-<version>.tgz
   ```

   O canal npm instala o `lib/` já construído; o canal git constrói-o na instalação através do script `prepare` (tsdown), sem compilação manual.

2. **Configuração mínima** (os padrões já funcionam; uma linha de bundle sem `config` usa todos os padrões, com o caminho do pacote de regras a apontar para o `rules/eia-guide-check.yaml` incluído):

   ```yaml
   - insert:
       - id: dsh-eia-guide-check
         name: dsh-eia-guide-check
   ```

3. **Verifique que ele monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
   ```

   Depois entregue-lhe uma folha. A saída esperada do exemplo incluído (`samples/quickstart/expected/result.json`):

   ```json
   {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
   ```

   Pode reexecutá-lo neste repositório (primeiro `pnpm run build` para produzir `lib/`):

   ```sh
   node samples/quickstart/run.mjs --json
   ```

**Desinstalar**: `dsh plugin --profile <name> remove dsh-eia-guide-check` (ou remova a linha do patch do perfil).

<details>
<summary>Usar no WorkBuddy / Coze</summary>

Pesquise «Professional Document Check Suite» (o conjunto completo; esta verificação é uma das suas partes; disponibilidade conforme o mercado) no WorkBuddy / Coze para usar a mesma capacidade de verificação sem linha de comando.

</details>

<details>
<summary>Instalar a partir do mercado do DSH Desktop</summary>

Todos os plugins PerryLink podem ser explorados no mercado integrado do DSH Desktop: **Market → Sources → add source → colar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ selecionar**. A instalação continua a passar pela verificação de identidade npm do mercado e pela sua confirmação.

</details>

## Capacidades principais

`dsh-eia-guide-check` registra a ferramenta `eia_guide_check`: lê uma folha de aplicabilidade de diretrizes, aplica um pacote de regras versionado e devolve um relatório.

- **Sete regras num pacote de dados** — o pacote de regras é dados, não código (`rules/eia-guide-check.yaml`); substituí-lo troca todo o conjunto de regras sem tocar numa linha de TypeScript.
- **Somente leitura sobre o material** — aceita JSON ou YAML e nunca altera o original; ESM puro, sem pedidos de rede nem chamadas ao modelo.
- **Sem citações inventadas** — cada regra traz `document` / `number` / `clause` / `excerpt` / `kind` / `source`; este pacote não obteve nesta passagem o texto literal de nenhuma diretriz, por isso cada `excerpt` o diz explicitamente e fica marcado `derived-from-principle`: uma descrição nunca é apresentada como citação.
- **A gravidade segue a evidência** — `derived-from-principle` tem teto `warn`, a configuração institucional (`institutional-configuration`) teto `info`, e um teste verifica-o.
- **Uma lista de problemas vazia nunca significa «não há nada errado»** — cada verificação que não pôde ser executada é reportada em `skipped` com o motivo; uma regra cuja lista obrigatória não está configurada reporta-se a si própria em `skipped` em vez de passar em silêncio.
- **Sem catálogo de diretrizes** — não consegue mapear um elemento para «a diretriz que o deveria reger», por isso não deteta o erro mais consequente: usar a diretriz errada para um elemento. Isso exige a lista de classificação e o âmbito de cada diretriz.
- **Sem linguagem que adjudique** — o relatório lista divergências e nunca se pronuncia sobre conformidade, responsabilidade ou correção; um guardião de redação impõe-no e todo relatório traz o aviso legal.

| Regra | Verificação | Gravidade | Tipo de base |
|---|---|---|---|
| `EG-001` | cada elemento indica a diretriz aplicável (nome ou número) | warn | principle |
| `EG-002` | o número da diretriz segue a forma publicada | warn | principle |
| `EG-003` | o estado da diretriz vem do seu vocabulário (desligada por padrão) | info | local |
| `EG-004` | está registado um método ou uma norma aplicável | warn | principle |
| `EG-005` | os elementos não estão registados duas vezes | warn | principle |
| `EG-006` | a folha declara o projeto e o tipo de documento | warn | principle |
| `EG-007` | a coluna da norma não tem marcadores por substituir | warn | principle |

### Exemplos

São os pontos de entrada reais do plugin; instale uma vez e chame um. A primeira linha da tabela seguinte é o caso detalhado e as restantes são casos curtos.

**Exemplo detalhado** — ferramenta `eia_guide_check`, entrada:

```json
{"rows":[{"序号":"1","评价要素":"环境空气","导则名称":"","导则编号代码":"", ...}]}
```

Saída:

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

| Você pergunta | O que ele responde |
|---|---|
| Uma linha de elemento deixa vazios o nome e o número da diretriz. Isso é reportado? | Sim. `EG-001` reporta essa linha quando `guideName` e `guideCode` estão ambos vazios, porque a linha tem de indicar pelo menos um deles. Verifica apenas se uma diretriz é indicada, nunca se é a correta para esse elemento: o plugin não inclui qualquer catálogo de diretrizes nem associa elementos a diretrizes. |
| O número da diretriz está escrito como `HJ 2.3`, sem ano. Isso é detetado? | Sim. `EG-002` verifica a forma «HJ número—ano de quatro dígitos», como em `HJ 2.3—2018`, pelo que um valor sem o ano de quatro dígitos não corresponde e é reportado linha a linha. Verifica apenas a forma: não que o número exista, não que esteja em vigor e não que corresponda ao nome ao lado. Uma célula `guideCode` vazia não é reportada aqui: os valores vazios ficam fora desta verificação de forma. |
| A coluna de estado está preenchida com um valor do nosso próprio vocabulário. Porque é que nunca foi verificada? | Porque a lista `values` de `EG-003` vem vazia, ou seja, o vocabulário de estados ainda não está configurado: a regra reporta-se a si própria em `skipped`, com o motivo de que esse vocabulário é da instituição, em vez de passar em silêncio. Depois de configurado, verifica apenas se o valor preenchido consta da lista, não se a diretriz está realmente em vigor. |
| O método de avaliação está preenchido, mas a coluna da norma ainda tem um marcador de modelo por substituir. Isso é detetado? | `EG-004` exige apenas que um de `method` ou `standard` esteja preenchido, pelo que um método preenchido a satisfaz; não julga se o método é aplicável nem se a norma está correta. O marcador remanescente é reportado por `EG-007`, que procura na coluna da norma o primeiro termo configurado que encontra (marcadores entre parênteses retos, `XXX`, `TBD` e semelhantes). Esses termos são ajustáveis, e uma célula de norma totalmente vazia não é reportada por nenhuma das duas regras. |
| O elemento `地表水` está registado duas vezes, uma para qualidade da água e outra para sedimentos. O que acontece? | `EG-005` reporta o valor repetido de `element` e indica com que linha anterior coincide, porque a repetição impede saber que diretriz rege esse elemento. Compara apenas o texto sem espaços e o resultado exige confirmação humana: avaliar um mesmo elemento por meio é normal, por isso escreva o subelemento no nome do elemento em vez de apagar a linha. Se a folha não tiver coluna `element`, a regra reporta que não pôde ser executada em vez de passar em silêncio. |
| O cabeçalho não traz o nome do projeto nem o tipo de documento de avaliação. O que acontece? | `EG-006` reporta que faltam ao cabeçalho `project` e `reportType`, porque o tipo de documento (memória, formulário ou ficha de registo) determina que conjunto de requisitos se aplica. Verifica apenas que o cabeçalho os declare; não julga se a classificação do tipo está correta. |

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| Série de Diretrizes Técnicas de Avaliação de Impacto Ambiental | versão em vigor de cada diretriz não verificada nesta passagem | EG-001, EG-002 |
| Critério institucional de gestão da qualidade de AIA (configurado pela sua instituição) | sem norma unificada (a base é o vocabulário de estados configurado pela instituição) | EG-003 |
| Diretrizes Técnicas de Avaliação de Impacto Ambiental — Programa Geral | HJ 2.1 (versão em vigor e números de cláusula não verificados nesta passagem) | EG-004, EG-005, EG-007 |
| Catálogo para a Gestão da Classificação da Avaliação de Impacto Ambiental de Projetos de Construção | versão em vigor e números de cláusula não verificados nesta passagem | EG-006 |

**Limite:** este plugin verifica a rastreabilidade de uma **folha de aplicabilidade de diretrizes de AIA** —que cada elemento ambiental indica a diretriz aplicável, que o número da diretriz segue a forma publicada, que o estado vem do seu vocabulário, que está registado um método de avaliação ou uma norma aplicável, que os elementos não estão duplicados, que a folha declara o projeto e o tipo de documento, e que não resta nenhum marcador. **Não** decide se a avaliação de impacto ambiental está em conformidade, se o nível de avaliação é o correto, se um modelo de previsão se aplica nem se as conclusões se sustentam.

> ### ⚠️ Leia isto antes de confiar numa citação do relatório
>
> **O estado de `excerpt` é por regra, não uniforme.** Algumas regras citam a cláusula literalmente (`kind: direct`), outras derivam do princípio dos artigos citados (`kind: derived-from-principle`, teto `warn`) e outras usam limiares que a sua instituição configura (`kind: institutional-configuration`, teto `info`). O pacote nunca parafraseia uma citação: quando o texto não foi obtido, o campo `excerpt` di-lo e o raciocínio vive em `note`; um teste exige que nenhuma regra afirme uma citação que não tem. **Para qualquer regra ainda marcada como não obtida, substitua o `excerpt` pela cláusula real e eleve `kind` para `direct` quando tiver o texto.**
>
> A conclusão é do revisor: este plugin lista divergências que consegue apontar no material e não decide factos nem conformidade.

## Configuração

Todos os parâmetros são campos Schemastery `Config` de `src/config.ts` (alteráveis a partir do cordis.yml); os limiares por regra vivem no pacote de regras em `rules/`. Uma sobreposição por id substitui a linha inteira: repita todas as chaves de que precisa.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

Parâmetros por regra que vale a pena conhecer:

- `EG-002` `pattern` — a forma do número, por padrão «HJ número (decimal opcional) — ano de quatro dígitos». Alargue-a se o seu registo escrever os números de outra maneira.
- `EG-003` `values` — o seu vocabulário de estados, p. ex. `[em vigor, revogada, substituída, parcialmente aplicável]`. Vazio significa sem verificação; não há tabela de versões em vigor incorporada.
- `EG-007` `terms` — os marcadores a procurar.

Exemplo de sobreposição no seu patch de perfil:

```yaml
- insert:
    - id: dsh-eia-guide-check
      name: dsh-eia-guide-check
      config:
        disabledRules: [EG-003]
        timeoutMs: 180000
```

## Formato do material

A ferramenta aceita JSON ou YAML:

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

Os nomes de coluna são comparados sem distinguir maiúsculas e ignorando espaços, sublinhados e hífenes; os nomes de coluna da folha são mantidos, por isso um achado nomeia a coluna que leu. Os campos são opcionais na camada de leitura e validados pelo motor, pelo que uma folha parcialmente exportada produz achados de «falta um item» em vez de uma falha.

## Fontes das regras

Os dados das regras vivem em `rules/eia-guide-check.yaml`, separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, extrato literal e URL de origem. O cabeçalho do pacote declara por completo que o plugin não inclui catálogo de diretrizes, não associa elementos a diretrizes e não verificou a versão em vigor de cada uma; a `note` de cada regra repete a parte que lhe diz respeito. O guardião de carregamento exige `document` / `clause` / `excerpt` / `source` e proíbe que uma verificação derivada de princípios ou configurada localmente seja marcada como `error`. `check:citations` audita os extratos: um segmento que se apresenta como citação literal tem de ser rastreável até ao texto de origem obtido, enquanto as regras que declaram não ter obtido o texto contam como marcadores; `rules/citations-baseline.json` só pode encolher. Um pacote que exagere a sua base falha ao carregar em vez de produzir um relatório com aparência sólida.

## FAQ

<details>
<summary>Ele dirá que um elemento usa a diretriz errada?</summary>

Não: é o limite mais importante do plugin. Não inclui catálogo de diretrizes nem associa um elemento à diretriz que o deveria reger; a coluna da diretriz é a declaração da própria folha, e o plugin só verifica que está escrita, que a forma do número se sustenta e que o estado está entre os valores que você configurou. Decidir entre HJ 2.2 e HJ 2.3 exige a lista de classificação e o âmbito de cada diretriz; essa conclusão fica com o engenheiro de AIA.

</details>

<details>
<summary>A coluna de estado está preenchida, então porque é que `EG-003` nunca reporta?</summary>

Porque a lista `values` de `EG-003` vem vazia, ou seja, o vocabulário de estados não está configurado: a regra reporta-se a si própria em `skipped` com o motivo de que esse vocabulário é da instituição, em vez de passar em silêncio. Depois de configurado, continua a verificar apenas se o valor preenchido consta da lista, não se a diretriz está realmente em vigor; isso exige acompanhar os anúncios de publicação e revogação do ministério, e não há tabela de versões incorporada.

</details>

<details>
<summary>Uma lista `issues` vazia pode ser lida como «não há nada errado»?</summary>

Não. Cada verificação que não pôde ser executada aparece em `skipped` com o motivo (um vocabulário por configurar, uma coluna `element` ausente, etc.). Leia `issues` e `skipped` em conjunto antes de tirar qualquer conclusão; `skippedCount` conta apenas as regras que de facto não correram, não as que correram limpas.

</details>

<details>
<summary>A minha folha é um ficheiro Excel. Posso usá-lo diretamente?</summary>

Sim: converta primeiro para JSON ou YAML; no chat a plataforma pode fazer a conversão se o permitir. A ferramenta apenas lê o material e nunca altera o original.

</details>

<details>
<summary>Aguenta uma folha completa ou um diretório inteiro de uma vez?</summary>

A ferramenta funciona nos modos `native` e `ptc`; para trabalho em lote (um conjunto de folhas de AIA ou um diretório completo) use `ptc`, onde o custo do esquema é pago uma só vez. As verificações são correspondência local de colunas, sem pedidos de rede nem chamadas ao modelo; `timeoutMs` (120 s por padrão) é o orçamento de tempo limite cooperativo.

</details>

## Solução de problemas

- **Não assinalou a diretriz errada de um elemento.** É por design: não tem catálogo e nunca associa um elemento a uma diretriz. Confirme com a lista de classificação e o âmbito de cada diretriz.
- **`EG-002` aceita um número que sei estar revogado.** A verificação lê a forma do número, nunca a sua validade ou vigência. Acompanhar versões é outro trabalho.
- **`EG-002` dispara num número que escrevi bem.** O padrão exige o prefixo `HJ`, o número e um ano de quatro dígitos separados por hífen ou travessão. Ajuste o padrão ou corrija a célula.
- **`EG-003` nunca corre.** O seu vocabulário está vazio; preencha-o com os estados que o seu sistema de qualidade usa.
- **`EG-005` dispara em duas linhas do mesmo elemento.** Avaliar um mesmo elemento por meio (qualidade da água superficial e sedimentos, por exemplo) é legítimo: escreva o subelemento no nome do elemento em vez de apagar uma linha.
- **O plugin instala mas a ferramenta não aparece.** Confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o produziu; um `main` errado faz o carregador saltar a entrada em silêncio.
- **`dsh plugin add` recusa o pacote por incompatibilidade.** A faixa de peers cobre `0.1.x` e `0.2.x`; se o seu runtime estiver fora, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-eia-guide-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reporta `manifest-peers` como falha.** O verificador estático compara com uma faixa de peers codificada anterior à linha 0.2. O runtime aplica a compatibilidade de peers na instalação, por isso a faixa declarada é a correta; é um problema conhecido do `dsh-plugin-dev`.

## Compatibilidade

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-rc.2`. `engines.dsh` é declarado como `>=0.2.1-0 <0.3.0` e o host aplica-o desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native` e `ptc`; para uma folha de avaliação completa use `ptc` |

## Ecossistema e qualidade

- [Espelho Gitee](https://gitee.com/perrylink/dsh-eia-guide-check) (espelho sincronizado; o GitHub é o canónico)
- [Página do plugin no dshfind](https://dshfind.com/plugins/PerryLink/dsh-eia-guide-check) (instalações e ranking)
- [Relatório OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-eia-guide-check) (impulsionado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listado)
- **Canal da loja 1024**: `npm i -g dsh1024` uma vez e depois `dsh1024 plugin --profile <name> add dsh-eia-guide-check` (conta para o ranking de instalações de [deepseek1024.com](https://deepseek1024.com))
- [Base de conhecimento do ecossistema](https://perrylink.github.io/dsh-plugin-guide/) — guia de desenvolvimento de plugins · dados de seleção medidos · critérios de manutenção

## Desenvolvimento

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: suíte partilhada de plugins de tabela + fixtures emparelhados
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # as specs de dependências resolvem-se a partir do registry
pnpm run check:lockfile                             # verificação de deriva do lockfile
pnpm run check:readmes                              # consistência dos README em cinco idiomas
pnpm run check:citations                            # linha de base de citações do pacote de regras
node ../scripts/sync-shared.mjs dsh-eia-guide-check   # atualizar src/shared a partir de ../_shared
pnpm pack                                           # o tarball publicado
```

O plugin é **somente dados**: `src/model.ts` declara a forma da tabela, o kit partilhado fornece o leitor e o motor de verificação, e o pacote de regras declara cada verificação. Execução local do exemplo (requer `pnpm run build` antes para produzir `lib/`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
```

A entrada do exemplo está em `samples/quickstart/input/`, a saída esperada em `samples/quickstart/expected/result.json` e uma captura em `docs/assets/quickstart.png`. As imagens do README são geradas programaticamente por [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) e podem ser reexecutadas sem risco; o diagrama de fluxo de uma só pele e as imagens de demonstração antigas permanecem em `docs/assets/` para ligações externas, enquanto os README só referenciam o novo par claro/escuro.

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `eia`, `guide`

## Família e agradecimentos

Este projeto faz parte da família de plugins do DeepSeek Harness da [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Índice completo da família: [escolher um verificador por material](https://perrylink.github.io/zh/checkers/choose/) e [todos os plugins](https://github.com/PerryLink). Se for útil, **uma estrela ajuda a próxima pessoa a encontrá-lo** — nada fica bloqueado atrás dela.

- [@PerryLink](https://github.com/PerryLink) — criador e mantenedor: o pacote de regras somente de dados (EG-001..EG-007), a ferramenta `eia_guide_check`, a linha de base de citações e a documentação em cinco idiomas.

<details>
<summary>Expandir todos os plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 APOSENTADO (repo arquivado) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 APOSENTADO (repo arquivado) |

</details>

## Licença

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-eia-guide-check contributors

<p align="center"><sub>Apache-2.0 · Plugin da comunidade, sem afiliação com a DeepSeek.</sub></p>
