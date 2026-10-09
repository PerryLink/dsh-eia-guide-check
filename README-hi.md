# dsh-eia-guide-check — पर्यावरण प्रभाव मूल्यांकन दिशानिर्देश प्रयोज्यता शीट की जाँच

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-eia-guide-check` पर्यावरण प्रभाव मूल्यांकन की एक दिशानिर्देश-प्रयोज्यता शीट पढ़ता है — परियोजना हेडर और प्रत्येक मूल्यांकित तत्व की एक पंक्ति — और उसी शीट की संदर्भ-योग्यता जाँचता है: क्या हर तत्व अपना लागू दिशानिर्देश बताता है, क्या दिशानिर्देश क्रमांक प्रकाशित रूप में लिखा है, क्या दिशानिर्देश की स्थिति आपके द्वारा कॉन्फ़िगर की गई शब्दावली से ली गई है, क्या मूल्यांकन विधि या लागू मानक दर्ज है, क्या कोई तत्व दो बार दर्ज नहीं है, क्या हेडर परियोजना और मूल्यांकन दस्तावेज़ का प्रकार घोषित करता है, और क्या मानक-कॉलम में कोई अपरिवर्तित टेम्पलेट प्लेसहोल्डर शेष नहीं है।

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-eia-guide-check: real output over its EG-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-eia-guide-check/main/docs/assets/dsh-eia-guide-check-demo.png)

इस प्लगइन का अपने ही `EG-001` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| किसी तत्व की पंक्ति में दिशानिर्देश का नाम और क्रमांक दोनों खाली हैं। क्या यह दर्ज होता है? | हाँ। जब `guideName` और `guideCode` दोनों खाली हों, `EG-001` उस पंक्ति को दर्ज करता है, क्योंकि पंक्ति को इनमें से कम से कम एक बताना होता है। यह केवल देखता है कि दिशानिर्देश बताया गया है या नहीं, यह नहीं कि वह उस तत्व के लिए सही है: प्लगिन में दिशानिर्देशों की कोई सूची नहीं है और तत्व से दिशानिर्देश की मैपिंग नहीं की जाती। |
| दिशानिर्देश क्रमांक `HJ 2.3` लिखा है, वर्ष के बिना। क्या यह पकड़ में आता है? | हाँ। `EG-002` «HJ संख्या—चार अंकों का वर्ष» रूप की जाँच करता है, जैसे `HJ 2.3—2018`, इसलिए चार अंकों के वर्ष के बिना मान मेल नहीं खाता और पंक्ति-दर-पंक्ति दर्ज होता है। यह केवल रूप देखता है: न यह कि क्रमांक वास्तव में मौजूद है, न यह कि वह वर्तमान में लागू है, और न यह कि वह बगल के नाम से मेल खाता है। खाली `guideCode` सेल यहाँ दर्ज नहीं होता — खाली मान इस रूप-जाँच से बाहर रहते हैं। |
| स्थिति कॉलम में `现行` लिखा है। जाँच क्यों नहीं चली? | क्योंकि `EG-003` की `values` सूची खाली आती है, यानी स्थिति की शब्दावली अभी कॉन्फ़िगर नहीं है: नियम चुपचाप पास होने के बजाय `skipped` में स्वयं को दर्ज करता है और बताता है कि यह शब्दावली संस्था की अपनी है। कॉन्फ़िगर करने के बाद भी यह केवल देखता है कि भरा गया मान सूची में है या नहीं, यह नहीं कि दिशानिर्देश वास्तव में लागू है। |
| मूल्यांकन विधि भरी है, पर मानक-कॉलम में अब भी `【待填】` लिखा है। क्या यह पकड़ में आता है? | `EG-004` केवल इतना चाहता है कि `method` या `standard` में से एक भरा हो, इसलिए विधि भरी होने पर वह पास हो जाता है; यह नहीं आँकता कि विधि लागू है या मानक सही है। शेष प्लेसहोल्डर `EG-007` दर्ज करता है, जो मानक-कॉलम में कॉन्फ़िगर किए गए शब्द खोजता है (`【`, `】`, `XXX`, `待填`, `TBD`, `示例` आदि) और पहला मिला शब्द दर्ज करता है। ये शब्द बदले जा सकते हैं, और पूरी तरह खाली मानक-सेल इन दोनों में से कोई भी नियम दर्ज नहीं करता। |
| एक ही तत्व `地表水` दो बार दर्ज है — एक बार जल गुणवत्ता और एक बार तलछट के लिए। क्या होता है? | `EG-005` दोहराया गया `element` मान दर्ज करता है और बताता है कि वह किस पिछली पंक्ति से मेल खाता है, क्योंकि दोहराव से यह तय नहीं होता कि उस तत्व पर कौन-सा दिशानिर्देश लागू है। यह केवल बिना रिक्त स्थान वाले पाठ की तुलना करता है और परिणाम के लिए मानवीय पुष्टि ज़रूरी है: एक ही तत्व को माध्यम के अनुसार बाँटना सामान्य है, इसलिए पंक्ति हटाने के बजाय तत्व के नाम में उप-मद लिखें। शीट में `element` कॉलम न हो तो नियम चुपचाप पास होने के बजाय बताता है कि वह चल नहीं सका। |
| हेडर में परियोजना का नाम नहीं है और मूल्यांकन दस्तावेज़ का प्रकार भी नहीं लिखा। क्या होता है? | `EG-006` दर्ज करता है कि हेडर में `project` और `reportType` नहीं हैं, क्योंकि दस्तावेज़ का प्रकार (`报告书`／`报告表`／`登记表`) तय करता है कि कौन-सा आवश्यकता-समूह लागू होगा। यह केवल देखता है कि हेडर इन्हें घोषित करता है या नहीं; यह नहीं आँकता कि प्रकार का वर्गीकरण सही है। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-eia-guide-check
dsh --profile <name> --dump-config | grep 'dsh-eia-guide-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/eia-guide-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-eia-guide-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-eia-guide-check contributors.
