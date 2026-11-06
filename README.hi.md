<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-eia-guide-check-hero-en-light.webp" width="100%" alt="dsh-eia-guide-check: बाईं ओर प्लगइन का नाम, दो मूल्य-पंक्तियाँ और यह टिप्पणी है कि यह केवल शीट पढ़ता है और अनुपालन पर निर्णय नहीं देता; दाईं ओर साथ आए नियम-पैक के प्रमाण-स्तर हैं — direct: 0 नियम (पैक में कोई शब्दशः पाठ नहीं; हर excerpt यही बताता है), derived-from-principle: 6 नियम (EG-001, EG-002, EG-004, EG-005, EG-006, EG-007, सीमा warn), institutional-configuration: 1 नियम (EG-003, सीमा info, values: [] के साथ आता है, इसलिए skipped में जाता है); पाद में नमूना रन के issues[] 1 (warn) और skipped[] 1 हैं।">
</picture>

# dsh-eia-guide-check

**EIA दिशानिर्देश-प्रयोज्यता शीट की संदर्भ-योग्यता जाँचें — आपको मिलता है कि कौन-सी पंक्ति, कौन-सा कॉलम और क्या सुधारना है; अंतिम निर्णय समीक्षक का रहता है।**

DeepSeek Harness के लिए एक केवल-डेटा जाँच प्लगइन: यह एक दिशानिर्देश-प्रयोज्यता शीट (परियोजना हेडर और प्रत्येक मूल्यांकित तत्व की एक पंक्ति) पढ़ता है, साथ आने वाले संस्करणबद्ध नियम-पैक (EG-001..EG-007) को लागू करता है, और केवल वे अंतर गिनाता है जिन्हें सामग्री के भीतर इंगित किया जा सकता है — कभी अनुपालन का निर्णय नहीं, कभी दायित्व का निर्धारण नहीं।

[इंस्टॉल](#तीन-चरणों-में-शुरुआत) · [कॉन्फ़िगरेशन](#कॉन्फ़िगरेशन) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#संगतता)
[![npm](https://img.shields.io/npm/v/dsh-eia-guide-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-eia-guide-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-eia-guide-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-eia-guide-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#संगतता)

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

<sub>समुदाय प्लगइन, DeepSeek से आधिकारिक रूप से संबद्ध नहीं। एकमात्र रिपॉज़िटरी: <https://github.com/PerryLink/dsh-eia-guide-check> (Gitee प्रतिबिंब है)।</sub>

## यह क्या है

`dsh-eia-guide-check` पर्यावरण प्रभाव मूल्यांकन की एक दिशानिर्देश-प्रयोज्यता शीट पढ़ता है — परियोजना हेडर और प्रत्येक मूल्यांकित तत्व की एक पंक्ति — और उसी शीट की संदर्भ-योग्यता जाँचता है: क्या हर तत्व अपना लागू दिशानिर्देश बताता है (नाम या क्रमांक, कम से कम एक), क्या दिशानिर्देश क्रमांक प्रकाशित रूप में लिखा है, क्या दिशानिर्देश की स्थिति आपके द्वारा कॉन्फ़िगर की गई शब्दावली से ली गई है, क्या मूल्यांकन विधि या लागू मानक दर्ज है, क्या कोई तत्व दो बार दर्ज नहीं है, क्या हेडर परियोजना और मूल्यांकन दस्तावेज़ का प्रकार घोषित करता है, और क्या मानक-कॉलम में कोई अपरिवर्तित टेम्पलेट प्लेसहोल्डर शेष नहीं है।

यह तय नहीं करता कि पर्यावरण प्रभाव मूल्यांकन अनुपालन में है, मूल्यांकन स्तर सही है, पूर्वानुमान मॉडल लागू है, या निष्कर्ष टिकाऊ हैं।

- **किसके लिए**: EIA तैयार करने वाले और पर्यावरण अधिकारी; कमांड लाइन की ज़रूरत नहीं — सामग्री चैट में दे दें।
- **आप क्या देते हैं**: वह मूल सामग्री जिस पर जाँच चलती है (एक तालिका, रजिस्टर या दस्तावेज़); मूल कभी नहीं बदला जाता। Excel को पहले JSON/YAML में बदला जा सकता है, चैट में भी अगर प्लेटफ़ॉर्म सक्षम हो।
- **आप क्या पाते हैं**: «कौन-सी पंक्ति, कौन-सा कॉलम, क्या कम है, कैसे सुधारें» की सूची; हर वह जाँच जो नहीं चल सकी, `skipped` में कारण के साथ दर्ज होती है।

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-eia-guide-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-eia-guide-check-flow-v5-light.svg" width="100%" alt="dsh-eia-guide-check की संरचना (कॉलम → नियम वायरिंग बोर्ड): एक applicability शीट (JSON/YAML) के 8 कैनोनिकल कॉलम उन 7 नियमों से जुड़े हैं जो उन्हें पढ़ते हैं — guideName और guideCode EG-001 में, guideCode EG-002 में भी, guideStatus EG-003 में, method और standard EG-004 में, standard EG-007 में भी, element EG-005 में, project और reportType EG-006 में; हर नियम पर उसकी गंभीरता-सीमा अंकित है (छह पर warn, एक पर info)। केवल दो निकास हैं: जो मिला वह issues[] में (उदाहरण: पंक्ति 1 में guideName और guideCode खाली), जो नहीं चल सका वह कारण के साथ skipped[] में (EG-003, values अनसेट), और जो नियम चला पर कुछ न मिला वह किसी में नहीं; खाली सूची का अर्थ स्वीकृति नहीं, निर्णय समीक्षक के पास रहता है।">
</picture>

## तीन चरणों में शुरुआत

1. **इंस्टॉल करें** (एक चैनल चुनें):

   ```sh
   # git चैनल (नवीनतम main; git+https://github.com/PerryLink/dsh-eia-guide-check.git के बराबर)
   dsh plugin --profile <name> add github:PerryLink/dsh-eia-guide-check
   # npm चैनल (प्रकाशित संस्करण)
   dsh plugin --profile <name> add dsh-eia-guide-check
   # tarball चैनल: इस रेपो में pnpm pack के बाद
   dsh plugin --profile <name> add ./dsh-eia-guide-check-<version>.tgz
   ```

   npm चैनल पहले से बना `lib/` देता है; git चैनल इंस्टॉल के समय `prepare` स्क्रिप्ट (tsdown) से उसे बनाता है, इसलिए मैन्युअल बिल्ड की ज़रूरत नहीं।

2. **न्यूनतम कॉन्फ़िगरेशन** (डिफ़ॉल्ट ही काम करते हैं; `config` के बिना bundle पंक्ति सभी डिफ़ॉल्ट लेती है, नियम-पैक पथ साथ आए `rules/eia-guide-check.yaml` की ओर इशारा करता है):

   ```yaml
   - insert:
       - id: dsh-eia-guide-check
         name: dsh-eia-guide-check
   ```

3. **जाँचें कि यह माउंट हुआ**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
   ```

   फिर उसे एक शीट दें। साथ आए नमूने का अपेक्षित आउटपुट (`samples/quickstart/expected/result.json`):

   ```json
   {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
   ```

   इस रेपो में इसे दोबारा चला सकते हैं (पहले `pnpm run build` से `lib/` बनाएँ):

   ```sh
   node samples/quickstart/run.mjs --json
   ```

**अनइंस्टॉल**: `dsh plugin --profile <name> remove dsh-eia-guide-check` (या प्रोफ़ाइल पैच से वह पंक्ति हटा दें)।

<details>
<summary>WorkBuddy / Coze में उपयोग करें</summary>

WorkBuddy / Coze में «Professional Document Check Suite» खोजें (पूरा सेट; यह जाँच उसका एक हिस्सा है; उपलब्धता मार्केट के अनुसार) और बिना कमांड लाइन के वही जाँच क्षमता पाएँ।

</details>

<details>
<summary>DSH Desktop मार्केट से इंस्टॉल करें</summary>

सभी PerryLink प्लगइन DSH Desktop के अंतर्निहित मार्केट में देखे जा सकते हैं: **Market → Sources → add source → चिपकाएँ** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ चुनें**। इंस्टॉल अब भी मार्केट की npm पहचान जाँच और आपकी पुष्टि से होता है।

</details>

## मुख्य क्षमताएँ

`dsh-eia-guide-check` `eia_guide_check` उपकरण पंजीकृत करता है: यह एक दिशानिर्देश-प्रयोज्यता शीट पढ़ता है, संस्करणबद्ध नियम-पैक लागू करता है और एक रिपोर्ट लौटाता है।

- **एक डेटा पैक में सात नियम** — नियम-पैक डेटा है, कोड नहीं (`rules/eia-guide-check.yaml`); उसे बदलने से पूरा नियम-समुच्चय बदल जाता है, TypeScript की एक पंक्ति छुए बिना।
- **सामग्री पर केवल पढ़ना** — JSON या YAML स्वीकार करता है और मूल कभी नहीं बदलता; शुद्ध ESM, कोई नेटवर्क अनुरोध नहीं, कोई मॉडल कॉल नहीं।
- **कोई गढ़ा उद्धरण नहीं** — हर नियम में `document` / `number` / `clause` / `excerpt` / `kind` / `source` होते हैं; इस पैक को इस बार किसी भी दिशानिर्देश का शब्दशः पाठ नहीं मिला, इसलिए हर `excerpt` यह स्पष्ट लिखता है और `derived-from-principle` चिह्नित रहता है: विवरण को कभी उद्धरण बनाकर नहीं पेश किया जाता।
- **गंभीरता साक्ष्य के अनुसार** — `derived-from-principle` अधिकतम `warn`, संस्थागत कॉन्फ़िगरेशन (`institutional-configuration`) अधिकतम `info`, और एक परीक्षण इसे सत्यापित करता है।
- **खाली समस्या-सूची का अर्थ «कुछ गलत नहीं» कभी नहीं** — हर वह जाँच जो नहीं चल सकी, `skipped` में कारण के साथ दर्ज होती है; जिस नियम की आवश्यक सूची अनकॉन्फ़िगर है, वह चुपचाप पास होने के बजाय स्वयं को `skipped` में दर्ज करता है।
- **कोई दिशानिर्देश-सूची नहीं** — यह किसी तत्व को «जो दिशानिर्देश उस पर लागू होना चाहिए» से जोड़ नहीं सकता, इसलिए सबसे बड़ी त्रुटि नहीं पकड़ सकता: किसी तत्व के लिए गलत दिशानिर्देश का उपयोग। उसके लिए वर्गीकरण सूची और हर दिशानिर्देश का दायरा देखना पड़ता है।
- **कोई निर्णायक भाषा नहीं** — रिपोर्ट केवल अंतर गिनाती है और अनुपालन, दायित्व या शुद्धता पर कभी निर्णय नहीं देती; शब्दावली-रक्षक इसे लागू करता है और हर रिपोर्ट के साथ अस्वीकरण होता है।

| नियम | जाँच | गंभीरता | आधार प्रकार |
|---|---|---|---|
| `EG-001` | हर तत्व अपना लागू दिशानिर्देश बताता है (नाम या क्रमांक) | warn | principle |
| `EG-002` | दिशानिर्देश क्रमांक प्रकाशित रूप में है | warn | principle |
| `EG-003` | दिशानिर्देश की स्थिति आपकी शब्दावली से आती है (डिफ़ॉल्ट रूप से बंद) | info | local |
| `EG-004` | मूल्यांकन विधि या लागू मानक दर्ज है | warn | principle |
| `EG-005` | तत्व दो बार दर्ज नहीं हैं | warn | principle |
| `EG-006` | शीट परियोजना और दस्तावेज़ प्रकार घोषित करती है | warn | principle |
| `EG-007` | मानक-कॉलम में कोई अपरिवर्तित प्लेसहोल्डर नहीं | warn | principle |

### उदाहरण

ये प्लगइन के वास्तविक प्रवेश-बिंदु हैं; एक बार इंस्टॉल करें और एक को कॉल करें। नीचे दी गई तालिका की पहली पंक्ति विस्तृत केस है, बाकी संक्षिप्त केस हैं।

**विस्तृत उदाहरण** — उपकरण `eia_guide_check`, इनपुट:

```json
{"rows":[{"序号":"1","评价要素":"环境空气","导则名称":"","导则编号代码":"", ...}]}
```

आउटपुट:

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

| आपका सवाल | इसका जवाब |
|---|---|
| किसी तत्व की पंक्ति में दिशानिर्देश का नाम और क्रमांक दोनों खाली हैं। क्या यह दर्ज होता है? | हाँ। जब `guideName` और `guideCode` दोनों खाली हों, `EG-001` उस पंक्ति को दर्ज करता है, क्योंकि पंक्ति को इनमें से कम से कम एक बताना होता है। यह केवल देखता है कि दिशानिर्देश बताया गया है या नहीं, यह नहीं कि वह उस तत्व के लिए सही है: प्लगइन में दिशानिर्देशों की कोई सूची नहीं है और तत्व से दिशानिर्देश की मैपिंग नहीं की जाती। |
| दिशानिर्देश क्रमांक `HJ 2.3` लिखा है, वर्ष के बिना। क्या यह पकड़ में आता है? | हाँ। `EG-002` «HJ संख्या—चार अंकों का वर्ष» रूप की जाँच करता है, जैसे `HJ 2.3—2018`, इसलिए चार अंकों के वर्ष के बिना मान मेल नहीं खाता और पंक्ति-दर-पंक्ति दर्ज होता है। यह केवल रूप देखता है: न यह कि क्रमांक वास्तव में मौजूद है, न यह कि वह वर्तमान में लागू है, और न यह कि वह बगल के नाम से मेल खाता है। खाली `guideCode` सेल यहाँ दर्ज नहीं होता — खाली मान इस रूप-जाँच से बाहर रहते हैं। |
| स्थिति कॉलम में हमारी अपनी शब्दावली का मान भरा है। जाँच क्यों नहीं चली? | क्योंकि `EG-003` की `values` सूची खाली आती है, यानी स्थिति की शब्दावली अभी कॉन्फ़िगर नहीं है: नियम चुपचाप पास होने के बजाय `skipped` में स्वयं को दर्ज करता है और बताता है कि यह शब्दावली संस्था की अपनी है। कॉन्फ़िगर करने के बाद भी यह केवल देखता है कि भरा गया मान सूची में है या नहीं, यह नहीं कि दिशानिर्देश वास्तव में लागू है। |
| मूल्यांकन विधि भरी है, पर मानक-कॉलम में अब भी टेम्पलेट प्लेसहोल्डर बचा है। क्या यह पकड़ में आता है? | `EG-004` केवल इतना चाहता है कि `method` या `standard` में से एक भरा हो, इसलिए विधि भरी होने पर वह पास हो जाता है; यह नहीं आँकता कि विधि लागू है या मानक सही है। शेष प्लेसहोल्डर `EG-007` दर्ज करता है, जो मानक-कॉलम में कॉन्फ़िगर किए गए पहले शब्द को ढूँढता है (कोष्ठक चिह्न, `XXX`, `TBD` आदि)। ये शब्द बदले जा सकते हैं, और पूरी तरह खाली मानक-सेल इन दोनों में से कोई भी नियम दर्ज नहीं करता। |
| एक ही तत्व `地表水` दो बार दर्ज है — एक बार जल गुणवत्ता और एक बार तलछट के लिए। क्या होता है? | `EG-005` दोहराया गया `element` मान दर्ज करता है और बताता है कि वह किस पिछली पंक्ति से मेल खाता है, क्योंकि दोहराव से यह तय नहीं होता कि उस तत्व पर कौन-सा दिशानिर्देश लागू है। यह केवल बिना रिक्त स्थान वाले पाठ की तुलना करता है और परिणाम के लिए मानवीय पुष्टि ज़रूरी है: एक ही तत्व को माध्यम के अनुसार बाँटना सामान्य है, इसलिए पंक्ति हटाने के बजाय तत्व के नाम में उप-मद लिखें। शीट में `element` कॉलम न हो तो नियम चुपचाप पास होने के बजाय बताता है कि वह चल नहीं सका। |
| हेडर में परियोजना का नाम नहीं है और मूल्यांकन दस्तावेज़ का प्रकार भी नहीं लिखा। क्या होता है? | `EG-006` दर्ज करता है कि हेडर में `project` और `reportType` नहीं हैं, क्योंकि दस्तावेज़ का प्रकार (रिपोर्ट, फ़ॉर्म या पंजीकरण शीट) तय करता है कि कौन-सा आवश्यकता-समूह लागू होगा। यह केवल देखता है कि हेडर इन्हें घोषित करता है या नहीं; यह नहीं आँकता कि प्रकार का वर्गीकरण सही है। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| पर्यावरण प्रभाव मूल्यांकन तकनीकी दिशानिर्देश श्रृंखला | हर दिशानिर्देश का वर्तमान संस्करण इस बार सत्यापित नहीं | EG-001, EG-002 |
| संस्थागत EIA गुणवत्ता-प्रबंधन मानदंड (आपकी संस्था द्वारा कॉन्फ़िगर) | कोई एकीकृत मानक नहीं (आधार संस्था की कॉन्फ़िगर की गई स्थिति-शब्दावली है) | EG-003 |
| पर्यावरण प्रभाव मूल्यांकन तकनीकी दिशानिर्देश — सामान्य कार्यक्रम | HJ 2.1 (वर्तमान संस्करण और धारा संख्याएँ इस बार सत्यापित नहीं) | EG-004, EG-005, EG-007 |
| निर्माण परियोजनाओं के पर्यावरण प्रभाव मूल्यांकन के वर्गीकरण प्रबंधन की सूची | वर्तमान संस्करण और धारा संख्याएँ इस बार सत्यापित नहीं | EG-006 |

**सीमा:** यह प्लगइन एक **EIA दिशानिर्देश-प्रयोज्यता शीट** की संदर्भ-योग्यता जाँचता है — कि हर पर्यावरणीय तत्व अपना लागू दिशानिर्देश बताता है, कि क्रमांक प्रकाशित रूप में है, कि स्थिति आपकी शब्दावली से आती है, कि मूल्यांकन विधि या लागू मानक दर्ज है, कि तत्व दोहराए नहीं गए, कि शीट परियोजना और दस्तावेज़ प्रकार घोषित करती है, और कोई प्लेसहोल्डर शेष नहीं है। यह **नहीं** तय करता कि पर्यावरण प्रभाव मूल्यांकन अनुपालन में है, मूल्यांकन स्तर सही है, पूर्वानुमान मॉडल लागू है, या निष्कर्ष टिकाऊ हैं।

> ### ⚠️ रिपोर्ट में उद्धरण पर भरोसा करने से पहले यह पढ़ें
>
> **`excerpt` की स्थिति हर नियम में अलग है, एकसमान नहीं।** कुछ नियम धारा को शब्दशः उद्धृत करते हैं (`kind: direct`), कुछ उद्धृत अनुच्छेदों के सिद्धांत से निकाले गए हैं (`kind: derived-from-principle`, अधिकतम `warn`), और कुछ आपकी संस्था द्वारा कॉन्फ़िगर किए गए सीमा-मानों का उपयोग करते हैं (`kind: institutional-configuration`, अधिकतम `info`)। पैक कभी उद्धरण का पैराफ़्रेज़ नहीं करता: जब पाठ नहीं मिला, तो `excerpt` यह कहता है और तर्क `note` में रहता है; एक परीक्षण सुनिश्चित करता है कि कोई नियम ऐसा उद्धरण होने का दावा न करे जो उसके पास नहीं है। **जिन नियमों पर अब भी «पाठ नहीं मिला» लिखा है, पाठ मिलने पर `excerpt` को वास्तविक धारा से बदलें और `kind` को `direct` करें।**
>
> निष्कर्ष समीक्षक का है: यह प्लगइन केवल वे अंतर गिनाता है जिन्हें सामग्री में इंगित किया जा सकता है और तथ्य या अनुपालन पर निर्णय नहीं देता।

## कॉन्फ़िगरेशन

सभी समायोज्य विकल्प `src/config.ts` में Schemastery `Config` फ़ील्ड हैं (cordis.yml से बदले जा सकते हैं); प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं। id-आधारित ओवरराइड पूरी पंक्ति बदल देता है — ज़रूरी हर कुंजी दोबारा लिखें।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

जानने योग्य नियम-स्तरीय पैरामीटर:

- `EG-002` `pattern` — क्रमांक का रूप, डिफ़ॉल्ट «HJ संख्या (वैकल्पिक दशमलव) — चार अंकों का वर्ष»। अगर आपका रजिस्टर क्रमांक दूसरे ढंग से लिखता है तो इसे बढ़ाएँ।
- `EG-003` `values` — आपकी स्थिति-शब्दावली, जैसे `[प्रचलित, निरसित, प्रतिस्थापित, आंशिक रूप से लागू]`। खाली का अर्थ कोई जाँच नहीं; कोई वर्तमान-संस्करण तालिका अंतर्निहित नहीं है।
- `EG-007` `terms` — खोजे जाने वाले प्लेसहोल्डर शब्द।

प्रोफ़ाइल पैच में ओवरराइड का उदाहरण:

```yaml
- insert:
    - id: dsh-eia-guide-check
      name: dsh-eia-guide-check
      config:
        disabledRules: [EG-003]
        timeoutMs: 180000
```

## सामग्री का प्रारूप

उपकरण JSON या YAML स्वीकार करता है:

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

कॉलम नाम बिना केस-भेद और रिक्त स्थान, अंडरस्कोर व हाइफ़न छोड़कर मिलाए जाते हैं; शीट के अपने कॉलम नाम सुरक्षित रहते हैं, इसलिए निष्कर्ष उसी कॉलम का नाम लेता है जिसे उसने पढ़ा। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय «अनुपस्थित मद» श्रेणी के निष्कर्ष मिलते हैं।

## नियमों के स्रोत

नियम-डेटा `rules/eia-guide-check.yaml` में कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। पैक का हेडर पूरी तरह बताता है कि प्लगइन में दिशानिर्देश-सूची नहीं है, तत्व-से-दिशानिर्देश मैपिंग नहीं की जाती, और हर दिशानिर्देश का वर्तमान संस्करण सत्यापित नहीं किया गया; हर नियम का `note` उससे जुड़ा हिस्सा दोहराता है। लोड-समय रक्षक `document` / `clause` / `excerpt` / `source` चाहता है और सिद्धांत-व्युत्पन्न या स्थानीय-कॉन्फ़िगर जाँच को `error` बनाने से रोकता है। `check:citations` उद्धरणों की जाँच करता है: जो अंश स्वयं को शब्दशः उद्धरण कहता है उसे प्राप्त मूल पाठ तक खोजा जा सकना चाहिए, जबकि «पाठ नहीं मिला» कहने वाले नियम प्लेसहोल्डर गिने जाते हैं; `rules/citations-baseline.json` केवल छोटा हो सकता है। अपने आधार को बढ़ा-चढ़ाकर बताने वाला पैक लोड पर विफल होता है, ठोस दिखने वाली रिपोर्ट बनाने के बजाय।

## FAQ

<details>
<summary>क्या यह बताएगा कि किसी तत्व के लिए गलत दिशानिर्देश इस्तेमाल हुआ?</summary>

नहीं — यह इस प्लगइन की सबसे महत्वपूर्ण सीमा है। इसमें दिशानिर्देश-सूची नहीं है और यह किसी तत्व को उस दिशानिर्देश से नहीं जोड़ता जो उस पर लागू होना चाहिए; दिशानिर्देश कॉलम स्वयं शीट का कथन है, और प्लगइन केवल यह देखता है कि वह लिखा है, क्रमांक का रूप सही है, और स्थिति आपके कॉन्फ़िगर किए मानों में है। HJ 2.2 और HJ 2.3 में से चुनना वर्गीकरण सूची और हर दिशानिर्देश के दायरे से तय होता है; वह निष्कर्ष EIA इंजीनियर का है।

</details>

<details>
<summary>स्थिति कॉलम भरा है, फिर `EG-003` कभी रिपोर्ट क्यों नहीं करता?</summary>

क्योंकि `EG-003` की `values` सूची खाली आती है, यानी स्थिति-शब्दावली कॉन्फ़िगर नहीं है: नियम चुपचाप पास होने के बजाय `skipped` में स्वयं को दर्ज करता है और बताता है कि यह शब्दावली संस्था की अपनी है। `values` सेट करने के बाद भी यह केवल देखता है कि भरा गया मान सूची में है या नहीं, यह नहीं कि दिशानिर्देश वास्तव में लागू है — उसके लिए मंत्रालय की प्रकाशन और निरसन सूचनाओं पर नज़र रखनी पड़ती है, और कोई संस्करण-तालिका अंतर्निहित नहीं है।

</details>

<details>
<summary>क्या खाली `issues` सूची को «कुछ गलत नहीं» माना जा सकता है?</summary>

नहीं। हर वह जाँच जो नहीं चल सकी, `skipped` में कारण के साथ दर्ज होती है (अनकॉन्फ़िगर शब्दावली, अनुपस्थित `element` कॉलम, आदि)। किसी भी निष्कर्ष से पहले `issues` और `skipped` दोनों पढ़ें; `skippedCount` केवल वे नियम गिनता है जो सचमुच नहीं चले, वे नहीं जो बिना अंतर के चले।

</details>

<details>
<summary>मेरी शीट Excel फ़ाइल है। क्या सीधे उपयोग कर सकता हूँ?</summary>

हाँ — पहले इसे JSON या YAML में बदलें; चैट में प्लेटफ़ॉर्म सक्षम हो तो रूपांतरण कर सकता है। उपकरण केवल सामग्री पढ़ता है और मूल कभी नहीं बदलता।

</details>

<details>
<summary>पूरी शीट या पूरा फ़ोल्डर एक बार में संभलेगा?</summary>

उपकरण `native` और `ptc` दोनों मोड में चलता है; बैच कार्य (EIA शीटों का सेट या पूरा फ़ोल्डर) के लिए `ptc` चुनें, जहाँ schema लागत एक ही बार लगती है। जाँचें स्थानीय कॉलम-मिलान हैं, कोई नेटवर्क अनुरोध नहीं, कोई मॉडल कॉल नहीं; `timeoutMs` (डिफ़ॉल्ट 120 सेकंड) सहकारी समय-सीमा बजट है।

</details>

## समस्या निवारण

- **किसी तत्व के लिए गलत दिशानिर्देश नहीं बताया।** यह डिज़ाइन से है: इसमें सूची नहीं है और यह कभी तत्व को दिशानिर्देश से नहीं जोड़ता। वर्गीकरण सूची और हर दिशानिर्देश के दायरे से स्वयं पुष्टि करें।
- **`EG-002` ऐसे क्रमांक को पास कर देता है जो मुझे पता है निरसित है।** जाँच क्रमांक का रूप पढ़ती है, कभी उसकी वैधता या प्रचलन नहीं। संस्करणों पर नज़र रखना अलग काम है।
- **`EG-002` उस क्रमांक पर भी चलता है जो मैंने सही लिखा।** पैटर्न `HJ` उपसर्ग, संख्या और चार अंकों का वर्ष हाइफ़न या डैश से अलग चाहता है। पैटर्न समायोजित करें या सेल ठीक करें।
- **`EG-003` कभी नहीं चलता।** इसकी शब्दावली खाली है; अपने गुणवत्ता तंत्र में प्रयुक्त स्थितियाँ भरें।
- **`EG-005` एक ही तत्व की दो पंक्तियों पर चलता है।** एक ही तत्व को माध्यम के अनुसार मूल्यांकित करना (जैसे सतही जल गुणवत्ता और तलछट) उचित है — पंक्ति हटाने के बजाय तत्व के नाम में उप-मद लिखें।
- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं।** जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है; गलत `main` से लोडर प्रविष्टि चुपचाप छोड़ देता है।
- **`dsh plugin add` असंगत बताकर मना करता है।** peer रेंज `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version dsh-eia-guide-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` में `manifest-peers` विफल दिखता है।** स्थिर जाँचकर्ता 0.2 पंक्ति से पहले के हार्डकोडेड peer रेंज से तुलना करता है; रनटाइम इंस्टॉल के समय peer अनुकूलता लागू करता है, इसलिए घोषित रेंज सही है; यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है।

## संगतता

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों को स्वीकार करने के लिए सत्यापित। `engines.dsh` `>=0.2.1-0 <0.3.0` के रूप में घोषित है और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 \|\| >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` में काम करता है; पूरी मूल्यांकन शीट के लिए `ptc` चुनें |

## पारिस्थितिकी और गुणवत्ता

- [Gitee प्रतिबिंब](https://gitee.com/perrylink/dsh-eia-guide-check) (समन्वित प्रतिबिंब; GitHub मानक है)
- [dshfind प्लगइन पृष्ठ](https://dshfind.com/plugins/PerryLink/dsh-eia-guide-check) (इंस्टॉल और रैंकिंग)
- [OpenSSF Scorecard रिपोर्ट](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-eia-guide-check) ([.github/workflows/scorecard.yml](.github/workflows/scorecard.yml) द्वारा संचालित)
- [DSH Market](https://dsh.market/) (सूचीबद्ध)
- **1024 स्टोर चैनल**: एक बार `npm i -g dsh1024`, फिर `dsh1024 plugin --profile <name> add dsh-eia-guide-check` ([deepseek1024.com](https://deepseek1024.com) की इंस्टॉल रैंकिंग में गिना जाता है)
- [पारिस्थितिकी ज्ञान-आधार](https://perrylink.github.io/dsh-plugin-guide/) — प्लगइन विकास गाइड · मापे गए चयन-आँकड़े · रखरखाव के मानदंड

## विकास

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: साझा टेबल-प्लगइन सूट + युग्मित फ़िक्स्चर
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # निर्भरता spec सभी registry से आते हैं
pnpm run check:lockfile                             # lockfile ड्रिफ्ट जाँच
pnpm run check:readmes                              # पाँच भाषाओं के README की एकरूपता
pnpm run check:citations                            # नियम-पैक उद्धरण आधार-रेखा
node ../scripts/sync-shared.mjs dsh-eia-guide-check   # ../_shared से src/shared ताज़ा करें
pnpm pack                                           # प्रकाशित tarball
```

प्लगइन **केवल-डेटा** है: `src/model.ts` तालिका का आकार घोषित करता है, साझा किट पाठक और जाँच इंजन देता है, और नियम-पैक हर जाँच घोषित करता है। स्थानीय नमूना चलाएँ (पहले `pnpm run build` से `lib/` बनाएँ):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"eia_guide_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
```

नमूना इनपुट `samples/quickstart/input/` में, अपेक्षित आउटपुट `samples/quickstart/expected/result.json` में और स्क्रीनशॉट `docs/assets/quickstart.png` में है। README की छवियाँ [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) से क्रमादेशित रूप से बनती हैं और दोबारा चलाई जा सकती हैं; पुराना एकल-रूप फ़्लो आरेख और डेमो छवियाँ बाहरी लिंक के लिए `docs/assets/` में बनी रहती हैं, जबकि README केवल नए प्रकाश/गहरे जोड़े का संदर्भ देते हैं।

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `eia`, `guide`

## परिवार और आभार

यह परियोजना [PerryLink](https://github.com/PerryLink) द्वारा अनुरक्षित DeepSeek Harness प्लगइन परिवार का सदस्य है (सभी Apache-2.0)। पूरा परिवार सूचकांक: [सामग्री के अनुसार जाँचकर्ता चुनें](https://perrylink.github.io/zh/checkers/choose/) और [सभी प्लगइन](https://github.com/PerryLink)। अगर यह उपयोगी हो, तो **एक स्टार अगले व्यक्ति को इसे खोजने में मदद करता है** — इसके पीछे कुछ भी बंद नहीं है।

- [@PerryLink](https://github.com/PerryLink) — निर्माता और अनुरक्षक: केवल-डेटा नियम-पैक (EG-001..EG-007), `eia_guide_check` उपकरण, उद्धरण आधार-रेखा और पाँच भाषाओं का दस्तावेज़ीकरण।

<details>
<summary>सभी प्लगइन खोलें</summary>

| प्लगइन | स्थिति |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 फ़्रोज़न — रेपो README देखें |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |

</details>

## लाइसेंस

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-eia-guide-check contributors

<p align="center"><sub>Apache-2.0 · समुदाय प्लगइन, DeepSeek से संबद्ध नहीं।</sub></p>
