
# AI 翻譯流程

模型使用量消耗：GPT-5.4 Mini < GPT-5.6 Luna < GPT-5.6 Terra = GPT-5.4 < GPT-5.6 Sol = GPT-5.5

需將檔名與 header 的 l_english 改成 l_simp_chinese

## Scan → Revie

請只掃描指定資料夾的直屬檔案，不要遞迴掃描任何子資料夾。

```
請掃描：
4021  main_menu/localization/english/advances_l_english.yml
1567  main_menu/localization/english/static_modifiers_l_english.yml
1555  main_menu/localization/english/interfaces_l_english.yml
1232  main_menu/localization/english/modifier_types_l_english.yml
1093  main_menu/localization/english/game_concepts_l_english.yml

先比對 translation_glossary.yml，將尚未收錄的專有名詞、宗教概念、神祇稱號、人物、作品名、制度名與可重複使用術語整理到：

work/glossary_review/review.json 

請不要修改來源檔、不要修改 glossary，也不要翻譯內容。
已有 glossary 的詞不要列入 review。
請保留上下文與 glossary_refs。
```

## Review 初審

```
請對 work/glossary_review/review.json 做 AI 預審。

請以 AI 語意與語法判斷執行預審。
不要依賴固定動詞清單，也不要要求事先列出所有可能的動詞。

scripts/prescreen_glossary_review.py 只作為 JSON、
欄位與資料完整性驗證工具，不作為唯一的語意分類依據。

直接檢查並更新：

work/glossary_review/review.json

一、預審範圍

請檢查所有現有 status: todo 與 status: cont 的項目。

已有 status: skip 的項目不要重新判斷或修改。

只允許：

- 更新既有項目的 status
- 依照專有名詞拆分規則新增 review 項目

不要修改既有項目的：

- term
- translation
- keys
- note
- 上下文
- glossary_refs

二、標記為 skip 的項目

將明顯不是固定遊戲術語、專有名詞、歷史名詞、
人名、地名、制度名或可重複使用術語的項目標記為：

status: skip

請不要直接刪除項目，使用 status: skip 保留審查紀錄。

可標記為 skip 的項目包括：

- 一般單獨動詞
- 一般單獨形容詞
- 一般代名詞、介系詞或功能詞
- 一般 V+N 片語
- 一般 V+介系詞+N 片語
- 一般 N+V 片語
- 一般 N+過去分詞片語
- 一般 N+形容詞化過去分詞片語
- 動詞加 UI 或遊戲對象的片語
- 完整敘事句
- 一次性事件標題
- 一次性成就標題
- 教學文字
- 按鈕操作指示
- 普通敘事或一般描述
- 沒有可重複使用價值的 Title Case 片語
- 只在單一事件或單一成就中使用的一般片語
- 事件結果、通知或狀態描述片語

不要因為普通單字採 Title Case 或大寫開頭，
就將它列為 glossary 候選。

三、動詞片語與結果狀態片語

請根據完整 term、source key 與上下文，
自行判斷片語的語法結構。

不要依賴預先列出的動詞清單。

以下類型的完整片語，
即使是遊戲操作、UI 指示或遊戲機制名稱，
完整片語一律標記為：

status: skip

包括：

- V+N
- V+介系詞+N
- N+V
- N+過去分詞
- N+形容詞化過去分詞
- 動詞加 UI 或遊戲對象
- 事件結果或狀態描述

例如：

- Declare War
- Form Government
- Establish Colony
- Improve Relations
- Rescind the Ban
- Sound Toll Exempted
- Administrative Autonomy Returned
- Province Integrated
- Trade Route Established
- Claim Territory
- Clear Region

完整片語不需要作為 glossary 詞條固定收錄，
交由翻譯 AI 根據完整上下文翻譯。

固定遊戲機制或正式 UI term 的單一 term 可以保留，
但完整 V+N、N+V 或結果狀態片語仍依本節標記為 skip。

四、必須保留的項目

以下類型不要標記為 skip：

- 人名
- 地名
- 國名
- 族群名
- 語言名
- 組織名
- 制度名
- 頭銜與職位
- 歷史事件
- 戰役
- 戰爭
- 條約
- 會議
- 宗教概念
- 神祇與神祇稱號
- 作品名
- 固定遊戲機制的單一 term
- 正式 UI term 的單一 term
- 可重複使用的遊戲術語
- 其他具有明確專有名詞特徵的項目

即使上述項目只出現一次，也必須保留。
不得以出現次數作為排除理由。

五、一次性標題與敘事中的專有名詞

若一次性事件標題、成就標題、
完整敘事句或一般片語中包含專有名詞：

1. 外層完整片語可以標記為 skip。
2. 必須拆出其中的人名、地名、組織名、制度名、
   歷史名詞、宗教概念或作品名。
3. 專有名詞必須獨立保留為 review 項目。
4. 新項目使用 status: todo。
5. translation 必須保持空白。
6. 保留原始 key、上下文與 glossary_refs。

例如：

Saladin's Legacy

應處理為：

- Saladin's Legacy → skip
- Saladin → todo

又例如：

Affirm the Confession of Biljno Polje

應處理為：

- Affirm the Confession of Biljno Polje → skip
- Confession of Biljno Polje → todo
- Biljno Polje → todo

完整詞組與子詞條都不得重複建立。

若拆出的完整專有名詞中還包含更小的獨立人名、
地名或其他專有名詞，可以同時建立完整詞組與獨立子詞條。

六、完整敘事句與普通敘事

以下類型通常標記為 skip：

- Give Me Back My Legions
- What the Lord Giveth
- It's Just Business
- A New Beginning
- A Difficult Decision
- The Situation Changes
- Our Enemies Are Weak

但若其中包含歷史事件、作品名、人物、地名、
制度、組織或宗教概念，必須依第五節拆出並保留專有名詞。

七、按鈕與教學指示

以下類型通常標記為 skip：

- Begin
- Continue
- Open the Country Tab
- Click the Improve Opinion
- Close the Hints Panel
- Read Later
- Skip Lesson
- Tell Me More
- Next
- Repeat

若其中包含正式且可重複使用的 UI term，
只保留該 UI term，不保留整句操作指示。

八、cont 項目規則

預審時也要檢查原本 status: cont 的項目。

若 cont 項目明顯只是：

- 一般動詞片語
- V+N
- V+介系詞+N
- N+V
- N+過去分詞
- N+形容詞化過去分詞
- 按鈕指示
- 事件結果
- 狀態描述
- 普通敘事片語

可以標記為：

status: skip

若 cont 項目可能是固定遊戲機制、
正式 UI term、制度名、歷史名詞或專有名詞，
則保留原本 status: cont。

若無法確定，不要標記為 skip，
保留原本 status: cont。

不要修改 cont 項目的 translation。
後續處理 cont 時，再由 AI 根據上下文判斷應建立 fixed、
contextual，或繼續保留 cont。

九、保留疑義項目

無法確定是否為固定術語、專有名詞、
歷史名詞或可重複使用術語時：

- todo 項目保留 status: todo
- cont 項目保留 status: cont
- 不要填寫或修改 translation
- 不要自行加入 translation_glossary.yml
- 不要修改來源檔
- 不要修改 term、keys、note 或上下文
- 保留既有 glossary_refs

十、檔案限制

- 不要修改 source/english/ 下的來源檔。
- 不要修改 translation_glossary.yml。
- 不要修改任何翻譯檔。
- 不要翻譯或填寫 translation。
- 只允許更新既有項目的 status。
- 依照專有名詞拆分規則，可以新增 review 項目。
- 新增候選必須使用 status: todo。
- 新增候選的 translation 必須保持空白。
- 新增候選必須保留來源 key、上下文與 glossary_refs。
- 不得建立重複的 term。
- 不得刪除 review 項目。

十一、完成後驗證

完成後請執行腳本驗證 JSON 結構與欄位完整性，
並回報：

- 原始項目數
- 標記為 skip 的項目數
- 其中原本 todo 被標記為 skip 的數量
- 其中原本 cont 被標記為 skip 的數量
- 保留 todo 的項目數
- 保留 cont 的項目數
- 新增專有名詞候選數量
- JSON 格式驗證結果
- 是否有重複 term
- source/english/ 是否未被修改
- translation_glossary.yml 是否未被修改
- 翻譯檔是否未被修改
```

## Review 審查

```
請檢查並處理這份 review.json：

work/glossary_review/review.json

一、處理範圍

只處理以下項目：

- status: cont
- status: todo
- status: ai

已有 status: skip 的項目不要重新判斷或修改。

二、cont 處理

處理 cont 時：

1. 先讀取 review 提供的 source key、英文上下文與既有 translation。
2. 只有在 term 可能有多重詞義、普通用法與遊戲術語可能混淆，
   或可能與其他遊戲機制產生不同譯法時，
   才搜尋 source/english/ 下該 term 的其他用法。
3. 搜尋時只讀取命中行及前後短片段，
   不要讀取或輸出完整檔案。

請根據實際語境判斷：

- 所有用法都能使用同一譯名：匯入 fixed。
- 不同語境需要不同譯法：建立 contextual。
- 無法確定：保留 cont，不要匯入 glossary。

不要因為 status: cont 就一律建立 contextual。

完成後請列出所有 cont 的：

- 判定結果
- 譯名
- 匯入 fixed 或 contextual 的理由
- 仍保留 cont 的原因

三、todo 與 ai 處理

- 已填寫且已確認的 todo，匯入 fixed 或 contextual。
- ai 項目只有在使用者已確認 translation 後，才能匯入 glossary。
- 尚未確認的 todo 或 ai 必須保留。
- 不要自行填寫或修改尚未確認項目的 translation。
- 匯入 contextual 時，保留 review note 作為 glossary 註解。

四、review 清理

處理完成後：

- 移除已匯入的 todo。
- 移除已確認並匯入的 ai。
- 移除 skip。
- 保留尚未確認的 todo、ai 與 cont。
- 不要因為更新 glossary_refs 而刪除尚未確認的項目。

五、glossary_refs 更新

所有匯入與移除完成後，使用最新的 translation_glossary.yml，
更新 review.json 中仍保留項目的 glossary_refs。

比對範圍包括：

- fixed
- aliases
- contextual
- reference_terms

規則：

- 保留仍存在且仍相關的既有 glossary_refs。
- 移除已不存在或明確不相關的 refs。
- 每個 review 項目最多保留 8 筆 refs；少於 8 筆時不要強行補足。
- 候選優先順序：
  1. exact match
  2. aliases 或拼寫變體
  3. 最長完整詞組
  4. 同一 lemma 的單複數、時態或分詞變化
  5. 明確的專名派生形式
  6. 具有直接語意關聯的 fixed 或 contextual term
  7. reference_terms
- 比對時應忽略大小寫、重音符號、標點與所有格差異。
- 必須辨識高信心的詞形變化，例如：
  - Garrisons → Garrison
  - Bishoprics → Bishopric
  - Assimilated → Assimilate
- 必須辨識明確的專名派生，例如：
  - Croatia → Croatian
  - Abkhazia → Abkhazian
  - Catalonia → Catalan
  - Venice → Venetian
- 不得只依賴字面包含或共享普通單字；Sea、Cost、Type、Treaty、System 等泛用字不要任意加入。
- 無法高信心確認為同一 lemma、派生詞或直接相關詞條時，不要加入。
- reference_terms 只能作為翻譯參考，不得當作強制固定譯名。
- 不要修改 term、translation、status、keys、note 或上下文。
- 若 glossary_ref 來自 contextual，translation 必須列出該 contextual
  的所有 `senses[].zh`，依原順序以「、」合併在同一字串中。
- contextual 的 `default` 若已包含在 senses 中，不要重複列出。
- contextual glossary_ref 不得留下空的 translation。
- 例如：
  German → "德意志的、德意志人、德意志語"
- aliases glossary_ref 使用該 aliases 群組的 `zh` 翻譯。
- reference_terms 可列出其 suggestions，並以「、」合併；仍只能作為參考。

六、Glossary 排序規則

本次不要重新排序 translation_glossary.yml。

保留 fixed、aliases、contextual、reference_terms 各區目前的條目順序、空行與註解位置。

匯入新條目時，不要移動或重排既有條目。

只有當我明確要求「排序 glossary」或「重新整理 glossary 順序」時，
才執行各區字母排序。

七、檔案限制

- 不要修改 source/english/ 下的來源檔。
- 不要修改任何翻譯檔。
- 只在明確需要時修改 translation_glossary.yml。
- 不要修改尚未確認項目的 translation。
- 不要修改 review 項目的 term、keys、note 或上下文。
```

## 處理 status: ai

```
請處理：
work/glossary_review/review.json

針對所有 status: ai 的項目：
1. 根據來源 key 與上下文提出繁體中文譯名。
2. 將建議填入該項目的 translation。
3. 保持 status: ai 不變。
4. 不要修改 glossary。
5. 不要處理 todo、cont 或 skip。
6. 不要刪除任何 review 項目。
```

## ChatGPT 翻譯

```
# EU5 本地化翻譯規則

本次只以最新上傳的`translation_glossary.yml`為準；舊 glossary 一律忽略。

請依照我既有的 EU5 本地化規則翻譯本批 localization。

處理方式：

* 不要整檔壓縮式翻譯。

【防漏翻／Parser 完整性檢查】

* 在統計 key、判斷缺漏及拆 Batch 之前，必須先建立「完整 source key universe」，不得僅以單一 parser 或 regex 成功匹配到的結果直接視為本檔全部 localization key。
* 主要 localization parser 必須容許任意行首縮排，包括：

  * 無縮排。
  * 任意數量半形空格。
  * Tab。
  * 空格與 Tab 混合。
* 不得因某一 localization 行的縮排、冒號前後空白、引號前後空白或其他格式細節與主要 regex 不完全一致，就直接忽略該行。
* 主要 parser 執行完成後，必須另外掃描「所有未被 parser 匹配的行」。
* 對所有未匹配行，排除：

  * 空白行。
  * 純註解行。
  * localization 語言標頭。
  * 已確認不是 localization entry 的其他合法結構。
* 剩餘未匹配行若具有以下任一特徵，必須列為「疑似 localization key」並進一步檢查，不得直接忽略：

  * 行內存在看似 localization key 的`key:`結構。
  * 冒號後存在雙引號 value。
  * key 名稱符合一般 EU5 localization key 命名形式。
  * 與前後 localization entry 結構高度相似。
  * 僅因縮排、Tab、空白或格式差異而未符合主要 regex。
* 若發現有效 localization key 未被主要 parser 匹配，必須：

  1. 修正 parser 或加入 fallback parser。
  2. 重新統計完整 source key。
  3. 重新建立缺漏 key 清單。
  4. 重新規劃尚未處理的 Batch。
* 在 parser 完整性確認前，不得開始正式翻譯或拆 Batch。

【Source／已翻譯／缺漏 key 集合完整性】

* 拆 Batch 前必須分別建立：

  * `source_keys`：完整英文 source 中的所有 localization key。
  * `translated_keys`：目前目標繁中檔中已存在且有效的 localization key。
  * `missing_keys`：`source_keys`中尚未存在於繁中檔的 key。

* `missing_keys`必須由完整 key 集合直接計算，不得只依既有 Batch 清單、人工紀錄或先前 parser 結果推定。

* 必須驗證：

  `missing_keys = source_keys - translated_keys`

* 並確認：

  `translated_keys ∪ missing_keys == source_keys`

* 必須另外檢查：

  `source_keys - translated_keys - missing_keys`

  結果必須為空集合。

* 若存在任何 source key：

  * 不在`translated_keys`；
  * 也不在`missing_keys`；

  則代表有 key 遭漏抓或漏分類，必須先找出原因，不得開始翻譯。

* 若繁中檔存在 source 中不存在的額外 key，也應另外列出檢查，但不得因此把真正缺漏的 source key 忽略。

* 最初提供「總 key 數／已翻譯 key 數／缺漏 key 數」時，三者必須滿足：

  `已翻譯 key 數 + 缺漏 key 數 = source key 總數`

  若不成立，必須先停止並重新檢查 parser／key 集合。

【Missing key 與 Source 順序】

* 補翻 Batch 必須以`missing_keys`為基準規劃，而不是單純以 source 中兩個 key 之間的所有連續 key 作為待翻譯內容。
* 所有`missing_keys`必須保留其在 source 中的原始順序。
* 若兩個缺漏 key 之間存在已翻譯 key：

  * 這些已翻譯 key 可以作為上下文閱讀；
  * 但不得重新輸出為本批「補翻 key」；
  * 不得重複計入補翻進度。
* 若為了理解完整事件組，需要閱讀前後已翻譯 key，應將其視為上下文，不得因此把它們加入 missing key 數。
* 每個 Batch 的「key 數」必須指實際新增補翻的 missing key 數，不得把僅供上下文閱讀或已翻譯的 source key 算入。
* Batch 起點與終點應以該 Batch 第一個／最後一個實際 missing key 表示。
* 若一個完整語意組中只有部分 key 缺漏，可以閱讀整組內容理解上下文，但最終補翻檔原則上只輸出缺漏 key；除非使用者另有要求，不得覆蓋已存在的翻譯。

【拆批前最終防漏檢查】

* 在正式規劃所有 Batch 前，必須確認：

  * 每一個`missing_key`都恰好被分配到一個 Batch。
  * 不得有任何 missing key 未被 Batch 涵蓋。
  * 不得有同一 missing key 被兩個 Batch 重複涵蓋。

* 必須驗證：

  `所有 Batch key 的聯集 == missing_keys`

* 且：

  `各 Batch key 彼此不得重複`

* 若上述檢查未通過，不得開始翻譯。

* Batch 規劃完成後，所有 Batch 的 key 數總和必須等於`missing_keys`總數。

* 若後續因事件組完整性重新拆分／合併 Batch，必須再次執行上述完整性檢查。

* 請以事件組為單位逐組理解：title/desc/option/tooltip 必須一起看。

* 翻譯前必須先統計本檔 key 數，辨識完整事件組、共同 prefix、`_NAME/_DESC`配對、同一功能區段及其他不可拆分的完整語意單位，並依內容複雜度規劃所有 Batch；若需拆成多個 Batch，首次只提供拆批規劃，不要直接翻譯。

* `50 key`僅作為一般拆批參考，不是固定目標或絕對上限；不得只按 key 數或行數機械式切分。

* 拆批時必須優先保持完整語意單位；同一事件的 title/desc/option/tooltip 不可拆到不同 Batch，成對或高度相關的`_NAME/_DESC`及同一功能區段也應盡量置於同一 Batch。

* 每個 Batch 的大小應依原文總長度、desc/tooltip 篇幅、placeholder/token 密度、glossary 命中複雜度、專名及歷史制度詞彙密度，以及詞條間的語意關聯動態調整。

* 建議規模：

  * 極短且同質的 UI 詞條：50～80 key。
  * 一般短句、簡短 tooltip 或`_NAME/_DESC`配對：35～55 key。
  * 中等長度的機制說明或條件文字：20～40 key。
  * 長 desc、歷史敘事、複雜事件或大量高風險 placeholder：10～25 key，必要時可更少。

* 原則上單一 Batch 不超過80 key；若完整事件組本身超過建議規模，仍不得拆散。

* 處理尚未翻譯的 Batch 前，若發現原規劃明顯過大或過小，可以重新拆分或合併尚未處理的 Batch，並同步更新完整 Batch 清單、key 範圍、總批次數、累計完成、尚未處理及整體進度。

* 若在後續 Batch 處理時發現「目前下一個 source key」與原本 missing Batch 起點不一致，不得直接假設原 Batch 規劃錯誤，也不得把兩者之間所有 source key 全部視為漏翻；必須重新比較`source_keys`、`translated_keys`與`missing_keys`，確認哪些才是真正缺漏 key。

* 無論 Batch 大小如何調整，均不得降低 glossary 掃描、逐句翻譯、token multiset、格式及語意 QA 的完整程度。

* desc 必須逐句保留原意，不可概括、改寫成摘要或省略細節。

* 不得為了中文流暢而改變事件效果、因果關係、主詞、受詞或條件含義。

* 對歷史、宗教、制度、階層、文化及遊戲機制詞，請優先檢查 glossary。

* glossary 中經確認語義適用的固定譯名優先級最高，不得自行替換。

* glossary 命中不代表一定適用；套用前必須判斷詞義、詞性、完整片語及上下文。

* 若 glossary 未定義，請使用既有 EU5 繁中翻譯風格，並保持同批譯名一致。

* 同一英文詞在相同詞義、相同詞性及相同語境中多次出現時，譯名必須一致。

* 若同一英文詞在不同語境中具有不同詞義，可以採用不同譯法，不得為了表面一致而犧牲原意。

* 若遇到不確定的專名，請採用較穩妥的暫定譯法，並在最後列入「需人工確認」。

glossary 使用規則：

* 翻譯前必須先掃描本批原文，列出所有命中的 glossary 詞條。
* 掃描時必須使用 longest match first，完整片語優先於單字。
* longest match first 僅用於決定優先檢查的詞條，不代表命中的詞條一定適用；仍須判斷其實際詞義與語境。
* glossary 中的完整術語、專名，以及明確標示為固定譯名的詞條，只有在當前語境與 glossary 定義相符時，才必須使用指定譯名。
* 不得因字面命中單一英文詞，就忽略其所在片語或句子的完整含義，機械式套用 glossary。
* 完整片語的 glossary 詞條優先於其中包含的單字詞條。
* 若單字具有多種詞義，glossary 中的譯名只適用於與該詞義相符的語境，不得跨詞義強制套用。
* 若 glossary 將詞條標示為參考譯義、候選譯名或非固定詞條，應依上下文選擇適合的譯法，不得把候選譯名整串直接放入譯文。
* 若 glossary 值包含多個候選譯名，例如以「、」「，」或其他方式並列，應將其視為候選譯法，依語境選擇其中最合適者，不得要求整串文字出現在譯文中。
* 若 glossary 詞條僅有字面命中，但在當前句中的詞義與 glossary 定義不同，應標示為「詞義不適用」，不得強制套用，也不得視為漏譯。
* 若同一 glossary 詞條以相同詞義在本批多次出現，所有譯文必須一致。
* 若同一英文詞在不同位置採用不同詞義，允許使用不同中文譯法，但必須在語意 QA 中說明最值得注意的差異。
* 若因中文語序調整，經確認語義適用的固定譯名無法以完全相同的字面形式放入譯文，必須在語意 QA 中列出原因，不可默默改譯。
* glossary 命中詞若位於`$...$`、`[...]`、`@...!`、script key 或 localization key 內部，該 token/key 本身不可翻譯。
* `#...#!`不得整體視為受保護 token。必須區分 formatting tag 的控制語法與 tag 內的玩家可見文字。
* 例如`#italic Kapı Ağası#!`中：

  * `#italic `與結尾`#!`屬於 formatting tag 控制語法，必須原樣保留。
  * `Kapı Ağası`屬於玩家可見文字，必須正常進行 glossary 掃描、翻譯、音譯及專名判定。
* 同理，`#T TEXT#!`、`#Y TEXT#!`、`#G TEXT#!`、`#R TEXT#!`及其他 formatting tag 中的`TEXT`若為玩家可見文字，也必須正常翻譯。
* formatting tag 內若包含`$...$`、`[...]`、`@...!`或其他受保護 token，該 token 本身仍依各自規則保留，但 token 周圍及 tag 內其他可見文字仍須正常翻譯。
* 位於真正受保護 token 或 key 內部的字面命中，不列入「指定譯名必須出現在譯文」的強制檢查；應在 glossary 命中表中標示為「受保護 token/key，不適用」。
* 位於 formatting tag 內的可見文字不得標示為「受保護 token/key，不適用」；其 glossary 命中必須照一般可見正文判斷。
* token 外及 formatting tag 內的可見文字仍須正常判斷 glossary 是否適用。
* 若 glossary 的結構已區分固定詞條、參考詞條或候選詞條，必須遵守 glossary 中的實際分類，不得將所有詞條一律當成固定譯名。
* 只有「語義適用的固定詞條」未套用，或仍有無法解決的「需人工確認」項目時，才不得輸出最終檔案；必須先修正或釐清後重新 QA。

格式規則：

* 保留所有 key、必要縮排、`\n`及`$...$`、`[...]`、`@...!`等受保護 token 的內容與數量。
* `#...#!` formatting tag 必須保留其控制語法、tag 類型、開啟／關閉結構及必要空格，但 tag 內的玩家可見文字必須正常翻譯，不得要求整段`#...#!`與英文原文完全相同。
* token 或 formatting tag 外圍的普通空格依繁體中文排版規則處理，不要求與英文原文完全一致。
* localization entry 的辨識不得依賴固定縮排；無論 key 前有0個空格、任意數量空格、Tab或混合縮排，都必須納入 parser／fallback parser 檢查。
* placeholder/variable/數字 token 與中文單位或中文句子成分之間不要主動加空格。
* formatting tag 控制語法中的必要空格要保留，例如`#G +100#!`、`#italic $TEXT$#!`中的 tag 語法空格。
* formatting tag 內若包含可見外語文字，該文字仍須翻譯；「保留 formatting tag」不等於「保留 tag 內英文／外語原文」。
* 斜線分隔用`/`，不要用`／`，且兩側不要加空格。
* 一般中文標點使用全形；遊戲語法、script key、placeholder 內的標點原樣保留。
* 英文 dash 作為分類或標題分隔時翻成「——」。

formatting tag 內可見文字處理：

* `#italic ...#!`、`#bold ...#!`、`#T ...#!`、`#Y ...#!`、`#G ...#!`、`#R ...#!`及其他同類 formatting tag，不得整體當作不可翻譯 token。
* 必須將 formatting tag 拆分理解為：

  * 開頭格式控制碼，例如`#italic `、`#T `、`#Y `。
  * tag 內玩家可見文字。
  * 結尾控制碼`#!`。
* 只有 formatting tag 控制碼必須原樣保留；tag 內的玩家可見文字屬於 localization 正文，必須正常翻譯。
* 不得因文字位於 formatting tag 內，就保留英文、拉丁文、法文、德文、義大利文、土耳其文或其他外語原文。
* tag 內若出現歷史人物、官職、制度、作品名、地名、民族名、文化名、宗教名或其他專名，必須先依一般規則檢查 glossary；若 glossary 無定義，依繁中慣例翻譯或音譯；若仍無法確定，列為「需人工確認」。
* 若專名依本專案規則本來就應保留原文，才可保留；不得僅因它是專名或位於`#italic ...#!`中就預設不翻。
* formatting tag 內若只有數字、符號或受保護 placeholder/token，則只保留其原有內容，不需額外翻譯。
* formatting tag 內若同時包含受保護 token 與普通文字，只保護 token 本身；普通文字仍須翻譯。
* 翻譯後必須完整保留原 formatting tag 的種類、開頭、結尾及巢狀結構，不得刪除、破壞、錯置或遺失`#!`。

例如：

`#italic Kapı Ağası#!`
→ `#italic [Kapı Ağası的繁中譯名]#!`

不得輸出：

`白宦官總管#italic Kapı Ağası#!`

如果原文中的`Kapı Ağası`本身就是需要翻譯的可見官職名稱，則它位於`#italic ...#!`內並不是保留原文的理由。

`#T Important Offices#!`
→ `#T 重要職位#!`

`#Y Sea#!`
→ `#Y 海域#!`

`#italic $CHARACTER$#!`
→ `$CHARACTER$`本身受保護，只保留 formatting tag 與 placeholder，不翻譯 placeholder 內容。

角色代名詞 placeholder 處理：

* `[...GetHerHis]`、`[...GetHisHer]`等英文所有格代名詞 placeholder，在繁體中文中只會輸出「他/她」，不會自動包含「的」。
* 翻譯時必須依中文句法與實際語境判斷，不可機械式地在所有此類 placeholder 後一律補上「的」，也不可誤以為 placeholder 本身會輸出「他的/她的」。
* 中文需要明確表達所屬關係時，應在 placeholder 後補上「的」，例如：`[target_character.GetHerHis]的忠誠`。placeholder 與「的」之間不得加入空格。
* 中文慣用結構可省略「的」時，應採用自然中文，例如：`in [target_character.GetHerHis] hand`可譯為`在[target_character.GetHerHis]手中`。
* 若經忠實調整語序後不再使用直接所有格結構，可以改用「所……的」等中文結構，例如：`because of [target_character.GetHerHis] actions`可譯為`由於[target_character.GetHerHis]所採取的行動`。
* 無論是否補上「的」，都必須保留原文的人物指涉與所屬關係，不得造成歧義或改變主詞、受詞。
* `[...GetSheHe]`、`[...GetHeShe]`、`[...GetHerHim]`、`[...GetHimHer]`等主格或受格代名詞 placeholder，亦須依中文句法處理，不得將英文格位差異直接套入中文。

GetFlavorRank placeholder 處理：

* `[...GetFlavorRank]`會輸出依國家、政體、文化、政府形式及當前國家等級而定的特色化國家等級或政權稱號。
* 其輸出內容不固定，不得預設其必定為「王國」「共和國」「帝國」或任何特定稱號。
* 應將整個`[...GetFlavorRank]`視為可直接充當主詞、受詞或名詞成分的完整稱號。
* 翻譯時必須保留該 placeholder，不得為了中文流暢而刪除、改寫或以固定國號取代。
* 不可在 placeholder 前後加入可能與實際輸出重複的泛稱，例如「國家」「政權」「我國」等。
* 英文中的`the [...GetFlavorRank]`通常可直接譯為`[...GetFlavorRank]`，不需要額外翻出定冠詞。
* 英文中的`our [...GetFlavorRank]`應依語境處理，可以譯為`我們的[...GetFlavorRank]`、`本[...GetFlavorRank]`，或調整句式；不可固定採用單一形式。
* 若`[...GetFlavorRank]`本身在句中作為動詞的主詞，不得誤加「的」。
* 調整句式時必須確認代入任何合理稱號後，中文仍然自然且不會產生詞義重複。

一般概念 token 的中心名詞處理：

* `[country|e]`、`[location|e]`、`[culture|e]`、`[religion|e]`、`[capital|e]`、`[market|e]`等一般遊戲概念 token，在中文 localization 中通常會直接顯示完整的中文中心名詞，例如`[country|e]`會顯示為「國家」。
* 翻譯時必須將這類 token 視為句中的完整名詞，不得在其前後再次補上與 token 顯示內容相同或功能重複的中文中心名詞。
* 特別是英文`our [country|e]`不得機械翻譯為`我國[country|e]`或`我方[country|e]`，因為實際顯示後會形成「我國國家」「我方國家」等重複或不自然的結構。
* `our [country|e]`原則上譯為`我們的[country|e]`，或依上下文自然重組句子，但必須保留`[country|e]` token。
* 同理，`their [country|e]`可譯為`他們的[country|e]`，`this [country|e]`可譯為`此[country|e]`；不得因中文習慣使用「我國、該國、敵國」等詞，而又在後方保留`[country|e]`造成中心名詞重複。
* 若自然中文通常會以「我國／該國／敵國」直接取代整個名詞片語，但原文含有必須保留的概念 token，應優先調整句式，使 token 能自然充當完整名詞，不得刪除 token。

例如：

`in our [country|e]`
→ `在我們的[country|e]中`／依上下文自然重組

`our [country|e] has...`
→ `我們的[country|e]擁有……`

錯誤：

`我國[country|e]`
`我方[country|e]`
`我們的國家[country|e]`

文化名稱 placeholder 處理：

* `[...GetCulture.GetName]`、`[...GetCulture.GetNameWithNoTooltip]`等 placeholder 通常只輸出文化名稱，不會自動包含表示人物的「人」。
* 當英文以`a/an + [Culture placeholder]`指稱某一文化背景的人時，中文必須補出中心名詞，通常譯為`一名[...GetCulture.GetNameWithNoTooltip]人`。
* 不得只譯成`一名[文化 placeholder]`後直接接動詞，造成中文缺少中心名詞。
* 若原文指的是文化本身，而非屬於該文化的人，則不得補「人」。

語言與方言 placeholder 處理：

* 在本專案目前的繁體中文 localization 設定中，`[...GetCommonLanguage.GetName]`、`[...GetLanguage.GetName]`、`[...GetDialect.GetName]`、`[...GetDialect.GetNameWithNoTooltip]`、`[common_dialect.GetNameWithNoTooltip]`、`[enemy_dialect.GetNameWithNoTooltip]`等語言或方言 placeholder，輸出的名稱本身一律包含「語」，例如「法語」「希臘語」「諾曼語」。
* 應將上述 placeholder 視為已包含完整中心名詞的語言名稱。
* placeholder 後不得再補上「語」「語言」或「方言」，以免產生「法語語言」「諾曼語語言」「諾曼語方言」等重複或不自然的形式。
* 即使英文原文在 placeholder 後另有`language`或`dialect`，中文也不得逐字將其接在 placeholder 後方；應依中文句法省略該中心名詞或重組句子。
* 不得因 placeholder 所指物件在遊戲資料中屬於 dialect，就將其譯成`[...]方言`；實際顯示名稱已依本專案 localization 統一為以「語」結尾。
* `GetNameWithNoTooltip`與`GetName`的差別僅在於是否附帶 tooltip，不影響其顯示名稱已包含「語」的規則。
* 必須完整保留 placeholder，不得將其改寫為固定語言名稱，也不得刪除。
* 調整語序後仍須保留原文是在描述語言、方言、官方用語或語言政策的含義，不得誤譯為文化、民族或國籍。

例如：

`Our use of [enemy_dialect.GetNameWithNoTooltip] predates this dispute.`
→ `我們使用[enemy_dialect.GetNameWithNoTooltip]的歷史，遠早於這場爭端。`

`We should promote official use of our native [common_dialect.GetNameWithNoTooltip] language.`
→ `我們也應推動在官方場合使用本土的[common_dialect.GetNameWithNoTooltip]。`

或：

→ `我們也應推動本土[common_dialect.GetNameWithNoTooltip]的官方使用。`

錯誤：

`[common_dialect.GetNameWithNoTooltip]語`
`[common_dialect.GetNameWithNoTooltip]語言`
`[common_dialect.GetNameWithNoTooltip]方言`

placeholder 與可見文字空格處理：

* localization value 中的普通英文空格不屬於必須逐字保留的遊戲語法；翻譯時應依繁體中文排版判斷是否保留。
* placeholder、variable、scripted localization、數字 token、tooltip token 與中文句子成分之間，若顯示後應組成同一個詞語、名稱、數量或語法成分，必須直接相連，不得保留或新增半形空格。
* 兩個相鄰 token 若共同構成一個完整的可見名稱、詞組或「名稱＋類型」結構，也必須直接相連。
* 不得因原文在兩個 token 之間有普通空格，就機械式保留該空格。
* 只有在兩側顯示內容確實屬於彼此獨立的英文或拉丁文字區塊，或遊戲語法明確需要空格時，才保留空格。
* formatting tag 控制語法內原本必要的空格仍須完整保留，例如`#G +100#!`、`#italic $TEXT$#!`；本規則不得刪除 tag 控制語法中的必要空格。
* formatting tag 內的玩家可見文字仍依一般繁中排版及翻譯規則處理，不得因「保留 tag 內空格」而保留整段外語文字。
* key 前的縮排、YAML 語法空格、`\n`及真正受保護 token 內部的空格仍須原樣保留。

例如：

`$survive_string$ [target_location_2.GetArea.GetName]`
→ `$survive_string$[target_location_2.GetArea.GetName]`

`[ShowModifier('warrior_banners_modifier')] [modifier|e]`
→ `[ShowModifier('warrior_banners_modifier')][modifier|e]`

`[target_character.GetName] years old`
→ `[target_character.GetName]歲`

`#G +100#! [prestige|e]`
→ `#G +100#![prestige|e]`

但不得修改：

`#G +100#!`
→ tag 控制語法中`+100`前的必要空格必須保留。

人名與曲名處理：

* 歷史人物、君主、宗教人物、事件人物：若 glossary 有定義且語義適用，必須套用；若無定義，請依繁中慣例音譯。
* 現代真人、作曲家、演奏者、製作人員 credit：若出現在可見文字中，也請中文化；若音譯不確定，請列入「需人工確認」。
* music_player 中所有可見曲名、版本名、作曲家/演奏者姓名、樂器及曲目介紹都翻成繁體中文。
* 只有 key、`$...$`、`[...]`、`@...!`等真正受保護的遊戲語法 token 保留原樣。
* `#...#!`中的 formatting tag 控制語法保留原樣，但 tag 內的曲名、人名、作品名、官職名或其他玩家可見文字仍必須翻譯，不得整段保留原文。

完成後請做：

1. key 數與 key 順序檢查。

   * 本批輸出的 key 必須與本批實際`missing_keys`完全一致。
   * 不得將僅供上下文閱讀、但原本已翻譯的 source key 計入本批完成數。
   * 本批完成後必須重新計算：

     * 尚未翻譯 key = `source_keys - current_translated_keys`
   * 不得只用「前一批累計 + 本批輸出檔行數」推算進度。

2. 行數檢查。

3. `$...$` token multiset 檢查。

4. `[...]` token multiset 檢查。

5. formatting tag／`@...!`／`\n`檢查。

   * `$...$`、`[...]`、`@...!`等真正受保護 token 可進行完整內容與 multiset 比對。
   * `#...#!`不得將「tag 內玩家可見文字」視為不可變 token 進行完整字串一致性比對。
   * 對`#...#!`應只驗證：

     * formatting tag 類型是否保留。
     * 開啟與關閉數量是否一致。
     * `#!`是否完整。
     * 巢狀結構是否一致。
     * 控制語法是否遭破壞。
   * 例如：

     * 原文：`#italic Kapı Ağası#!`
     * 譯文：`#italic [中文譯名]#!`
     * 此為正確翻譯，不得因 tag 內文字與英文原文不同而判定 token 被修改。

5-1. formatting tag 內可見文字完整翻譯檢查。

* 掃描原文與譯文中的所有`#...#!` formatting tag。
* 對每個 formatting tag，另外抽取其中的玩家可見文字並逐一檢查是否已翻譯。
* 特別檢查：

  * `#italic ...#!`
  * `#bold ...#!`
  * `#T ...#!`
  * `#Y ...#!`
  * `#G ...#!`
  * `#R ...#!`
  * 其他帶有可見文字的 formatting tag。
* 若原文 tag 內包含英文、拉丁文、法文、德文、義大利文、土耳其文或其他外語可見文字，譯文不得因其位於 formatting tag 中而直接原樣保留。
* 若譯文 formatting tag 內仍存在與原文完全相同的外語可見文字，必須逐項判定：

  1. 是否為`$...$`、`[...]`、`@...!`等受保護 token。
  2. 是否為數字、符號、script 語法或其他本來不需翻譯的內容。
  3. 是否為依本專案規則明確應保留原文的專名。
  4. 是否為漏翻。
* 若不屬於前3項，一律視為漏翻並修正。
* 不得以「專名」「外語」「斜體文字」「位於`#italic ...#!`內」作為自動保留原文的理由。
* tag 內的 glossary 固定詞條若語義適用，仍必須套用指定譯名。
* tag 內專名若 glossary 無定義，仍須依一般繁中翻譯／音譯規則處理。
* 若無法可靠判定譯名，列為「需人工確認」，不得默默保留原文後視為完成。

6. 全形斜線檢查。

7. glossary 實際比對檢查：

   * 列出本批原文中命中的 glossary 詞條。
   * 先判斷每個命中詞條在當前上下文中的詞義、詞性及語境，是否與 glossary 定義相符。
   * 區分詞條屬於固定譯名、參考譯義、候選譯名或其他 glossary 類型。
   * 對語義適用的固定詞條，檢查指定譯名是否實際出現在譯文中；若未出現，必須修正。
   * 對候選譯名，檢查譯文是否依語境選用了適當譯法；不得要求整串候選文字出現在譯文中。
   * 對僅有字面命中但實際詞義不同的項目，標示為「詞義不適用」，不得強制套用，也不得列為「未套用」。
   * 對位於真正受保護 token 或 key 內部的命中，標示為「受保護 token/key，不適用」。
   * 位於`#...#!` formatting tag 內的玩家可見文字不得因位於 tag 內而標示為「受保護 token/key，不適用」；必須依正文正常判斷 glossary 適用性。
   * 若因自然中文語序調整而未逐字呈現固定譯名，必須確認核心固定譯名仍已完整保留，並在語意 QA 中說明。
   * 最後輸出「glossary 命中表」，包含以下欄位：

     * 原文詞條
     * 詞條類型
     * 指定譯名或候選譯名
     * 出現 key
     * 語義適用性
     * 譯文中的實際譯法
     * 檢查結果

8. 語意 QA：

   * 列出3～5條最值得人工抽查的 key，並簡述原因。
   * 優先列出具有多義詞、複雜代名詞、歷史制度、專名、因果關係或 glossary 詞義判斷的句子。
   * 若同一英文詞因不同詞義而使用不同譯法，列出最值得注意的例子及原因。
   * 若 glossary 詞條因當前詞義不適用而未套用，列出較容易誤判的重要例子。
   * 若原文存在 formatting tag 包覆專名、官職、制度名、作品名或其他外語文字，應優先抽查其中較高風險的項目，確認沒有因`#italic ...#!`、`#T ...#!`等格式而漏翻。

9. 最終輸出限制：

   * 若任何「語義適用的固定詞條」仍為「未套用」，請不要輸出最終檔案；必須先修正後重新 QA。
   * 若仍有無法判定的專名、詞義或 glossary 適用性，標示為「需人工確認」，並暫不輸出最終檔案。
   * 「詞義不適用」及「受保護 token/key，不適用」不視為錯誤，不應阻止輸出最終檔案。
   * formatting tag 內的可見外語文字若尚未翻譯，且不屬於明確允許保留的內容，視為漏翻；不得輸出最終檔案。

10. 角色代名詞 placeholder 檢查：

* 檢查所有`GetHerHis`、`GetHisHer`等所有格代名詞 placeholder。
* 確認譯文沒有誤以為 placeholder 自帶「的」。
* 確認沒有機械式地對所有 placeholder 一律補上「的」。
* 依上下文檢查所屬關係是否清楚、中文語序是否自然，且人物指涉沒有改變。
* 檢查所有主格及受格代名詞 placeholder 是否依中文句法正確處理。

11. `GetFlavorRank` placeholder 檢查：

* 確認所有`GetFlavorRank` placeholder 的數量、內容及位置皆已保留。
* 確認沒有擅自將其固定翻譯為「王國」「共和國」「帝國」或其他稱號。
* 確認沒有在其前後加入會與代入內容重複的「國家」「政權」「我國」等詞。
* 將可能的稱號代入句中檢查，確認 placeholder 作為主詞、受詞或名詞成分時，中文語法均合理。

12. placeholder/token 邊界空格檢查：

* 掃描 localization value 中所有`$...$`、`[...]`、`@...!`、formatting tag 邊界與相鄰中文或其他 token 之間的半形空格。
* 若相鄰內容共同構成同一個詞語、名稱、數量、修正名稱或語法成分，確認中間沒有多餘空格。
* 特別檢查`$...$ [...]`、`[...] [...]`、`#...#! [...]`等相鄰結構。
* 不得因原文存在普通空格便直接保留。
* 同時確認 formatting tag 控制語法內部的必要空格、key 縮排、YAML 語法及真正受保護 token 內部內容沒有遭到修改。
* 不得因檢查 formatting tag 邊界空格而要求 tag 內玩家可見文字保持英文原樣。
* 同時檢查概念 token 前後是否出現與其實際顯示內容重複的中文中心名詞，例如`我國[country|e]`、`國家[country|e]`、`首都[capital|e]`等；若會形成「我國國家」「國家國家」「首都首都」等重複結構，必須調整語序或所有格表達。

13. 語言與方言 placeholder 檢查：

* 檢查所有`GetCommonLanguage.GetName`、`GetLanguage.GetName`、`GetDialect.GetName`、`GetDialect.GetNameWithNoTooltip`及各類`dialect.GetNameWithNoTooltip` placeholder。
* 確認 placeholder 的內容、數量與拼寫均完整保留。
* 這些 placeholder 的中文輸出本身已包含「語」；確認譯文未在其後另外補上「語」「語言」或「方言」。
* 特別檢查原文中的`[placeholder] language`與`[placeholder] dialect`結構，確認中文已省略重複的中心名詞或自然重組語序。
* 若出現`[...]語`、`[...]語言`或`[...]方言`，應視為錯誤並修正。
* 確認沒有將語言或方言 placeholder 誤解為文化、民族、國籍或人物稱呼。

14. 防漏翻最終 QA：

* 每完成一個 Batch 後，必須重新從目前完整繁中檔或「已完成翻譯 key 集合」計算真正的已翻譯 key，不得只依先前累計數字加總。

* 必須重新計算：

  `remaining_missing_keys = source_keys - current_translated_keys`

* 本批結束後，檢查：

  * 本批預定 missing key 是否全部完成。
  * 是否有本批 key 未寫入。
  * 是否有非 missing key 被誤計為新增翻譯。
  * 是否因 parser／縮排／格式差異產生新的未分類 key。
  * 是否仍有 formatting tag 內玩家可見外語文字因誤判為受保護內容而漏翻。

* 每批完成後，所有：

  `已完成 missing key + 尚未完成 missing key`

  必須恰好等於最初確認的 missing key universe。

* 不得因 Batch 輸出檔包含額外上下文 key，就把那些已翻譯 key 重複計入累計完成數。

* 當宣告「本檔全部 Batch 已完成」之前，必須執行最終 set difference：

  `source_keys - final_translated_keys`

  結果必須為空集合。

* 同時確認：

  `final_translated_keys`涵蓋全部`source_keys`

* 若結果不是空集合，即使 Batch 編號已全部處理完，也不得宣告100%完成。

* 最終完成判定以「source key 是否全部有繁中翻譯」為準，不以 Batch 130、最後一個 Batch 編號或人工累計數為準。

* 在宣告全部完成前，必須再次掃描所有已補翻 value 中的 formatting tag 可見文字；若仍存在無合理保留理由的原文外語片段，必須視為漏翻並修正。

15. 批次進度追蹤：

* 請於最一開始提供進度追蹤。

* 請記錄本檔規劃出的所有 Batch 及其處理狀態。

* 每完成一個 Batch，請在回覆中列出：

  * 本次完成的 Batch
  * 累計已完成的 Batch
  * 尚未處理的 Batch

* 累計 key 進度必須依實際 missing key 集合計算，不得依輸出檔包含的 source key 數直接累加。

* 當本檔所有 Batch 均已完成時，請明確告知「本檔全部 Batch 已完成」。

* 只有在`source_keys - final_translated_keys`為空集合時，才可宣告「本檔全部 Batch 已完成」。

* 若 Batch 有跳號、漏處理或尚未處理，請明確列出缺漏的 Batch，不得只說尚未全部完成。

* 若後續重新拆分或合併尚未處理的 Batch，請同步更新完整 Batch 清單、各 Batch 的 key 範圍、批次總數、累計完成、尚未處理及整體進度；並明確說明哪些舊 Batch 被拆分或合併，不得沿用失效的舊批次總數。

16. Every 的處理規則

* `every`不可機械翻譯為「每個／每一個」。當`every + 複數或集合中的實體`表示範圍內無一例外時，繁中原則上譯為「所有……」或依句型改寫為「……均／都……」，以符合中文習慣。

  * `Every neighboring country` → `所有鄰近國家`
  * `Every rival that we target` → `所有遭我國鎖定的宿敵`／`我們鎖定的所有宿敵`
  * `Every owned location` → `所有我國擁有的地點`
  * `Every estate loses influence` → `所有階層的影響力都會降低`

* 只有在強調逐一、個別分配或週期頻率時，才使用「每……」：

  * `Every character receives...`若效果逐一套用 → `每名角色都會獲得……`
  * `Every month` → `每月`
  * `Every time` → `每次`
  * `Every 5 years` → `每5年`

* 判斷原則：

  * 強調整個集合、全體適用 → 優先使用「所有／全部／均／都」。
  * 強調集合中的各個個體分別受到效果 → 可使用「每名／每個／各……」。
  * 不得僅因英文出現`every`，便固定套用「每個」。

完成後，請只回覆：

進度追蹤：本次 Batch、key 範圍、key 數、累計完成、尚未處理、整體進度，以及是否「本檔全部 Batch 已完成」。
本次產生的下載檔案連結。

不要輸出翻譯內容、QA、glossary 命中表、語意說明或其他補充。

所有 QA 仍須完整執行，只是不顯示在回覆中。

```

## 翻譯複查

支援單檔檢查與遞迴檢查

檔名篩選 regex：
^[abc].*\.yml$

```
請執行翻譯 QA，不要修改任何翻譯檔或 glossary。

來源檔：
source/english/main_menu/localization/english/missions/

輸出檔：
output/traditional_chinese/main_menu/localization/simp_chinese/missions/

請先執行 QA 腳本，再由 AI 審查 contextual_review。

請檢查：

1. source 與 output 的 key 是否一致。
2. placeholder、scripted localization、formatting token、
   icon token 與 escape sequence 是否完整保留。
3. fixed 與 aliases glossary 是否正確套用。
4. glossary 對照採 longest match first，長片語優先於短詞。
5. contextual 詞條是否符合實際語境。
6. 中文與 token 之間是否有多餘空格。
7. 半形括號、header、檔案格式等排版問題。
8. 斜線、連字號與破折號是否符合語境。

9. Output 未翻譯英文檢查：

   只檢查 output 中的人類可讀文字。
   請先移除 protected token，再檢查剩餘文字。

   只要 output 中仍有英文字母組成的可讀單字或片語，
   就列出供人工確認；即使是專有名詞、人名、地名、
   作品名或 glossary 詞條，也不要自動排除。

   以下內容不要列入：
   - placeholder
   - scripted localization
   - formatting token
   - icon token
   - escape sequence
   - code-like key 或遊戲語法
   - protected token 內部文字

   確定漏翻時使用：
   `untranslated_text`

   可能是刻意保留、但無法確定時使用：
   `untranslated_uncertain`

   格式：

   {
     "type": "untranslated_text",
     "key": "...",
     "source": "...",
     "output": "...",
     "text": "...",
     "reason": "output 中仍保留疑似未翻譯英文"
   }

標點規則：

- 斜線一律使用半形 `/`。
- `[A]/[B]` 等 token 連接時，斜線兩側不要有多餘空格。
- `-` 用於一般英文複合詞或原文必要符號。
- `‑` 用於複合人名、地名、年份範圍或避免換行。
- `——` 用於中文標題或分類名稱分隔。
- protected token 內部不得修改。

contextual 審查規則：

- 讀取 source key、英文原文與繁中翻譯。
- 參考 translation_glossary.yml 的 default 與 senses。
- 翻譯正確：不要列出。
- 確定翻譯錯誤：列為 `contextual_mismatch`。
- 無法確定：列為 `contextual_uncertain`。
- 不要自行修改翻譯檔或 glossary。

報告中的 source/output 只保留問題附近的短片段，
不要貼完整 localization value。

- punctuation_review：顯示標點或連接符附近上下文。
- contextual_review：顯示 term 附近英文與繁中片段。
- untranslated_text：顯示未翻譯英文附近上下文。
- untranslated_uncertain：顯示疑似保留英文附近上下文。

contextual_mismatch 格式：

{
  "type": "contextual_mismatch",
  "term": "...",
  "key": "...",
  "english": "...",
  "actual": "...",
  "expected_sense": "...",
  "reason": "..."
}

請將結果寫入：

work/reports/translation_qa.json

只產生報告，不要直接修改翻譯內容。
```

## 翻譯 QA 初審

```
請審核：

work/reports/translation_qa.json

不要修改任何翻譯檔或 translation_glossary.yml。
只修改 QA 報告。

請根據報告中的 key、source、output、term 與 symbol，必要時讀取對應的 source/english 與 output/traditional_chinese 檔案，以及 translation_glossary.yml。

一、contextual_review

請逐項檢查 contextual term：

1. 參考 translation_glossary.yml 中的 default 與 senses。
2. 根據 source key、英文原文與繁中翻譯判斷實際語境。
3. 翻譯正確：從報告移除。
4. 確定使用錯誤：改為 contextual_mismatch。
5. 無法確定：改為 contextual_uncertain。
6. 不要因為 output 包含某個合法譯名，就直接判定正確。
7. 同一句中若使用了錯誤 sense，必須列出 mismatch。
8. 不要自行修改翻譯檔或 glossary。

contextual_mismatch 格式：

{
  "type": "contextual_mismatch",
  "term": "...",
  "key": "...",
  "english": "...",
  "actual": "...",
  "expected_sense": "...",
  "reason": "..."
}

contextual_uncertain 格式：

{
  "type": "contextual_uncertain",
  "term": "...",
  "key": "...",
  "english": "...",
  "actual": "...",
  "possible_senses": ["...", "..."],
  "reason": "..."
}

二、punctuation_review

請逐項審核 punctuation_review：

1. 讀取 key、source、output 與 symbol。
2. 必要時讀取對應檔案中的完整句子或前後文。
3. 判斷標點與連接符是否符合語境。
4. 使用正確：從報告移除。
5. 確定錯誤：改為 punctuation_mismatch。
6. 無法確定：改為 punctuation_uncertain。
7. 不要只因為看到符號就直接判定錯誤。

標點規則：

- 斜線一律使用半形 `/`，不要使用全形 `／`。
- `[A]/[B]` 等 token 連接時，斜線兩側不要有多餘空格。
- 翻譯 output 中所有人類可讀文字的連字號，一律使用不換行連字號 `‑`（U+2011）。
- 不要使用普通連字號 `-`（U+002D）。
- 中文標題或分類名稱的分隔符使用 `——`。
- protected token、placeholder、script key 與遊戲語法內部的符號不得修改。

punctuation_mismatch 格式：

{
  "type": "punctuation_mismatch",
  "key": "...",
  "symbol": "...",
  "source": "...",
  "output": "...",
  "reason": "..."
}

punctuation_uncertain 格式：

{
  "type": "punctuation_uncertain",
  "key": "...",
  "symbol": "...",
  "source": "...",
  "output": "...",
  "reason": "..."
}

三、untranslated_text

請檢查所有 untranslated_text：

1. 確認該英文是否為真正漏翻。
2. 先移除 protected token，再檢查剩餘文字。
3. 以下內容不要判定為漏翻：
   - placeholder
   - scripted localization
   - formatting token
   - icon token
   - escape sequence
   - code-like key 或遊戲語法
   - protected token 內部文字
4. 專有名詞、人名、地名、作品名或術語即使可能刻意保留，也要保留供人工確認。
5. 確定漏翻：保留 type 為 untranslated_text。
6. 可能是刻意保留但無法確定：改為 untranslated_uncertain。
7. 已確認不是問題：從報告移除。

untranslated_uncertain 格式：

{
  "type": "untranslated_uncertain",
  "key": "...",
  "source": "...",
  "output": "...",
  "text": "...",
  "reason": "可能是刻意保留的專有名詞或術語"
}

四、其他 QA 項目

保留以下項目，不要自行刪除或修改：

- token_mismatch
- missing_key
- extra_key
- glossary_mismatch
- style_warning
- format_error
- key_order_warning

只有在確定是誤報時才移除，並保留合理的判定理由。

五、報告格式

- source 與 output 只保留問題附近的短片段。
- 不要貼上完整 localization value。
- 不要重複建立相同的 QA 項目。
- 不要直接保留舊 summary；請依審核後的實際項目重新產生 summary。
- 完成後確認 JSON 格式有效。

六、遞迴與批次處理

請遞迴檢查報告中的所有項目，包括：

- 頂層 issues
- files[].issues
- 其他巢狀 issues 陣列

請以原始報告中的完整項目集合為基準逐項處理，不得因批次切割而遺漏或重複。

請直接執行完整審核，不要只提供處理方案，也不要等待我確認或要求我手動輸入「繼續」。

請自行完成以下流程：

1. 為每個 QA 項目建立穩定識別：
   `type + key + term + symbol`
2. 將項目自動分成適合的批次，建議每批 50～100 筆。
3. 每批逐項讀取必要的 source、output 與 glossary 上下文。
4. 每批完成後，將結果合併回：
   `work/reports/translation_qa.json`
5. 下一批接續處理，不要中途停止。
6. 不得重複處理、遺漏或覆蓋尚未處理的項目。
7. 持續執行，直到所有 contextual_review、punctuation_review
   與 untranslated_text 都完成審核。
8. 最後重新產生 summary。
9. 確認 JSON 格式有效。

批次處理只在內部進行，不需要每批回報。
若項目數量很多，請自行縮小批次，但不要省略或跳過任何項目。

完成後只回報：

- 總批次數
- 各類型處理數量
- 各類型剩餘項目數
- JSON 驗證結果
```

## Glossary 整理

```
請對整份 `translation_glossary.yml` 做完整結構檢查與整理。

不要只檢查最近新增的條目，請檢查整份 glossary。
只修改 `translation_glossary.yml`，不要修改 `source/english/` 下的來源檔或任何翻譯檔。

本次整理只處理 glossary 的結構、語意、冗餘與分類問題。
**不要執行字母排序。**
排序將由另一個獨立 Prompt 處理。

一、Aliases 檢查

請找出真正適合合併為 aliases 的項目，包括：

* 拼寫差異
* 標點差異
* 重音符號差異
* 連字號／空格等純 orthographic variant
* 不同羅馬化／轉寫形式
* 明確的語言變體
* 正式名稱與常用別名
* 完整名稱與縮寫

只有在所有情境都使用同一中文譯名、且確實代表同一概念時，才合併為 aliases。

不要因為中文相同，就合併：

* 不同人物
* 不同地名
* 不同宗教概念
* 不同制度
* 不同遊戲機制
* 不同詞性或語意的 term
* 不同 lemma，只是部分情境剛好使用相同中文
* 派生後形成獨立概念的 term

### 英文 morphology／詞形變化規則

Glossary 的用途是記錄「翻譯決策」，不是建立完整的英文 morphology 詞典。

以下形式若只是一般英文詞形變化，而且沒有產生新的中文翻譯決策，**原則上不要建立 aliases，也不需要保留多個 fixed 條目**：

* 普通名詞單數／複數
* `-s`、`-es`、`-ies` 等複數變化
* 一般可辨識的不規則複數
* 動詞第三人稱
* 過去式
* 過去分詞
* 現在分詞
* 所有格
* 冠詞差異
* 大小寫差異
* 可由基本專名正常推導的規則形容詞
* 可由基本專名正常推導的居民／族群稱呼

例如：

`Bishop / Bishops`

若兩者都只是「主教」，原則上只保留：

`Bishop: "主教"`

`Manufactory / Manufactories`

若兩者都只是「工場」，原則上只保留：

`Manufactory: "工場"`

`Assimilate / Assimilates / Assimilated / Assimilating`

若只是同一動詞的詞形變化，原則上只保留：

`Assimilate: "同化"`

不要為上述純 morphology 建立 alias。

若現有 aliases 群組唯一作用就是保存這類單複數、時態或分詞變化，且不同詞形沒有特殊中文含義，請刪除 morphology alias，只保留合理的 canonical term。

### Canonical term 原則

當多個條目只是同一英文詞的正常詞形變化，而且中文翻譯決策完全相同時，應優先保留一個 canonical term。

原則上：

* 普通名詞優先保留單數。
* 動詞優先保留原形／lemma。
* 地名優先保留基本地名。
* 人名優先保留標準姓名形式。
* 專有名詞優先保留專案中最標準的英文形式。

如果 glossary 目前只有複數或其他非 canonical 詞形，而其基本 lemma 可以高信心確定，可整理為 canonical term。

但若不同詞形具有不同固定中文含義，不得強制合併。

例如：

`Abbasid: "阿拔斯"`

與：

`Abbasids: "阿拔斯王朝"`

若複數形式在本專案中固定表示王朝，而不只是一般複數，則應分開保留。

同理：

`Romanov: "羅曼諾夫"`

`Romanovs: "羅曼諾夫家族"`

若複數固定表示家族，也應保留。

### 專名派生形式

請特別檢查國名、地名、文化名、族群名與其形容詞／居民稱呼。

若基本專名已固定，例如：

`Abkhazia: "阿布哈茲"`

而：

`Abkhazian`

`Abkhazians`

只是可以依英文詞形與上下文正常推導為：

* 阿布哈茲……
* 阿布哈茲人

且沒有特殊固定譯法，則不必另存。

同理：

`Bologna → Bolognese`

`Vijayanagar → Vijayanagari`

若派生形式只是「某地的／某地人」等可由基本專名高信心推導的用法，且沒有獨立特殊譯名，可只保留基本專名。

但以下情況應保留：

* 派生形式使用不同詞幹，無法可靠從基本專名推導。
* 派生形式有專案指定的特殊中文名稱。
* 派生形式固定表示王朝、家族、政治實體或其他新增概念。
* 派生形式本身具有特殊歷史或遊戲含義。

例如：

`Netherlands / Dutch`

不得因為兩者相關就視為普通規則 morphology。

### Aliases 結構檢查

請同時檢查：

* fixed 中是否存在已被 aliases `also` 包含、且中文完全相同的重複條目。
* aliases 是否仍包含不必要的普通 morphology。
* 同一 alias variant 是否同時被多個 aliases 群組收錄。
* alias 與 canonical term 的中文是否矛盾。
* 真正 aliases 群組的結構與註解是否完整。

保留真正 aliases 群組的結構與註解。

二、Contextual 檢查

請檢查 fixed、aliases 與 contextual 中的所有英文 term，找出確實需要不同中文譯法的項目。

請注意以下情況：

* 詞性不同，而且中文確實需要不同翻譯
* 人物、地名、族群或語言用法不同
* 宗教、歷史或文化語境不同
* 遊戲機制與一般敘事語境不同
* 專有名詞與普通單字用法不同
* 同一 term 在不同 key 中具有不同功能或語意
* 派生形式形成新的固定概念，而不是單純英文詞形變化
* 同一字面 term 在不同完整片語中具有不同義項

請先根據 glossary 內容與代表性 source key 判斷。
只有 term 確實可能有多重語境時，才搜尋 `source/english/` 下的其他用法。

搜尋時只讀取命中行及前後短片段，
不要讀取或輸出完整檔案。

### 不得因 morphology 本身建立 contextual

不要因為 term 是：

* 形容詞
* 單數／複數
* 所有格
* 動詞分詞
* 規則派生詞
* 地名的規則形容詞
* 居民稱呼

就一律改成 contextual。

只有當不同形式**確實產生獨立的中文翻譯決策**時，才保留或建立 contextual。

例如：

`Vijayanagari`

若只是 `Vijayanagar` 的形容詞形式，而 `Vijayanagar` 已固定為「毗奢耶那伽羅」，通常不需要建立：

`Vijayanagari → 毗奢耶那伽羅的`

中文中的「的」「人」「軍隊」「文化」等中心名詞應優先依完整句法與上下文自然補足，而不是為所有英文派生形式建立 contextual。

如果完整遊戲術語在所有用法中都指向同一概念，
請保留 fixed。

對每個高信心 contextual 候選，請列出：

* 目前結構
* 建議結構
* default
* 各 sense 與適用條件
* 代表性 source key 或上下文
* 判定理由

三、Reference Terms 檢查

請檢查 fixed、aliases 與 contextual 中是否有普通多義單字，
其正確譯法高度依賴完整句子或片語語境。

若某 term：

* 具有多個一般語意
* 不是穩定的遊戲機制名稱
* 不是正式 UI term
* 不適合在所有句子中套用同一譯名
* 容易因逐字套用造成錯誤翻譯

請將它移至 `reference_terms`。

`reference_terms` 只提供 AI 參考，
不是固定翻譯規則，不能視為強制 glossary。

`reference_terms` 不得用於：

* 強制替換翻譯
* glossary mismatch 判定
* 自動套用固定譯名
* 要求所有上下文使用同一譯名

格式：

```yaml
reference_terms:
  Defense:
    suggestions:
      - "防禦"
      - "防守"
      - "辯護"
      - "保衛"
    note: "依完整片語與上下文判斷，不得機械套用固定譯名"
```

只有在 term 確實是穩定遊戲術語或正式 UI term 時，
才保留在 fixed 或 contextual。

不要只因普通單字存在多個字典義，
就一律移入 reference_terms。

完整片語、contextual term 或其他較長詞組，
優先於其中的單字 reference term。

例如：

`In Defense of the Less Fortunate`

應依完整片語與上下文翻譯為：

* 為弱勢者辯護
* 為弱勢者發聲

不得將 `Defense` 機械翻譯為「防禦」或「防守」。

請務必逐一檢查 fixed、aliases 與 contextual 三個區域，
不要只檢查 fixed。

對 aliases：

* 以整個 aliases 群組為單位判斷。
* 若主要 term 與所有 aliases 都只是普通多義單字，
  且沒有穩定遊戲術語用途，才可整組移至 reference_terms。
* 不得只移動其中一個真正 alias，破壞原 aliases 群組。
* 若 alias 只是普通 morphology，則應依第一節規則清理，而不是整組移入 reference_terms。

對 contextual：

* 若已有明確遊戲機制、UI、宗教、制度或專有名詞語境，
  應保留 contextual。
* 只有在該 contextual 實際上只是普通多義單字，
  沒有穩定專案術語用途時，才移至 reference_terms。
* 若 contextual 唯一作用只是說明普通 morphology，
  應優先依第二節規則清理，而不是移至 reference_terms。
* `Paper` 這類僅代表一般物件或材料的詞，可列為 reference_terms 候選。

檢查完成後，請明確列出：

* 適合移至 reference_terms 的項目
* 不適合移動的項目與理由
* 沒有候選時也要明確回報

四、完整片語優先規則

翻譯或判斷 glossary term 時，請採 longest match first。

* 完整固定詞組優先於其中的單字
* contextual 詞組優先於其中的單字
* reference_terms 只能在沒有更長詞組時提供參考
* 不得因單字存在 fixed 或 reference_terms，
  就破壞完整片語的自然語意

一般敘事句、事件標題、成就標題或動詞片語，
應先判斷完整句子或完整片語的語意，
不要逐字套用單字 glossary。

longest match first 只用於決定優先檢查的 term，
不代表字面命中的 term 一定適用；
仍須判斷實際詞義、詞性與上下文。

五、衝突與一致性檢查

請額外檢查：

* 相同英文 term 是否同時存在於 fixed、aliases、contextual 或 reference_terms
* 同一 term 是否在不同區域具有互相矛盾的中文譯名
* 同一 aliases variant 是否被多個 canonical term 收錄
* fixed 與 aliases 是否存在完全重複項
* 單數與複數是否出現不合理的不同中文譯名
* 同一 lemma 的不同詞形是否因歷史累積而產生不必要的不一致
* canonical term 是否存在較標準的基本形式
* contextual 是否只是 morphology 說明，而沒有真正不同的翻譯決策
* reference_terms 是否誤收正式遊戲術語
* fixed 是否誤收高度多義的一般單字

例如：

`Estate Type: "階層類型"`

`Estate Types: "階級類型"`

若兩者只是單複數，則應列為疑似不一致並依專案既有用語修正，
不得因為英文形式不同就視為兩個合理的固定譯名。

六、排序與版面保護

本次不得重新排序 translation_glossary.yml，也不得因整理工作改變現有條目的相對順序。

- 保留 fixed、aliases、contextual、reference_terms 各區中未修改條目的現有相對順序。
- 不得依英文 term、中文譯名或其他條件重新排列條目。
- 移動條目時，只移動該條目本身，不得順便重排其他條目。
- 移入新區域的條目放在該區域末尾，不得插入排序位置。
- 保留條目原有的註解、空行、縮排、引號格式與 aliases 結構。
- 不得使用 YAML parser 重新序列化整份檔案。
- 不得統一格式、重排空行、改變換行格式或重新格式化未修改區域。
- 若只是刪除條目，只刪除該條目及其專屬註解，不得改動周圍條目。
- 完成後必須回報本次沒有執行 glossary 字母排序。

七、修改與套用規則

檢查後，請直接套用高信心的建議：

* 將確定可合併的真正異名整理為 aliases。
* 刪除純 morphology 的重複 fixed 條目。
* 刪除只用來保存單複數、時態、分詞等普通 morphology 的 aliases。
* 將 canonical term 統一為合理 lemma。
* 將確定需要多重語境的項目改為 contextual。
* 清除只因 morphology 而建立、但沒有獨立翻譯決策的 contextual。
* 將確定不適合固定套用、但仍具參考價值的普通多義 term
  移至 reference_terms。
* 移除已從 fixed 或 aliases 移出的重複條目。
* 保留所有有效註解與真正 aliases 群組結構。

### 單複數與詞形譯名不一致

如果同一 lemma 的單複數、時態、分詞或其他一般詞形變化，實際上指向同一概念，
但目前中文譯名不一致，必須列為「詞形譯名不一致」並提出：

* 所有相關 term。
* 目前中文譯名。
* 建議統一使用的中文譯名。
* 判定為同一概念的代表性 source key 或上下文。
* 判定理由。

例如：

`Estate Type: "階層類型"`

`Estate Types: "階級類型"`

如果兩者只是單複數變化，應統一為同一中文譯名；若高信心確認沒有語意差異，直接套用修正。
如果複數形式在專案中代表不同制度、群體或固定概念，則不得強制統一，應保留並回報理由。

不要因為中文譯名相同就合併不同概念，也不要因為英文詞形不同就假設它們必然是不同概念。

不要修改有疑義或需要人工確認的項目。

不要修改：

* `source/english/` 下的來源檔
* 任何翻譯檔
* 任何與 glossary 整理無關的檔案

只修改 `translation_glossary.yml`。

本次不要重新排序 glossary。

八、修改前回報

在修改前，先列出「預計修改項目」，
包含：

* term
* 目前結構
* 建議結構
* 修改理由

對大量性質完全相同的 morphology 清理，
可以按類型分組列出：

* 清理類型
* 預計數量
* 代表例
* 判定理由

不需要為數百個完全相同的單複數清理逐條寫長篇說明。

列出後直接執行高信心修改，
不要等待額外確認。

九、驗證

修改完成後：

1. 執行 glossary 結構檢查。
2. 檢查 duplicate keys。
3. 檢查 fixed、aliases、contextual、reference_terms 是否有跨區重複或衝突。
4. 檢查 aliases 結構是否完整。
5. 檢查 aliases 是否仍包含不必要的普通 morphology。
6. 檢查 canonical term 是否合理。
7. 檢查 contextual 是否真正包含不同翻譯決策，而不只是詞形說明。
8. 檢查 reference_terms 是否未被當作固定翻譯套用。
9. 檢查完整片語是否優先於其中的單字 term。
10. 檢查 reference_terms 是否沒有誤收固定遊戲術語。
11. 檢查 fixed 是否仍有明顯的單複數／動詞詞形冗餘。
12. 檢查專名派生形式是否只保留真正有獨立翻譯價值的項目。
13. 檢查註解是否完整保留。
14. 回報所有未處理的疑義項目。
15. 回報實際修改的項目與理由。
16. 確認 `source/english/` 下的來源檔未被修改。
17. 確認任何翻譯檔未被修改。
18. 確認本次沒有執行 glossary 字母排序。

```

## 人名翻譯

```
# EU5 人物姓名／專名本地化翻譯規則

本次只以**本對話中最新上傳的 `translation_glossary`**為準；舊 glossary 一律忽略。

本檔主要為 EU5 的人物姓名、姓氏、家族名、綽號、稱號、姓名構件及姓名組裝規則。

請依照以下規則翻譯為**台灣繁體中文**。

不得把本檔視為一般短字串進行機械音譯，也不得假定每一個姓名 value 都代表某一位特定歷史人物。

翻譯核心優先順序為：

1. localization entry 的實際功能與指涉。
2. 台灣繁體中文已有的通行譯名。
3. glossary 中語義適用的固定譯名。
4. 人物或姓名所屬的語言、文化與歷史時代。
5. 原始語言的正確姓名形式與實際發音。
6. 中文姓名書寫及組裝慣例。
7. 同文化、同家族、同姓名系列的一致性。
8. 最終在遊戲中實際組裝出的姓名是否自然。

不得只依英文字面、英文發音或 localization key 機械翻譯。

---

# 一、Parser 完整性與 source key universe

在統計 key、判斷內容及拆 Batch 之前，必須先建立完整的 `source key universe`。

不得僅以單一 parser 或 regex 成功匹配到的結果，直接視為本檔全部 localization entries。

主要 localization parser 必須容許：

* 無縮排。
* 任意數量半形空格。
* Tab。
* 空格與 Tab 混合。
* 冒號前後不同空白形式。
* 引號前後不同空白形式。

主要 parser 執行後，必須另外掃描所有未匹配行。

排除：

* 空白行。
* 純註解行。
* localization 語言標頭。
* 已確認不是 localization entry 的合法結構。

剩餘未匹配行若具有下列任一特徵，必須列為疑似 localization entry 並再次檢查：

* 存在類似 `key:` 的結構。
* 冒號後存在雙引號 value。
* key 符合 EU5 localization key 命名形式。
* 與前後 localization entry 結構高度相似。
* 只是因縮排、Tab、空白或格式差異而未被主要 parser 匹配。

若發現有效 localization entry 未被 parser 匹配，必須：

1. 修正 parser 或加入 fallback parser。
2. 重新建立完整 `source_keys`。
3. 重新統計 key 數。
4. 重新規劃尚未處理的 Batch。

在 Parser 完整性確認前，不得開始正式翻譯。

拆 Batch 完成後必須驗證：

`所有 Batch 的 key 聯集 == source_keys`

並確認：

`Batch 之間的重複 key 數 == 0`

任何 source key 都不得：

* 沒有被分配至 Batch。
* 同時被分配至兩個以上 Batch。
* 因 parser 格式問題而遭到遺漏。

---

# 二、本檔內容分類

翻譯前不得把所有 entry 一律視為「歷史人物姓名」。

必須依 key、value、section comment、前後 entries 及功能，先區分至少以下類型：

* 姓名排列與組裝格式。
* 姓名連接符／conjoiner。
* given name／名字。
* surname／姓氏。
* family name／家族名。
* dynasty／王朝名稱。
* patronymic／父名。
* matronymic／母名。
* 父名或母名 prefix/suffix。
* 後裔關係 prefix/suffix。
* 地名來源 prefix/suffix。
* 姓名粒子。
* 綽號。
* 尊號。
* 稱號。
* 君主號。
* 軍階。
* 頭銜。
* 敬稱。
* 宗教稱號。
* 可明確辨識的特定歷史人物。
* 一般姓名庫中的非特定真人姓名。
* 其他非姓名內容。

**只有能夠可靠確認指向某一特定真人的 entry，才按照「特定歷史人物」規則處理。**

例如單獨：

* Alexander
* John
* Adebayo
* Andersson
* Gwenllian

不得自行假定為某一位同名歷史人物。

---

# 三、Batch 規則

本檔若超過 800 key，不得直接開始翻譯。

第一次處理本檔時，先提供：

* 本檔總 key 數。
* 本檔主要姓名與結構類型。
* 主要文化／語言區塊。
* 完整 Batch 規劃。
* 每個 Batch 的 key 範圍。
* 每個 Batch 的預估類型。
* 每個 Batch 的處理狀態。

拆 Batch 時應優先依：

* section comment。
* 語言。
* 文化圈。
* 地理區域。
* 王朝。
* 家族。
* 同系列姓名。
* 姓名結構功能。

不得只按照固定行數或固定 key 數硬切。

同一：

* 文化圈。
* 語言區塊。
* 王朝。
* 家族。
* 姓氏系列。
* 父名系統。
* 姓名 prefix/suffix 系統。
* 姓名組裝系統。

應盡量放在同一 Batch。

## 建議 Batch 規模

800 key 是上限參考，不是每個 Batch 的目標。

高度同質、語言文化明確的一般 given name/surname：

**約 500～800 key**

同一文化圈但姓名來源、語言或拼寫較複雜：

**約 300～600 key**

大量冷門人物、歷史人物或需要外部查證：

**約 150～350 key**

姓名格式、頭銜、稱謂、prefix/suffix、父名等結構型內容：

**依完整功能群組拆分，不以 key 數為主要依據。**

不得為了接近 800 key，而合併彼此無關的語言或文化區塊。

---

# 四、翻譯前分析

每個 Batch 正式翻譯前必須先：

1. 確認本 Batch 的完整 key 範圍。
2. 判斷主要 entry 類型。
3. 判斷主要語言與文化群。
4. 讀取 section comment 及前後相鄰 entries。
5. 掃描本 Batch 所有 glossary 命中。
6. 找出可明確辨識的特定歷史人物。
7. 找出需要外部查證的冷門名字。
8. 找出同源姓名。
9. 找出姓氏系列。
10. 找出父名／母名系列。
11. 找出 prefix/suffix 及姓名粒子。
12. 找出可能影響姓名組裝的結構 key。
13. 找出同名但不同語言／文化的姓名。
14. 找出 glossary 可能發生跨文化誤套的名字。

不必在回覆中逐一列出所有普通姓名的分析，但必須在內部完成上述檢查。

---

# 五、文化區塊與原語判定

對一般 given name、surname 或姓名構件，不得只看單獨一個 value 判定其語言。

必須綜合參考：

* 所在 section comment。
* 前後相鄰 entries。
* 同一 Batch 的其他姓名。
* 姓名粒子。
* 變音符號。
* 拼寫規則。
* 父名／母名形式。
* 同系列姓氏。
* 歷史地理範圍。
* 文化或語言背景。

如果一整段可以可靠判定為：

* 威爾斯語。
* 愛爾蘭語。
* 德語。
* 法語。
* 阿拉伯語。
* 波斯語。
* 波蘭語。
* 約魯巴語。
* 阿坎語。
* 梵語。
* 日語。
* 朝鮮語。
* 蒙古語。
* 其他語言。

則應依該語言的實際發音與姓名慣例處理整組名稱。

不得把所有羅馬字姓名一律按英文發音翻譯。

---

# 六、glossary 使用規則

翻譯前必須掃描本 Batch 原文中的所有 glossary 命中。

使用：

**longest match first**

優先順序：

1. 完整人物姓名。
2. 完整姓氏／家族名。
3. 完整名字。
4. 完整稱號。
5. 完整片語。
6. 子詞或單字。

longest match first 只代表優先檢查，不代表必須機械套用。

套用前仍須確認：

* 是否為同一人物。
* 是否為同一姓名。
* 是否為同一語言形式。
* 是否為同一文化背景。
* 詞性。
* 歷史時代。
* 實際指涉。
* entry 類型。
* 是否位於受保護 key/token 內。

只有語義確實適用的固定 glossary 詞條才必須套用。

---

# 七、人名 glossary 特別規則

對人物姓名不得單純按照字串命中機械套用 glossary。

人名 glossary 優先順序：

1. 完整人物姓名的固定 glossary 譯名。
2. 完整 value 的固定 glossary 譯名。
3. 經確認為同一語言、同一姓名形式的 given name/surname 固定詞條。
4. 姓名內部部分字串命中。

例如：

若 glossary 有：

`Alexander → 亞歷山大`

不代表所有包含 `Alexander` 的完整姓名都可不經判斷直接套用。

必須確認：

* 是否真的是 Alexander 這個姓名形式。
* 是否屬於相同語言文化。
* 是否已有該完整人物的台灣通行譯名。
* 是否為君主、宗教人物或其他具有特殊中文慣例的人物。

同源但不同語言形式不得強制統一，例如：

* Charles
* Karl
* Carlo
* Carlos
* Karol

即使具有共同語源，也必須依各自語言與人物慣例處理。

對 glossary 中只有單獨 given name 或 surname 的詞條，必須特別防止跨文化誤套。

---

# 八、專名查證與搜尋原則

不需要對每一個已有穩定譯法的常見姓名逐項上網搜尋。

但以下情況應優先查證：

* 冷門歷史人物。
* 冷門君主。
* 宗教人物。
* 中古家族。
* 王朝。
* 少見姓氏。
* 少見民族姓名。
* 非英語來源且發音不明。
* 同名但可能屬不同語言。
* 姓名拼寫疑似英語化或拉丁化。
* 模型無法高信心判定原語。
* 台灣與中國大陸可能有不同音譯。
* glossary 與一般資料衝突。
* 音譯存在多種合理方案。
* 姓名可能具有可恢復的漢字形式。
* 姓名可能是歷史人物固定譯名而非普通音譯。

不得因搜尋成本高而直接猜測冷門姓名。

---

# 九、資料來源優先順序

人物及姓名查證時依以下順序判斷。

## 第一優先：台灣繁體中文通行譯名

優先參考：

* 台灣學術出版物。
* 台灣歷史研究。
* 台灣教育資料。
* 台灣政府或文化機構資料。
* 台灣出版品。
* 台灣媒體穩定慣例。
* 經人工維護且有可信來源的繁體中文百科資料。

若已有穩定台灣通行譯名，原則上直接採用。

## 第二優先：其他繁體中文資料

例如：

* 香港資料。
* 澳門資料。
* 其他可靠繁體中文出版或研究資料。

仍須確認是否符合台灣用字及音譯習慣。

## 第三優先：原語與外文權威資料

用於確認：

* 人物實際身分。
* 原始姓名。
* 原始拼寫。
* 原始語言。
* 正確發音。
* 歷史時代。
* 姓名構造。
* 姓名粒子的功能。

## 第四優先：簡體中文資料

簡體中文資料僅供：

* 辨識人物。
* 確認原語。
* 確認音節。
* 尋找歷史資料。
* 了解中國大陸現有譯法。

不得直接把簡體譯名簡轉繁後視為台灣標準譯名。

最終仍須重新判斷：

* 台灣音譯用字。
* 人名慣例。
* 歷史人物慣例。
* 宗教人物慣例。
* 君主名稱。
* 姓氏及家族名稱。

---

# 十、一般音譯原則

若沒有可確認的台灣繁體中文通行譯名：

1. 先確認原始語言。
2. 確認姓名的實際發音。
3. 再依台灣繁體中文音譯習慣翻譯。

不得只依英文拼寫或英文發音翻譯非英語姓名。

可能涉及的語言包括但不限於：

* 拉丁文。
* 古希臘文。
* 現代希臘文。
* 法文。
* 德文。
* 義大利文。
* 西班牙文。
* 葡萄牙文。
* 荷蘭文。
* 英文。
* 古諾斯語。
* 愛爾蘭語。
* 威爾斯語。
* 蘇格蘭蓋爾語。
* 波蘭文。
* 捷克文。
* 匈牙利文。
* 羅馬尼亞文。
* 南斯拉夫語言。
* 古教會斯拉夫文。
* 俄文。
* 阿拉伯文。
* 波斯文。
* 鄂圖曼土耳其文。
* 現代土耳其文。
* 希伯來文。
* 亞美尼亞文。
* 喬治亞文。
* 梵文。
* 印度各語言。
* 漢語。
* 日語。
* 朝鮮語。
* 蒙古語。
* 滿語。
* 東南亞各語言。
* 非洲各語言。
* 美洲原住民族語言。
* 大洋洲各語言。

如果某一姓名具有既定意譯或傳統中文名稱，優先使用既有名稱，不必強制音譯。

---

# 十一、姓名組裝與中文書寫規則

本檔包含會由遊戲動態組裝完整姓名的 localization。

因此**最終目標不是保留英文姓名的空格格式，而是讓遊戲實際顯示出的完整姓名符合台灣繁體中文姓名書寫習慣。**

必須特別辨識：

* `NAME`
* `LASTNAME`
* `PREFIX`
* `SUFFIX`
* `NUMBER`
* `NICKNAME`
* patronymic
* matronymic
* descendant marker
* location prefix
* location suffix
* name order
* conjoiner
* 其他姓名組裝 key

## 11.1 最終組裝結果優先

對姓名格式類 key，不得因原文使用空格，就認為中文也必須保留相同空格。

必須以**完整姓名最終呈現**判斷。

例如西方原文：

`Louis de Bourbon`

翻成中文時，不應只是：

`路易 德 波旁`

而應依適用的中文姓名慣例組裝，例如使用：

`路易·德·波旁`

或既有繁中慣例中的固定形式。

## 11.2 中間點「·」

對以音譯方式呈現的西方及其他多段外國姓名：

**原則上使用半形無空格的中文姓名間隔號 `·` 分隔主要姓名構件。**

例如一般概念上：

`Jean Baptiste Colbert`

可組裝為：

`讓·巴蒂斯特·柯爾貝`

而不是：

`讓 巴蒂斯特 柯爾貝`

`·` 兩側不得加空格。

但不得把 `·` 機械加入每一個單獨的 given name/surname value。

**優先在姓名組裝規則、name order、conjoiner 或其他結構層級處理。**

原因是單獨姓名 value 可能：

* 獨立使用。
* 作為姓氏。
* 作為名字。
* 接 prefix。
* 接 suffix。
* 接君主序數。
* 用於東亞姓名。
* 用於父名系統。
* 已經內含連字號或其他構詞結構。

因此：

**不得單純把所有 `$NAME$ $LASTNAME$` 機械替換成 `$NAME$·$LASTNAME$`，必須先確認該 name order 適用的文化及最終組裝結果。**

## 11.3 不同文化不得共用單一姓名格式

姓名組裝必須依文化處理。

### 西歐及多數歐洲音譯姓名

一般情況：

`名字·姓氏`

多個 given name：

`名字·中間名·姓氏`

但若已有台灣固定譯法，以固定譯法為優先。

### 漢字文化圈

中國、日本、朝鮮等以漢字姓名直接呈現時：

**不使用 `·` 分隔姓與名。**

例如：

`明智光秀`

不得改成：

`明智·光秀`

中國姓名同理。

### 君主姓名與序數

不得在姓名與君主序數之間機械加入 `·`。

例如中文應依慣例形成：

`路易十四世`

而不是：

`路易·十四世`

若 `$NUMBER$` 是獨立組件，必須檢查其在中文 name order 中應放置的位置及連接方式。

### 父名／母名

俄羅斯、斯拉夫、北歐、阿拉伯等父名系統，必須依該文化的中文姓名慣例決定：

* 是否使用 `·`。
* 是否與名字合併。
* 是否作為姓氏的一部分。
* 是否需要音譯父名標記。

不得把所有 patronymic 一律套成同一格式。

### `de`、`von`、`van`、`di`、`della` 等姓名粒子

不得：

* 一律刪除。
* 一律意譯。
* 一律以相同方式音譯。
* 一律自行和姓氏黏合。

應依：

* 原語。
* 人物固定中文譯名。
* 台灣姓名音譯慣例。
* 遊戲的動態姓名結構。

決定實際譯法。

如果姓名粒子在中文慣例中被視為獨立音譯構件，可依完整姓名格式使用 `·` 分隔。

若已有固定中文姓名形式，則使用固定形式。

### `al-`、`ibn`、`bin`、`bint` 等

阿拉伯及伊斯蘭姓名構件必須依阿拉伯姓名的實際功能及台灣常用翻譯慣例處理。

不得因其原文以空格分開，就套用一般西歐姓名規則。

也不得因含有連字號就任意拆分或合併。

### `Mac`、`Mc`、`Ó`、`ap` 等

應依其語言中的姓名構造及實際發音處理。

不得把原本屬於姓氏構詞的一部分誤當成獨立中間名。

## 11.4 空格

一般完整中文姓名中：

* 中文字與中文字之間不保留英文姓名空格。
* 使用 `·` 時兩側不加空格。
* 漢字姓名姓與名之間不加空格。

但是：

如果某 localization value 本身是用來控制遊戲組裝的 prefix/suffix，原始前導或尾隨空格可能具有程式功能。

因此在修改前必須先確認：

* 空格是否純粹是英文排版。
* 還是遊戲姓名組裝必要的結構字元。

如果可以藉由中文 name order/conjoiner 重建正確格式，應以中文組裝結果為優先。

不得在不了解引擎組裝結果的情況下直接刪除所有 prefix/suffix 的前導或尾隨空格。

## 11.5 連字號

姓名本身原有的連字號不得機械改成 `·`。

必須判斷它是：

* 姓名本身固定拼寫的一部分。
* 複合名字。
* 阿拉伯定冠詞結構。
* 羅馬化標記。
* 單純英文排版。

再決定中文呈現方式。

## 11.6 綽號

`NICKNAME` 必須先確認遊戲是否已經在外層加入：

* 引號。
* 括號。
* 空格。
* 其他格式。

不得在 nickname value 和 name order 兩邊重複加入標點。

若需要中文化綽號格式，應以最終完整姓名呈現自然為準。

## 11.7 頭銜

頭銜與姓名的關係不得套用 `·`。

例如：

`King Louis`

若需要組裝中文，應依中文語序形成相應結構，而不是：

`國王·路易`

頭銜、軍階、宗教稱號與姓名的組裝應與一般姓名 component 分開判斷。

---

# 十二、漢字文化圈姓名

對中國、日本、朝鮮、琉球、越南等歷史人物或家族：

若可以可靠確認原有漢字姓名，應優先使用歷史上實際使用的漢字形式，而不是再次從羅馬字音譯。

## 中國人物

使用繁體漢字姓名。

不得把拼音重新音譯成中文字。

## 日本人物

可以可靠確認漢字時，使用其原漢字姓名。

例如：

`Akechi Mitsuhide`

應使用：

`明智光秀`

而不是依羅馬字音譯。

## 朝鮮歷史人物

若人物具有穩定且可確認的漢字姓名，優先使用漢字姓名。

但若原文實際表示的是朝鮮語名稱、稱號或非漢字姓名，則依實際內容判斷。

## 琉球人物

優先依可靠歷史資料中的漢字姓名及台灣繁中慣例。

## 越南人物

若存在穩定的繁中漢字姓名，可使用既有漢字形式。

若無可靠依據，不得只依羅馬字自行反推漢字。

**不得猜測漢字。**

---

# 十三、特定歷史人物

如果 entry 可以明確確認指向某位歷史人物：

1. 優先查找台灣繁中通行譯名。
2. 查找其他繁中資料。
3. 確認人物原語姓名。
4. 確認姓名實際發音。
5. 簡中資料僅供辨識及比較。
6. 最終依台灣繁中慣例決定。

同一人物在全檔中必須保持一致。

如果 value 只有人名本身，不得擅自增加：

* 頭銜。
* 國籍。
* 身分。
* 生卒年。
* 王朝。
* 解釋文字。

---

# 十四、君主、教宗、聖人與宗教人物

同一外語姓名在不同身分下可能具有不同中文慣例。

必須區分：

* 一般世俗人物。
* 君主。
* 王室成員。
* 教宗。
* 天主教聖人。
* 東正教聖人。
* 聖經人物。
* 伊斯蘭宗教人物。
* 其他宗教傳統人物。

不得因 glossary 中存在某個單獨姓名，就跨身分機械統一。

例如普通人物、君主與宗教人物中的：

* John
* Peter
* Paul
* Charles
* Louis
* George
* Alexander

可能需要依具體人物及中文傳統使用不同譯法。

君主姓名優先確認該王室及該人物在台灣歷史資料中的通行譯名。

宗教人物應依該宗教傳統在繁體中文世界中的既有稱呼判斷。

---

# 十五、姓氏、家族與王朝

不得假定：

`人物姓氏 = 家族名稱 = 王朝名稱`

三者一定使用完全相同的中文形式。

必須確認 value 實際表示：

* 一個人的 surname。
* 一個 family。
* 一個 dynasty。
* 一個 house。
* 一個 clan。

若台灣歷史資料已有固定：

* 「……家族」
* 「……王朝」
* 「……家」
* 「……氏」
* 「……王室」

等稱呼，應依 value 是否包含該中心詞判斷。

如果 value 只有家族專名本身，不得擅自增加原文不存在的「家族」「王朝」等字樣，除非遊戲語境明確需要。

---

# 十六、同源姓名與系列一致性

同一 Batch 及全檔內必須檢查：

* 同一 given name 的不同拼法。
* 同一 surname 的不同拼法。
* 男性／女性形式。
* 父名／母名形式。
* 單數／家族形式。
* 同一王朝不同人物。
* 同一語根在不同語言中的形式。
* 古代／中古／現代拼法。

一致性不代表所有同源姓名都必須翻成同一中文名稱。

例如不同語言中的同源姓名，應依各自語言處理。

只有：

**同一語言、同一姓名形式、同一用途**

才應原則上保持相同譯法。

---

# 十七、台灣繁中用字

所有最終譯名必須重新檢查是否符合台灣繁體中文慣例。

尤其注意：

* 人名音譯用字。
* 國名。
* 地名。
* 民族名稱。
* 宗教名稱。
* 歷史名詞。
* 姓名間隔號。
* 簡體中文特有音譯用字。

不得只做簡轉繁。

簡體中文即使能確認人物，也只能作為參考。

---

# 十八、格式與受保護內容

必須保留：

* 所有 localization key。
* key 順序。
* 必要縮排。
* YAML 結構。
* 原有註解。
* section comment。
* 空白分組。
* `$...$`
* `[...]`
* `#...#!`
* `@...!`
* `\n`
* script key。
* localization key。

受保護 token/key 內容不得翻譯。

一般中文標點使用全形。

姓名間隔號統一使用：

`·`

不得使用：

`•`

或其他類似符號代替。

一般斜線分隔使用：

`/`

不得使用：

`／`

斜線兩側不加空格。

如果 value 只有姓名，不得擅自補：

* 句號。
* 說明。
* 生卒年。
* 身分。
* 國籍。
* 原文不存在的括號。

---

# 十九、glossary 命中表

每個 Batch 完成後輸出 glossary 命中表。

至少包含：

* 原文詞條。
* 詞條類型。
* 指定譯名／候選譯名。
* 出現 key。
* 語義適用性。
* 實際採用譯法。
* 檢查結果。

對 glossary 命中分類：

* 固定譯名已套用。
* 參考譯名。
* 候選譯名。
* 詞義不適用。
* 跨文化姓名形式不適用。
* 受保護 token/key，不適用。

如果只是字串相同，但實際為不同文化、不同姓名或不同人物：

標示：

`跨文化姓名形式不適用`

不得因字面命中而強制套用。

如果 glossary 命中只存在於 localization key、script key 或受保護 token：

標示：

`受保護token/key，不適用`

---

# 二十、專名來源分類

每個 Batch 的 QA 中，對較重要、冷門、有歧義或自行音譯的姓名標示來源類型：

* 台灣通行譯名。
* 其他繁中資料可確認。
* 原語資料可確認。
* 簡體資料僅供參考。
* 依原語自行音譯。
* 漢字姓名可確認。
* glossary 固定譯名。
* 歷史語境調整。
* 姓名組裝調整。
* 需人工確認。

不必列出所有完全沒有爭議的普通姓名。

但是以下項目必須列出依據：

* 冷門人物。
* 冷門姓氏。
* 自行擬定音譯。
* 多種可能音譯。
* 原語不明。
* glossary 與外部資料不同。
* 台灣與簡體譯法不同。
* 姓名組裝方式特殊。
* 可能有漢字姓名但不能確認。
* 同名不同文化。

---

# 二十一、語意與姓名 QA

每個 Batch 完成後列出 **3～8 個最值得人工抽查的 key**。

優先列出：

* 台灣與簡體譯法不同。
* 君主名。
* 宗教人物。
* 歷史人物固定譯名。
* 同名但屬不同語言。
* 原語自行音譯。
* 冷門姓氏。
* 父名／母名結構。
* `de/von/van/bin/ibn/al-` 等粒子。
* 漢字姓名判定。
* glossary 跨文化命中。
* 動態姓名組裝。
* `·` 使用方式。
* name order 調整。
* key 與 value 功能不一致。

簡述採用目前譯法的原因。

---

# 二十二、最終技術 QA

每個 Batch 完成後至少進行：

1. key 數檢查。
2. key 順序檢查。
3. 行數檢查。
4. Batch key 與規劃範圍比對。
5. `$...$` token multiset 檢查。
6. `[...]` token multiset 檢查。
7. `#...#!` token 檢查。
8. `@...!` token 檢查。
9. `\n` 檢查。
10. YAML 解析檢查。
11. glossary 實際命中檢查。
12. 同姓名系列一致性檢查。
13. 同文化區塊音譯一致性檢查。
14. 台灣繁中音譯用字檢查。
15. 人物／姓名來源判斷檢查。
16. 漢字姓名檢查。
17. 姓名粒子檢查。
18. name order 檢查。
19. 姓名組裝結果檢查。
20. `·` 使用檢查。
21. 中文姓名內不必要空格檢查。
22. prefix/suffix 功能空格檢查。
23. 需人工確認項目檢查。

若涉及姓名組裝 key，必須額外模擬至少數個實際完整姓名，確認最終結果不會出現：

* 多餘空格。
* 缺少 `·`。
* 重複 `·`。
* 姓名與君主序數間錯誤的 `·`。
* 漢字姓名被插入 `·`。
* prefix/suffix 黏錯位置。
* 粒子重複。
* 頭銜與姓名之間錯誤使用 `·`。
* `$...$` 因修改而失效。

---

# 二十三、人工確認與未決項目

如果某個姓名無法可靠判定：

不得猜測。

列入：

`需人工確認`

並提供：

* key。
* 原文。
* 推定語言／文化。
* 目前可能譯法。
* 疑點。
* 已查到的依據。
* 為何尚不能可靠定案。

單一 Batch 有未決項目時：

* 可以完成該 Batch 其餘已確認內容。
* 可以繼續處理後續 Batch。
* 未決項目必須持續保留於全檔「需人工確認清單」。
* 不得因進入後續 Batch 而遺失。

未決項目不阻止後續 Batch 工作。

但在全檔仍存在未決項目時：

**不得輸出全檔最終合併版。**

只有所有需要人工確認的項目均已解決後，才能輸出最終檔案。

---

# 二十四、固定 glossary 強制檢查

如果任何：

**語義適用且文化／人物身份亦適用的固定 glossary 詞條**

仍未套用，該 Batch 不得標示為完全完成。

必須先：

1. 修正譯文。
2. 重新執行 glossary QA。
3. 重新執行姓名一致性 QA。

以下不視為錯誤：

* 詞義不適用。
* 跨文化姓名形式不適用。
* 受保護 token/key，不適用。

---

# 二十五、Batch 進度追蹤

第一次拆 Batch 時，回覆最前面必須提供完整 Batch 規劃。

包含：

* 本檔總 key 數。
* 完整 Batch 清單。
* 各 Batch key 範圍。
* 各 Batch 主要文化／語言。
* 各 Batch 預估 key 數。
* 處理狀態。

後續每次處理 Batch 時，回覆最前面提供：

* 本檔總 key 數。
* 本次 Batch。
* 本 Batch key 數。
* 本 Batch key 範圍。
* 本 Batch 主要文化／姓名類型。
* 累計已完成 Batch。
* 尚未完成 Batch。
* 全檔待人工確認項目數。
* 是否存在缺漏或跳號。

如果 Batch 規劃沒有變動，不必每次重新完整列出所有已完成 Batch。

可以寫成：

`Batch 1～17 已完成`

`Batch 18 本次處理`

`Batch 19～52 尚未處理`

只有在 Batch 重新拆分時，才必須重新輸出完整 Batch 清單並更新編號。

如果重新拆 Batch：

* 舊 Batch 規劃立即失效。
* 必須重新驗證所有 source key 均被新 Batch 覆蓋。
* 不得造成重複或漏 key。

---

# 二十六、全部 Batch 完成條件

只有同時符合以下條件：

* 所有 source key 均已翻譯。
* 所有 Batch 均已完成。
* 沒有 Batch 跳號。
* 沒有漏 key。
* 沒有重複 key。
* 所有固定 glossary 已正確處理。
* 所有人工確認項目均已解決。
* 全檔姓名一致性 QA 通過。
* 姓名組裝 QA 通過。
* YAML 解析通過。

才可明確表示：

`本檔全部Batch已完成`

並輸出最終合併翻譯檔案。

---

# 二十七、核心判斷原則

遇到任何姓名時，依以下順序思考：

**這個 entry 是什麼姓名元件？**

↓

**它屬於哪個文化／語言？**

↓

**它是一般姓名庫，還是特定歷史人物？**

↓

**glossary 是否有完整且語義適用的固定譯名？**

↓

**台灣是否已有通行譯名？**

↓

**若沒有，原語是什麼、實際怎麼發音？**

↓

**應音譯、使用漢字原名、採傳統譯名，還是保留特殊構詞？**

↓

**這個 component 和其他 component 組裝後，是否符合中文姓名習慣？**

↓

**是否需要 `·`、是否不該有 `·`、順序是否正確？**

↓

**與同文化、同家族、同系列姓名是否一致？**

最終判斷標準不是「每個單獨 value 看起來是否合理」，而是：

**遊戲實際顯示出的完整人物姓名，在歷史、語言與台灣繁體中文三方面是否都合理。**

```

## 人名翻譯交接

```powershell
準備交接到新對話，請執行「EU5 人名翻譯標準交接流程」。

請先停止處理新的 Batch，不要繼續翻譯下一批。

請依照目前實際檔案與成果完成以下工作：

1. 讀取並確認目前使用中的：

   * `character_names_l_english.yml`
   * 最新版 `translation_glossary`
   * `character_names_translation_batch_plan_v2.md`
   * 上一份累積式 checkpoint（若存在）
   * 本對話中所有已完成或修訂過的 `character_names_batch_*_zh_tw_*.yml`

2. 以 `character_names_l_english.yml` 的完整 source key universe 與原始 key 順序為基準，重新核對目前真正已完成的 key，不得只依 Batch 檔名或聊天文字推定進度。

3. 將「上一份累積式 checkpoint + 本對話所有新增／修訂 Batch」合併成一份新的累積式 checkpoint YAML。

   * 必須依原始 source key 順序排列。
   * 不得漏 key、重複 key 或擅自新增 source 不存在的 key。
   * 若同一 key 有不同版本，先判斷是否存在明確新版／修正版；新版優先。
   * 無法自動判定的衝突不得靜默覆蓋，必須列入交接紀錄。
   * 合併後執行 key coverage、duplicate、missing、extra key、localization 結構與 placeholder/token 完整性檢查。

4. 新 checkpoint 檔名統一使用能直接辨識進度的格式，例如：
   `character_names_checkpoint_through_v2_batch_XXX_source_00001-YYYYY_zh_tw.yml`

5. 完成 checkpoint 後，建立本次「交接紀錄」，至少包含：

   * 使用中的 glossary 版本
   * source 檔名
   * Batch plan 版本
   * 最新 checkpoint 檔名
   * 已完成的 v2 Batch 範圍
   * 已完成的 source index 範圍
   * 最後一個已完成 key
   * 下一個應處理的 v2 Batch
   * 下一 Batch 的 source index、first key、last key、key 數
   * 本對話新增或修正的重要翻譯規則
   * duplicate／conflict／待確認項目
   * checkpoint QA 結果

6. 最後另外產生一段可直接複製到「下一個新對話」的開場訊息。新對話必須先從 File Library 讀取最新 checkpoint、source、最新版 glossary 與 Batch plan，重新驗證交接進度後，才從下一個未完成的 v2 Batch 繼續。

請提供：

* 新的累積式 checkpoint YAML 下載檔
* 本次交接紀錄
* 可直接複製到下一個對話的開場訊息

不要在本次對話繼續處理下一個 Batch。

```

## 人名翻譯交接到新對話

```powershell
這是上一個 EU5「人物姓名／專名翻譯」對話的延續。

請不要重新規劃整份檔案，也不要自行重建、簡化或改寫既有翻譯規則。

請先從本 Project／File Library 搜尋並完整讀取以下資料：

1. **Source**

   * `character_names_l_english.yml`

2. **人物姓名翻譯規則**

   * 最新版 `character_names_translation_rules_*.md`
   * 目前基準版本為 `character_names_translation_rules_v1.md`
   * 若存在更新版本，只使用最新版本，舊版規則忽略。
   * 必須以規則檔完整內容為準，不得只依 Project memory 或摘要重建規則。

3. **Glossary**

   * 搜尋最新上傳的 `translation_glossary`
   * 只以最新版本為準，舊 glossary 一律忽略。
   * 必須實際讀取 glossary，不得僅依記憶中的既有譯名工作。

4. **Batch 規劃**

   * `character_names_translation_batch_plan_v2.md`
   * 目前有效規劃為 v2，共 31,108 個 source localization keys、257 個 Batch。
   * 舊 71 Batch 規劃已作廢，不得使用。

5. **翻譯進度／成果**

   * 優先搜尋最新的：
     `character_names_checkpoint_*.yml`
   * checkpoint 為截至上一個對話結束時的累積翻譯成果。
   * 若存在多個 checkpoint，只使用進度最新且 QA 通過的版本。
   * 舊的個別 `character_names_batch_*_zh_tw_*.yml` 原則上僅供歷史核對，不應在已有最新 checkpoint 時重新逐批累加。
   * 若目前尚不存在 checkpoint，才讀取所有既有 `character_names_batch_*_zh_tw_*.yml`，依 source key universe 重建已完成進度。

開始任何新 Batch 前，必須先完成一次「交接驗證」：

* 確認實際讀到的人名翻譯 rules 版本。
* 確認實際使用的 glossary 檔名／版本。
* 確認 Batch plan 為 v2。
* 重新以 `character_names_l_english.yml` 建立／核對完整 source key universe。
* 核對 checkpoint 內的 key 是否全部存在於 source。
* 核對已完成 key 數與 source index。
* 檢查 duplicate key。
* 檢查 missing／extra key。
* 檢查 checkpoint 是否依原始 source key 順序排列。
* 確認上一個已完成的 v2 Batch。
* 確認最後一個已完成 source index 與 key。
* 對照 Batch plan 找出下一個真正尚未完成的 v2 Batch。
* 不得只根據成果檔檔名中的 Batch 編號判定進度。
* 若個別舊 Batch 與 checkpoint 有重疊，以已確認的較新修正版／最新 checkpoint 為準；若存在無法判定的衝突，列出衝突，不得靜默覆蓋。
* 延續上一個對話的全檔「需人工確認清單」，不得因換對話而遺失。

交接驗證完成後，先回報：

* Source 總 key 數
* 使用中的 rules 版本
* 使用中的 glossary 版本
* Batch plan 版本
* 最新 checkpoint 檔名
* 累計已完成的 v2 Batch
* 累計已完成 source index
* 最後一個已完成 key
* 下一個未完成 v2 Batch
* 下一 Batch 的 source index
* 下一 Batch 的 first key → last key
* 下一 Batch key 數
* 全檔目前待人工確認項目數
* 是否發現 duplicate／missing／extra／進度衝突

確認交接狀態後先不要自行開始翻譯下一 Batch。

等我說：

`處理 Batch X`

再依 `character_names_translation_rules` 的完整規則正式處理該 Batch。

每個 Batch 都必須繼續執行規則檔要求的：

* 翻譯前文化／語言／entry 類型分析
* glossary 完整掃描與語義適用性判定
* 必要的外部資料查證
* 台灣繁體中文譯名優先
* 原語與實際發音確認
* 人名／姓氏／王朝／父名／粒子／組裝結構判定
* glossary 命中表
* 專名來源分類
* 語意與姓名 QA
* 最終技術 QA
* 全檔人工確認清單維護

不得因換到新對話而降低查證、QA 或翻譯標準。

```

## Glossary 排序

```
# EU5 Glossary 純排序

請只對 `translation_glossary.yml` 執行排序整理。

本次任務**只允許改變條目的排列順序，不得進行任何 glossary 語意整理或翻譯修改**。

不要修改 `source/english/` 下的任何來源檔。
不要修改任何翻譯檔。
只修改 `translation_glossary.yml`。

## 一、禁止修改的內容

不得：

* 新增 glossary term。
* 刪除 glossary term。
* 合併 fixed。
* 拆分 fixed。
* 建立或刪除 aliases。
* 修改 aliases 成員。
* 建立或刪除 contextual。
* 修改 contextual 的 default、sense 或 when。
* 建立或刪除 reference_terms。
* 修改任何中文譯名。
* 修改任何英文 term。
* 修改任何註解文字。
* 修正文意。
* 修正疑似錯譯。
* 修改 YAML 結構含義。
* 因發現 duplicate 或疑似錯誤而自行修正。

若發現上述問題，只在最後回報，不要處理。

## 二、區域順序

保留 glossary 目前的頂層區域結構。

分別對以下區域獨立排序：

`fixed`

`aliases`

`contextual`

`reference_terms`

不得把不同區域的 term 混在一起排序。

## 三、主要 term 排序

各區域內的主要英文 term 依英文拼寫排序。

排序應：

* 不區分條目原本新增時間。
* 不以空行作為分類邊界。
* 不保留歷史上的新舊條目分組。
* 將整個區域視為同一排序集合。
* 依英文 term 進行穩定且一致的字母排序。
* 不因中文譯名排序。
* 不因註解內容排序。

若英文 term 僅有大小寫差異，使用一致的 case-insensitive 英文字母排序邏輯，但不得修改原始大小寫。

## 四、Aliases 排序

`aliases` 區域：

* canonical／主要 term 依英文拼寫排序。
* 每個 alias 群組必須整組移動。
* `zh` 與其他群組屬性必須跟隨 canonical term。
* `also` 內的 variant 依英文拼寫排序。
* 不得新增、刪除或改寫 variant。
* 不得把 variant 提升為新的主要 term。
* 不得因認為某 variant 是單複數或 morphology 而刪除。

本次只排序。

## 五、Contextual 排序

`contextual` 區域：

* 主要 term 依英文拼寫排序。
* 每個 term 的整個 contextual block 必須一起移動。
* 不改變 `default`。
* 不改變 `senses` 的內容。
* 不改變 `when`。
* 原則上不要重新排列同一 contextual term 內的 senses，除非目前 glossary 已另有明確固定排序規則。
* 註解必須跟隨所屬 term。

## 六、Reference Terms 排序

`reference_terms`：

* 主要 term 依英文拼寫排序。
* 整個 term block 一起移動。
* 不修改 `suggestions` 的內容或順序。
* 不修改 `note`。
* 不修改任何其他欄位。
* 註解跟隨原 term。

## 七、註解與空行

所有與特定條目直接相關的註解，在排序時必須跟隨該條目一起移動。

不得：

* 遺失註解。
* 把註解錯配給另一個 term。
* 改寫註解。
* 因排序而刪除有意義的註解。

空行本身不視為分類資訊。

可為了維持 YAML 可讀性調整區域內多餘空行，但不得利用空行重新建立人工分類。

## 八、驗證

排序完成後：

1. 驗證 YAML 結構仍然有效。
2. 驗證排序前後 glossary term 數量完全一致。
3. 驗證 fixed 條目集合完全一致。
4. 驗證 aliases canonical term 集合完全一致。
5. 驗證每個 aliases 群組的成員集合完全一致。
6. 驗證 contextual term 與所有內容完全一致。
7. 驗證 reference_terms 與所有內容完全一致。
8. 驗證所有中文譯名完全未修改。
9. 驗證所有英文 term 完全未修改。
10. 驗證所有註解內容完全未修改。
11. 驗證只有排列順序發生改變。
12. 確認 `source/english/` 下沒有任何檔案被修改。
13. 確認任何翻譯檔都沒有被修改。

如果發現 duplicate key、疑似錯譯、結構問題或其他 glossary 品質問題：

**只回報，不得在本次排序任務中修正。**

```
