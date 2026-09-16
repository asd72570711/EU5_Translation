# ChatGPT 翻譯

## EU5 本地化翻譯規則

請依照以下規則，將 EU5 localization 翻譯為**台灣繁體中文**。

本規則的優先目標依序為：

1. 不漏 key、不重複 key、不破壞 source 順序。
2. 不破壞遊戲語法、資料型／內容型 token、formatting tag 或 YAML/localization 結構；語法型／語法關係型 placeholder 僅能依第十五節所定的狹義例外處理。
3. 忠實保留原文效果、條件、因果、主詞、受詞、程度、時間關係與完整語意。
4. 正確辨識原文實際指涉、歷史文化身分、詞義、詞性與遊戲機制。
5. 正確套用目前唯一有效的 glossary。
6. **玩家可見的完整句、desc、事件敘述與短文章，首版譯文必須同時通過「語意忠實」「中文母語自然度」與「歷史文化語域適切性」三項硬性標準。即使譯文沒有錯譯，只要仍明顯保留英文語序、關係子句、名詞化、被動、介系詞結構或逐片語對應痕跡，或為追求現代中文自然度而抹除原有歷史制度、文化語感與時代詞彙，就不得視為完成，必須在首版輸出前重新組句。**
7. 在 glossary 未固定或需要 contextual 判斷時，依台灣繁體中文的既有譯名、專業資料與原文化語境，選擇自然、準確且符合成熟母語與歷史語域的譯法。不得以逐詞對應、保留來源語言句法或「文法上成立」作為譯文合格的標準。
8. 維持同一機制、同一事件組、同一實體與同一詞義的譯名一致性。
9. 維持同一事件組、同一敘事段落與相關 localization 的中文文體、語氣與用字品質一致。

不要整檔壓縮式翻譯。

desc、事件敘述、歷史敘事與短文章必須逐句理解原文資訊，不可摘要、概括或省略細節。

但必須嚴格區分：

> **逐句理解原意 ≠ 逐句照英文句型翻譯。**

忠實保留的是原文的**語意結構**，不是英文的**表面句法結構**。

只要完整保留原意、邏輯、條件、因果、程度與遊戲效果，中文可以而且應該依母語習慣：

* 調整語序。
* 拆句。
* 合句。
* 重組主從句。
* 改變修飾語位置。
* 將英文名詞化結構改成中文動詞結構。
* 將不自然的英文被動改為中文自然句式。
* 省略中文不需要重複的主詞或代詞。
* 必要時重新寫出中心名詞以避免代詞指涉不清。
* 將英文慣用語改寫成語意完全等價的自然中文。
* 對語法型／語法關係型 placeholder，僅在第十五節條件全部成立時，允許由自然中文句法或詞彙完整吸收其語意。

不得把：

> 「最接近英文句子結構」

誤認為：

> 「最忠實的翻譯」。

---

## 一、最新 glossary 自動辨識

開始任何統計、拆 Batch 或翻譯之前，必須先從**目前可存取的 File Library 與本對話上傳檔案**中尋找所有可能的：

`translation_glossary*.yml`

並確定本次唯一有效的 glossary。

判定優先順序如下：

1. **使用者在目前對話中明確指定的版本**優先級最高。
2. 若使用者未明確指定，必須比較候選 glossary 的實際版本、內容與檔案 metadata，選擇**最新的實質版本**。
3. 若檔名含有版本時間戳，可作為版本判斷依據之一。
4. File Library 的 CreatedAt／ModifiedAt 可作為版本判斷依據，但不得僅因某份舊 glossary 被較晚重新上傳，就誤判成新版。
5. 若兩份 glossary 內容完全相同，只是檔名或重新上傳時間不同，視為同一實質版本。
6. 若 checkpoint、規則檔或其他可靠專案檔明確記載 authoritative glossary，可用來交叉驗證。
7. 若候選檔內容不同而版本先後仍無法可靠判定，不得混用；必須先進一步比對內容、版本資訊與專案紀錄。

選定後：

* 本次任務只能使用此單一有效 glossary。
* 不得把舊版與新版 glossary 混合。
* 若後續使用者明確指定另一版本，才重新切換。

---

## 二、Source parser 與完整 key universe

開始翻譯前，必須重新從 authoritative Source 建立完整 `source_keys` universe 與原始順序。

Parser 必須容忍：

* 0 個或任意數量空格。
* Tab。
* 混合縮排。
* localization key 與 `:` 之間可能的格式差異。
* value 中的 token、引號、特殊符號與 formatting tag。

不得只依單一 regex 即宣告完整。

主要 parser 完成後，必須再掃描未匹配但疑似 localization entry 的行，確認沒有因格式差異漏 key。

若已有 checkpoint：

* 從 checkpoint 實際內容建立 `translated_keys`。
* 計算 `missing_keys = source_keys - translated_keys`。
* 同時檢查 `extra_keys`、duplicate、conflict。
* 不得只依 checkpoint 檔名或 Batch 編號推定進度。

集合必須滿足：

`translated_keys ∪ missing_keys == source_keys`

且：

`source_keys - translated_keys - missing_keys == ∅`

若有 pending，必須獨立追蹤，不得把 pending 假裝成 confirmed，也不得重複當成一般 missing。

---

## 三、Batch 規劃

若已有經驗證的有效 Batch Plan，優先沿用；不得無理由重切。

若需要建立或重建 Batch Plan：

* 以 `missing_keys` 的 Source 原始順序為基礎。
* 依語意單位、事件組、NAME/DESC、同機制與文本負荷合理分組。
* 不得只追求固定 key 數。
* 極短 UI 與大量長事件敘述不得為湊 key 數而粗暴混合。
* 長 desc、事件敘述、歷史敘事與複雜 placeholder 文本應縮小 Batch，使每條都能在首版輸出前完成完整理解與母語化。

對長文本 Batch，目標不是最大化單批 key 數，而是讓每個文本都能在**首版輸出前**完成：

**完整理解 → 中文母語化重構 → 歷史文化語域校準 → 中文自我潤色 → 原文語意確認**

Batch 規劃完成後必須驗證：

`所有 Batch key 的聯集 == missing_keys`

且：

`各 Batch key 彼此不得重複`

所有 Batch 的 key 數總和必須等於 `missing_keys` 總數。

若後續重新拆分／合併尚未處理 Batch，必須重新執行完整性檢查並同步更新進度。

若「目前下一個 source key」與原 Batch 起點不一致，不得直接假設漏翻；必須重新比較 `source_keys`、`translated_keys`、`missing_keys`。

---

## 四、翻譯前上下文確認

每個 Batch 開始前，至少確認：

* Source 中該 Batch 的完整原文。
* 相鄰 key。
* NAME/DESC 配對。
* title/desc/option/tooltip。
* 同一事件組或事件鏈。
* positive/negative 或互為對照的 localization。
* placeholder scope。
* script key 與 localization key 是否共同提供消歧資訊。
* glossary 命中及其語義適用性。

若單一 value 無法可靠判斷，不得孤立逐句猜測。

---

## 五、玩家可見文字與結構的區分

必須先區分：

1. 玩家可見文字。
2. 受保護遊戲語法。
3. localization reference。
4. script key。
5. formatting control。
6. 純 UI/token 模板結構。

玩家可見文字必須翻譯；真正受保護的控制結構不得翻譯或任意修改。

不得因文字位於 formatting tag 中，就誤認為整段不可翻譯。

---

## 六、核心翻譯原則

### 六之一、語意忠實與中文母語化

忠實的是**命題、邏輯、效果與指涉**，不是英文句法。

不得：

* 漏譯。
* 摘要。
* 增譯。
* 改變主受詞。
* 改變因果。
* 改變條件。
* 改變程度。
* 改變時間關係。
* 改變可能性／必然性。
* 改變遊戲機制。

但若英文句法直接搬入中文會產生翻譯腔，必須重組。

### 六之二、長 desc／事件敘述的四階段內部處理

對長 desc、事件敘述、歷史敘事與短文章，第一次寫入輸出前必須：

1. **完整理解命題**
   * 誰做什麼。
   * 對誰。
   * 為什麼。
   * 結果。
   * 條件。
   * 語氣。
   * 資訊焦點。

2. **脫離英文句法重構中文**
   * 不逐片語拼接。
   * 不機械保留英文關係子句、介系詞或名詞化結構。
   * 依中文資訊結構重新安排。

3. **遮住 Source 做母語編輯**
   * 暫時只讀中文。
   * 若像翻譯稿、語序卡頓、中心名詞堆疊或過度「的」化，直接修正。

4. **回查 Source**
   * 確認沒有因自然化而漏義、增義或改變機制。
   * 確認資料型／內容型 token 完整。
   * 若語法型／語法關係型 placeholder 與 Source 數量不同，必須確認其語意已依第十五節完整、唯一且無歧義地由中文吸收，而非漏掉 token。

不得採：

> 英文片語 A → 中文片語 A  
> 英文片語 B → 中文片語 B  
> 英文片語 C → 中文片語 C  
> 最後把三段拼接

作為長文本主要翻譯方式。

### 六之三、歷史文化語域

EU5 的前現代制度、宗教、軍事、法律、政治、社會與文化文本，必須使用與其時代及文化背景相稱的成熟中文。

不得：

* 為追求現代流暢感，把前現代制度改寫成現代政府、企業、行政或商業術語。
* 為追求歷史感而自行文言化、古典化。
* 增加 Source 不存在的典故、敬語或修辭。

自然化的正確定義是：

> **用更自然的中文表達同一個命題。**

歷史語域校準的正確定義是：

> **用與該時代、制度與文化相稱的中文詞彙與文體表達同一個命題。**

### 六之四、英文表面形式不是中文結構

不得因英文存在：

* 冠詞。
* 複數。
* 所有格。
* 被動。
* 關係代詞。
* 介系詞。
* 名詞化。
* 代名詞重複。

就要求中文逐一產生形式對應。

應先確認該形式真正承載的語意，再用自然中文表達。

### 六之五、不得以「文法沒錯」作為合格標準

只要台灣繁中母語者在移除英文 Source 後仍明顯感覺：

> 「這是一句照英文結構翻出來的中文。」

就必須重寫。

### 六之六、同一事件組的敘事一致性

同一 event group、事件鏈、政策、災難、宗教事件、外交事件、title/desc/option/tooltip 組合必須橫向閱讀。

除了術語一致，還需檢查：

* 敘事人稱。
* 正式程度。
* 同一人物／群體稱呼。
* 相鄰句銜接。
* 同組長 desc 的語氣與品質。
* 歷史語域是否一致。
* 是否某句成熟、某句仍直譯。

同一事件組中不同英文字面不代表中文必須刻意換詞；但 Source 真正有意區分的語義也不能被抹除。

### 六之七、台灣繁中而非簡中直轉

不得因官方簡中已有譯法，就直接簡轉繁。

台灣既有穩定譯名、用字與專業語彙優先。

### 六之八、「網路／網絡」與 network

凡譯文在中文中需要使用「網路／網絡」這組詞時，**一律使用「網路」，不得使用「網絡」**。

但英文 `network` 不得機械固定翻成「網路」。必須依實際語境選擇最自然的台灣繁中，例如：

* communication network → `通訊網路`
* trade network → `貿易網路`
* spy/intelligence network → `間諜網`／`情報網`
* road network → `道路網`
* interpersonal network → `人脈`／`關係網`

判斷重點是自然且準確地表達實際關係；本規則只是排除譯文中的「網絡」，不是把所有 `network` 強制固定成「網路」。

### 六之九、「游牧／遊牧」統一用字

凡指 nomad、nomadic、nomadism 或以逐水草遷徙為核心的社會、文化、經濟與政治概念時，**一律使用「游牧」，不得使用「遊牧」**。

相關衍生詞也必須統一使用「游」字，例如：

* nomad／nomadic people → `游牧民`／`游牧民族`
* nomadic society → `游牧社會`
* nomadic culture → `游牧文化`
* nomadic lifestyle → `游牧生活`
* nomadic economy → `游牧經濟`
* nomadic polity／government → `游牧政體`／`游牧政府`

不得因來源詞性不同、句中作形容詞，或不同批次由不同模型翻譯，就在「游牧」與「遊牧」之間混用。若完整專有名詞或 glossary 已另有明確譯名，仍以該完整名稱為準；但其中一般性的 nomadic 概念仍使用「游牧」。

---

## 七、標題、短 UI 與效果敘述

短 UI、標題、按鈕、modifier、effect、trigger 必須簡潔，但簡潔不代表逐字翻譯。

效果敘述應優先清楚呈現：

* 適用範圍。
* 對象。
* 數值。
* 方向。
* 條件。

不得為了對齊英文詞序製造不自然中文。

---

## 八、歷史制度、宗教、文化與專名

遇到制度、官職、宗教、文化、族群、歷史人物、作品、軍事、法律、地名等專名時：

* 先確認實際指涉。
* 再確認台灣繁中既有譯名。
* 不得只看英文字面猜。
* 不得把功能性英文解釋詞逐字翻成現代中文，而忽略它實際代表的歷史制度或文化實體。

若是歷史文化特有概念，應優先確認：

* 是否有傳統漢譯。
* 是否有學術界穩定譯名。
* 是否是音譯、意譯或混合譯法。
* 是否存在時代差異、外稱／自稱差異。
* 是否因 English localization 已將原語概念解釋化，需回到原實體判斷。

---

## 九、台灣繁中術語與外部資料查證優先順序

查證必須分成兩步：

1. **確認原文實際指涉與語義。**
2. **確認該實體在台灣繁體中文中應使用什麼名稱。**

不得因先找到某個中文譯名，就反過來假定原文一定指該實體。

### A. 原文實際指涉與語義

優先順序：

1. EU5 本身完整上下文。
2. 原語與第一手／文化內部資料。
3. 可靠學術與專業資料。
4. 可靠百科與其他二手資料。
5. 其他可合理輔助判斷的來源。

不得只依英文拼寫、英文 Wikipedia 標題、搜尋摘要、某一份中文譯名或官方簡中名稱判斷原文真正指涉。

### B. 台灣繁中譯名

在實際指涉確認後，優先：

1. 目前唯一有效 glossary 中語義適用的固定譯名。
2. 台灣政府、教育、學術、文化、宗教及相關專業機構的穩定譯名。
3. 台灣學術出版物、專業出版品與穩定慣例。
4. 中文維基百科「臺灣正體（zh-tw）」顯示譯名。
5. 香港、澳門及其他可靠繁中資料。
6. 若無可靠既有譯名，依原語發音、歷史形式、文化背景與台灣音譯慣例自行翻譯。
7. 簡中資料僅作輔助，不得直接簡轉繁當成台灣標準。

### C. 簡體中文資料限制

簡中資料可用於辨認實體、查找原語、理解另一套漢譯傳統及輔助判斷，但不得壓過台灣既有譯名，也不得只做字形轉換。

### D. 專業來源

天主教、基督宗教、佛教、伊斯蘭、歷史地名、民族語言、動植物、制度史、官職與爵位等，應優先檢查相應領域的台灣權威或專業資料。

---

## 十、Glossary 使用規則

翻譯前必須掃描本批原文中的 glossary 命中。

使用：

**longest match first**

但不得只做完全字串比對。

同時必須辨識合理的：

* 單複數。
* 大小寫。
* 所有格。
* 動詞時態／分詞。
* 名詞／形容詞派生。
* 國名／居民／形容詞／語言等詞族關係。
* 宗教／信徒／形容詞等詞族關係。
* 歷史拼寫與可靠轉寫變體。

必須嚴格區分：

> **「屬於同一詞族」**

與：

> **「必須使用完全相同的中文譯名」**

詞族辨識表示應檢查並保留 glossary 的核心概念；若詞性、中心名詞、實體類型或語義功能改變，仍須依中文自然重構。

若 glossary 固定譯名與當前語境表面上不自然，先判斷：

1. 是否其實是不同詞義。
2. 是否發生 metonymy／轉喻。
3. 是否 glossary 本身需 contextual 使用。
4. 是否可由同組 key、script 或機制確認實際指涉。

確認後採取能忠實表達實際指涉、又最大程度保留既有術語核心的 contextual 譯法。

不得靜默永久改名 glossary。

---

## 十一、Comparator／數值 Trigger 規則

`$COMPARATOR$` 與比較值通常構成完整比較條件，中文原則上直接相連：

`$COMPARATOR$$NUM|...$`

不得因英文空格而機械保留：

`$COMPARATOR$ $NUM$`

負向 trigger 不得假設 comparator 固定展開為某一形式。

優先依實際指標重組，例如：

* `……數量並非$COMPARATOR$$NUM$`
* `……總值並非$COMPARATOR$$NUM$`
* `……比例並非$COMPARATOR$$NUM$`
* `……等級並非$COMPARATOR$$NUM$`

`can NOT`：

* 能力不足／條件不成立 → 優先「無法」。
* 規則禁止／不允許 → 優先「不可／不允許」。

---

## 十二、Every 的處理

`every` 不得機械翻成「每個／每一個」。

尤其在 effect、modifier、tooltip、trigger 等**描述效果適用範圍**的語境中，當 `Every + 對象` 表示「符合條件的全部對象均受到此效果」時，繁中原則上優先使用：

* 所有……
* 全部……
* ……均……
* ……都……

例如：

`Every country with X`
→ `所有擁有X的國家`

`Every neighboring country`
→ `所有鄰近國家`

`Every estate loses influence`
→ `所有階層的影響力都會降低`

`Every province owned by us`
→ `我國擁有的所有省份`

只有在真正強調：

* 逐一分配。
* 個別套用。
* 各自承擔。
* 週期頻率。

時，才優先使用：

* 每名……
* 每個……
* 各……
* 每月／每年／每次……

判斷標準不是英文限定詞本身，而是中文效果敘述是在表達**整體適用範圍**還是**逐一分配**。

## 十二之一、`a/an` 不定冠詞的處理

英文 `a/an` 不得機械翻成「一個」，也不得一律省略。必須先判斷它在完整句子中只是英文文法所需的冠詞，
還是實際承載了引入對象、單一數量、任選其一、不特定對象或子類關係等語意。

以下情況通常省略 `a/an`：

* 概念、術語或類別的定義句。
* 泛指某類人物、事物或機制的一般性質。
* 身分、職業或類別判定，且中文不需要量詞。
* 動作受詞不強調數量，也沒有引入特定個體的功能。

例如：

`A $game_concept_domestic_market$ is a [market_with_icon|e] in which you own [locations_with_icon|e].`
→ `$game_concept_domestic_market$是你擁有[locations_with_icon|e]的[market_with_icon|e]。`

不得機械寫成：

`一個$game_concept_domestic_market$是你擁有[locations_with_icon|e]的一個[market_with_icon|e]。`

`A [character|e] can have three [traits|e].`
→ `[character|e]可以擁有三項[traits|e]。`

以下情況必須保留 `a/an` 所承載的語意：

* 首次引入一個具體的新對象。
* 強調數量恰好為一，或與零個、多個形成對比。
* 從多個候選中選擇任一個對象。
* 表示不特定的「某一／某個」對象。
* 表示「一種／一類／其中之一」的子類或分類關係。

例如：

`A merchant arrived at court.`
→ `一名商人來到宮廷。`

`Select a [location|e].`
→ `選擇一處[location|e]。`

`Granted to a [country|e].`
→ `授予某個[country|e]。`

`A $game_concept_ruler_trait$ is a type of [trait|e].`
→ `$game_concept_ruler_trait$是一種[trait|e]。`

需要表達單一對象時，不得一律使用「一個」，必須依 token 實際展開的中心名詞選擇自然量詞，例如：

* 人物：一名／一位。
* 地點：一處。
* 建築：一座。
* 船艦：一艘。
* 制度、效果、議題：一項。
* 類型：一種。
* 不特定對象：某個／某一，並依中心名詞調整。

遇到 `a/an + token` 時，必須暫時代入至少一個合理的中文展開值，檢查：

1. 冠詞是否只是在滿足英文單數可數名詞語法。
2. 省略後是否仍完整保留單一數量、引介、選擇或分類語意。
3. 若需保留，量詞是否符合中心名詞，而不是機械使用「一個」。
4. 譯文是否出現「一個市場是一個市場」或「一個角色」等可省略或量詞不自然的直譯結構。

---

## 十三、受保護 token 與格式

必須保留：

* localization key。
* key 順序。
* 必要縮排。
* YAML/localization 結構。
* `\n`
* formatting tag 的控制語法與結構。
* script key。
* localization key。
* 所有資料型／內容型 `$...$`、`[...]`、`@...!` token。

所有**實際保留**的 `$...$`、`[...]`、`@...!` token 內部內容不得翻譯、改寫、拼字修正或變更參數。

資料型／內容型 token，例如：

* 人名。
* 國名。
* 地名。
* 數值。
* 效果。
* modifier。
* game concept。
* localization reference。
* 動態實體名稱。

不得為了中文流暢而刪除。

只有第十五節所定的**語法型／語法關係型 placeholder 語意吸收例外**，可以在嚴格條件全部成立時不逐一保留其 token；不得把這個例外擴張到一般資料型／內容型 token。

普通英文正文空格不是遊戲語法；翻譯後依第二十節處理。

一般中文標點使用全形。

### Token／localization reference 外側的玩家可見標點

protected token 或 localization reference 的保護範圍只包含 token 本體；緊接在 token 外側的標點仍是玩家可見文字，
必須依繁體中文句法翻譯，不得因整個 value 幾乎只有 token 就原樣保留英文標點。

例如：

`$REF$.`
→ `$REF$。`

`$REF$,`
→ `$REF$，`

`$REF$:`
→ `$REF$：`

`$REF$;`
→ `$REF$；`

`$REF$?`
→ `$REF$？`

`$REF$!`
→ `$REF$！`

同一規則也適用於 `[...]`、`#!` 或其他 protected token 結束後的玩家可見標點，例如：

`[country|e].`
→ `[country|e]。`

`#Y Text#!.`
→ `#Y 文字#!。`

若能解析 localization reference，必須先檢查被引用譯文的實際結尾：

* 被引用譯文已帶有等價句末標點時，移除外層重複標點，避免展開後出現 `。。`、`！！` 或 `？？`。
* 被引用譯文沒有句末標點時，保留外層標點並轉為適當的中文全形標點。
* 無法確認 reference 展開內容時，不得擅自刪除外層標點；應保守保留並轉為中文標點。

以下半形標點屬資料、格式或程式語法，不得機械轉為全形：

* 時間，例如 `$MIN$:$SEC$`、`12:30`。
* 小數、百分比格式或版本號，例如 `1.5`、`v1.2.0`。
* 網址、電子郵件、檔名與副檔名。
* protected token 內部的運算子、參數分隔、格式碼及其他語法。
* code-like、debug 或 API 文字中具有語法功能的標點。

一般斜線分隔使用：

`/`

不得機械改為全形斜線 `／`。

---

## 十四、Formatting tag 內可見文字

`#...#!` 不得整體視為不可翻譯 token。

必須拆成：

1. 開頭格式控制碼，例如 `#italic `、`#T `、`#Y `、`#G `、`#R `。
2. tag 內玩家可見文字。
3. 結尾 `#!`。

只有控制碼與結構受保護。

tag 內玩家可見文字必須正常翻譯、glossary 掃描、專名判斷與歷史制度判斷。

例如：

`#T Important Offices#!`
→ `#T 重要職位#!`

`#Y Sea#!`
→ `#Y 海域#!`

翻譯後必須保持：

* tag 類型一致。
* 開啟／關閉數量一致。
* `#!` 完整。
* 巢狀結構一致。
* 控制語法未遭破壞。
* formatting tag 控制語法所需空格保留。

開啟 formatting tag 與其玩家可見內容之間的普通 ASCII 空格屬於必要控制語法，必須保留。例如：

`#G 中文#!`
`#R 中文#!`
`#Y 中文#!`

但玩家可見內容結尾與關閉標記 `#!` 之間不需要空格。Source 中位於 `#!` 前的英文尾端空格
不屬於控制語法，翻譯時必須移除，讓 `#!` 直接接在最後一個可見字元或 token 後。

例如：

`#T Lost units #!\n The total units lost during the battle.`
→ `#T 損失的單位#!\n戰鬥期間損失的單位總數。`

不得寫成：

`#T 損失的單位 #!\n戰鬥期間損失的單位總數。`

若同一行在 `#!` 後還有另一個需要視覺間距的內容，間距必須放在 `#!` 外側，並依第二十節使用真正的 NBSP：

`#Y Name #! $VALUE$`
→ `#Y 名稱#! $VALUE$`

不得為了保留間距，把普通空格或 NBSP 留在玩家可見內容與 `#!` 之間。

錯誤：

`#G中文#!`
`#R中文#!`
`#G 中文 #!`
`#R 中文 #!`

---

## 十五、角色代名詞與語法關係型 placeholder

本節處理：

* `[...GetHerHis]`
* `[...GetHisHer]`
* `[...GetSheHe]`
* `[...GetHeShe]`
* `[...GetHerHim]`
* `[...GetHimHer]`
* `[...GetHerselfHimself]`
* 以及其他實際功能為人稱、所有格、受格、反身、性別化代詞等的語法型／語法關係型 placeholder。

**不能只看到 token 名稱就自動刪除；判斷標準永遠是該 token 在當前句子承載的實際語意功能。**

### A. 先判斷 placeholder 是否必須顯式保留

Source 與譯文的 token 數量**原則上應一致**。

但若某個語法型／語法關係型 placeholder 所承載的語意，已能由自然中文句法或詞彙**完整、唯一、無歧義**地吸收，則可不在譯文中逐一保留該 placeholder。

例如：

`[target_ruler.GetNameWithNoTooltip] should visit [target_location.GetNameWithNoTooltip] [target_ruler.GetHerselfHimself].`

可自然重構為：

`[target_ruler.GetNameWithNoTooltip]應親自拜訪[target_location.GetNameWithNoTooltip]。`

此處 `[target_ruler.GetHerselfHimself]` 的「本人親自」語意已由「親自」完整承接，因此不必硬譯成另一個代詞結構。

語法型 placeholder 的省略必須同時滿足：

1. 原文人物指涉不變。
2. 人稱、所有關係、反身關係、性別差異、對比或強調等實際語意沒有遺失。
3. 省略後不造成主詞、受詞或所屬關係歧義。
4. 不會因 placeholder 的不同動態輸出，而使被省略的資訊在中文中產生實質不同意思。
5. 譯文完整保留 Source 命題。
6. 省略是自然中文重構的結果，不是為了讓 token QA 比較方便或減少工作。

若任一條不成立，必須保留 placeholder 所承載的語意。

### B. `GetHerHis`／`GetHisHer` 的「的」

`[...GetHerHis]`、`[...GetHisHer]` 在本專案繁中輸出中只會產生「他／她」，**絕對不自帶「的」**。

`|U`、`|L` 等顯示修飾只影響輸出形式，不改變 placeholder 的人稱或所有格語法功能，
也不會自動補出「的」。因此 `[...GetHerHis|U]`、`[...GetHisHer|U]` 仍必須依完整中文句法，
按照本節相同規則判斷是否補「的」，不得把帶修飾符的形式視為例外。

因此判斷順序必須是：

1. 先判斷所有格語意是否可由中文完整吸收；只有符合 A 的全部條件時，才可不顯式保留 placeholder。
2. 若 placeholder 仍需保留，先把它視為實際輸出的「他／她」。
3. 再閱讀完整中文，判斷是否需要補「的」。

不得：

* 誤以為 placeholder 會輸出「他的／她的」。
* 因英文使用 possessive 就不經中文句法判斷直接省略「的」。
* 對所有所有格 placeholder 一律機械補「的」。

一般領屬名詞組若省略「的」會形成不自然結構，必須補「的」：

`[target_character.GetHerHis] loyalty`
→ `[target_character.GetHerHis]的忠誠`

`[target_character.GetHerHis] head`
→ `[target_character.GetHerHis]的頭顱`

`[target_character.GetHerHis] life`
→ `[target_character.GetHerHis]的性命`

`[target_character.GetHerHis] crimes`
→ `[target_character.GetHerHis]的罪行`

`[target_artist.GetHerHis|U] work`
→ `[target_artist.GetHerHis|U]的作品`

`[target_artist.GetHerHis|U] works`
→ `[target_artist.GetHerHis|U]的作品`

若需改寫成「筆下」結構，仍要檢查完整名詞組：

`[target_artist.GetHerHis|U] written words`
→ `[target_artist.GetHerHis|U]筆下的文字`

不得寫成：

* `[target_artist.GetHerHis|U]作品`
* `[target_artist.GetHerHis|U]筆下文字`

若完整中文本來就是成熟慣用結構，可以不加「的」：

`in [target_character.GetHerHis] hand`
→ `在[target_character.GetHerHis]手中`

同理：

* `在他手中`
* `在她肩上`
* `在他眼前`

可自然成立。

判斷時必須實際把 placeholder 分別代成「他」「她」閱讀完整句子。

若出現：

* `他頭顱`
* `她性命`
* `他忠誠`
* `她罪行`

表示缺少「的」或句子需要重組。

### C. `GetHerHis` 也可能被中文吸收，但不可機械省略

例如某些上下文中，英文所有格只是英文句法要求，而中文省略所有格後仍能唯一確認關係，則可以重組。

但若所有關係本身具有：

* 辨識功能。
* 對比功能。
* 敘事功能。
* 主體區分功能。

則必須保留其語意。

因此：

> **真正需要判斷的是 token 的語義功能，不是 token 名稱本身。**

---

## 十六、GetFlavorRank

`[...GetFlavorRank]` 會輸出依國家、政體、文化、政府形式與當前等級變化的完整特色化稱號。

不得預設它一定是：

* 王國。
* 共和國。
* 帝國。
* 國家。
* 政權。

必須把整個 placeholder 視為可直接充當主詞、受詞或名詞成分的完整稱號。

不得：

* 刪除 placeholder。
* 固定翻成某一稱號。
* 在前後加入可能與實際輸出重複的「國家」「政權」「我國」等中心名詞。

尤其：

`我國[...GetFlavorRank]`

原則上視為高風險／錯誤結構，必須重組。

英文：

`the [...GetFlavorRank]`

通常可直接譯為 placeholder。

英文：

`our [...GetFlavorRank]`

依語境可使用：

* `我們的[...GetFlavorRank]`
* `本[...GetFlavorRank]`
* 或自然重組整句。

翻譯與 QA 時，應將 placeholder 暫時代入「王國」「帝國」「公國」「共和國」「蘇丹國」等不同合理稱號，確認任何合理展開下中文都自然且不重複中心名詞。

---

## 十七、一般概念 token 的中心名詞

`[country|e]`、`[location|e]`、`[culture|e]`、`[religion|e]`、`[capital|e]`、`[market|e]` 等概念 token，通常已會顯示完整中心名詞。

不得再補同義中心名詞造成重複。

例如：

`our [country|e]`
→ `我們的[country|e]`

不得：

* `我國[country|e]`
* `我們的國家[country|e]`
* `國家[country|e]`
* `首都[capital|e]`
* `市場[market|e]`

若中文自然語序需要調整，優先重組句子；**這類一般概念／資料型 token 必須保留，不適用第十五節的語法型 placeholder 省略例外。**

### 動詞型概念 token 的詞形與中文語法

`[occupied|e]`、`[occupying|e]` 等動詞型概念 token 的英文名稱可能帶有 `-ed`、`-ing` 或其他詞形，
但本專案的中文概念顯示值原則上使用穩定的原形詞義，例如「佔領」。`|e` 只負責建立概念連結，
英文 token 名稱中的詞形也不會自動替中文補出時態、語態、進行、完成、分詞、動名詞或修飾關係。

翻譯時必須：

1. 完整保留原 token，不得把 `[occupying|e]` 擅自改成 `[occupy|e]`。
2. 將 token 暫時視為其中文原形譯名，再依完整句意重建自然中文語法。
3. 視語境在 token 外補上「已」「曾」「正」「正在」「持續」「被」「遭」「受到」「的」「時」「期間」「透過」等必要成分。
4. 不得假設英文詞形已由 token 的中文顯示值承擔，也不得逐字保留英文助動詞與語序。

例如概念 token 顯示為「佔領」時：

`is [occupied|e]`
→ `遭[occupied|e]`／`被[occupied|e]`

`has [occupied|e] the city`
→ `已[occupied|e]該城市`

`is [occupying|e] the city`
→ `正在[occupying|e]該城市`

`while [occupying|e] the city`
→ `[occupying|e]該城市期間`

`by [occupying|e] territory`
→ `透過[occupying|e]領土`

`[occupied|e] [locations|e]`
→ `遭[occupied|e]的[locations|e]`

不得機械處理英文詞尾：

* `-ed` 可能表示過去、完成、被動或形容詞化分詞，不得一律補「被／遭」或「已」。
* `-ing` 可能表示進行式、動名詞或現在分詞，不得一律補「正在」。
* 只有語境確實強調動作正在進行時，才使用「正／正在」；表示手段、一般行為或名詞修飾時，應依中文自然重組。
* 中文不需要明示時態或進行狀態時，不要為了對應英文詞尾強行加入標記。

翻譯 `game_concept` 本身的顯示值時，同一動作的 `Occupy`、`Occupied`、`Occupying` 等詞形原則上使用相同的中文原形詞義；
只有 glossary、既有專案規則或實際概念差異明確要求區分時，才使用不同譯名。

---

## 十八、文化名稱 placeholder

`[...GetCulture.GetName]`、`[...GetCulture.GetNameWithNoTooltip]` 通常只輸出文化名稱，不自帶「人」。

當英文 `a/an + [Culture placeholder]` 是指某文化背景的人時，中文必須補出中心名詞，通常：

`一名[Culture placeholder]人`

若原文指文化本身，不得補「人」。

---

## 十九、語言與方言 placeholder

本專案中：

* `GetCommonLanguage.GetName`
* `GetLanguage.GetName`
* `GetDialect.GetName`
* `GetDialect.GetNameWithNoTooltip`
* 各類 `dialect.GetNameWithNoTooltip`

其繁中輸出本身已包含「語」。

因此 placeholder 後不得再加：

* 語。
* 語言。
* 方言。

即使英文寫：

`[placeholder] language`
`[placeholder] dialect`

中文也必須省略重複中心名詞或重組句子。

---

## 二十、Placeholder/token 邊界、NBSP 與結構性空格

空格必須依功能處理，不得直接沿用英文詞間空格。

本專案的基本原則是：

* 中文語法不需要的空格直接刪除。
* 玩家可見且確實需要保留的分隔空格，原則上改用真正的 `U+00A0` 不換行空格（NBSP）。
* 只有 formatting/control 語法要求的空格，以及 protected token 內部原有的空格，才保留普通 ASCII 空格（`U+0020`）。
* 不得以 `&nbsp;` 或字面上的 `\u00A0` 代替真正的 NBSP，避免它們在遊戲中直接顯示為文字。

### A. 內容型 token／placeholder 與中文正文的外部邊界

當 `$...$`、`[...]`、數字 token、tooltip token、localization reference 等**內容型 token**與中文玩家可見文字直接相鄰時，原則上不得保留或新增英文式半形空格。

不得因 Source 中 token 與英文正文之間有空格，就把該空格直接沿用到繁中。

例如：

`$catholic_flavor.100.desc$ Now that...`
→ `$catholic_flavor.100.desc$如今……`

不得：

`$catholic_flavor.100.desc$ 如今……`

其他例子：

`[target_character.GetName] years old`
→ `[target_character.GetName]歲`

`#G +100#! [prestige|e]`
→ `#G +100#![prestige|e]`

### B. formatting/control 與 protected token 內部必要空格

格式控制語法本身要求的普通 ASCII 空格必須保留，不得改成 NBSP。

例如：

`#G 中文#!`
`#R 中文#!`
`#T 標題#!`
`#G +100#!`
`#italic Text#!`
`#TOOLTIP:$TAG$ $TEXT$#!`

不得改成：

`#G中文#!`
`#R中文#!`

此處的空格屬於控制結構，不是英文正文詞間空格。

protected token 內部原有的空格也必須逐字保留，例如：

`[SelectLocalization( CONDITION , 'YES', 'NO' )]`

不得刪除、增加或改成 NBSP。

### C. 多個 token 組成名稱或中文詞組

`$...$ $...$` 或 `[...] [...]` 即使整個 value 幾乎只由 token 組成，也不一定是 UI 模板。
翻譯前必須先讀取 localization key、上下文、token 名稱與可解析的引用內容，判斷各 token 展開後的語意角色，
再決定使用無分隔、音界號、NBSP、中文連接成分或調整語序。

不得只因 Source 以普通空格分隔，就機械保留空格、改成 NBSP、刪除空格或加入音界號。

處理原則：

* 已確認為同一位人物的外國音譯姓名片段時，依台灣既有譯名與該語言慣例決定是否使用音界號 `·`。
* 採漢字姓名的漢字文化圈人物，姓氏與名字直接相連，不使用普通空格、NBSP 或音界號。
* 頭銜、序數、尊稱、綽號、王朝名與姓名的組合，依中文慣用語序重組，不得機械以音界號連接。
* 共同構成中文複合詞或語法詞組時，移除空格，或依語意補入「的」「之」等中文成分。
* 只有確認為彼此獨立且需要視覺間距的 UI 元件時，才依下一節使用 NBSP。

例如，已確認為外國音譯姓名時：

`$FIRSTNAME$ $LASTNAME$`
→ `$FIRSTNAME$·$LASTNAME$`

採漢字姓名時：

`$name_yang.mandarin_language$ $name_shen4.mandarin_language$`
→ `$name_yang.mandarin_language$$name_shen4.mandarin_language$`

展開後應為「楊慎」，不得形成「楊·慎」或「楊 慎」。同一原則適用於採傳統漢字姓名的中國、日本、朝鮮與越南人物。

「東方人名」不得作為一律省略音界號的判準。阿拉伯、波斯、印度、蒙古及其他亞洲文化的音譯姓名，
仍須依實際人物、完整姓名的台灣慣例與各語言結構判斷。

頭銜與姓名例如：

`$TITLE$ $NAME$`
→ 依語境重組為 `$TITLE$$NAME$` 或 `$NAME$$TITLE$`

不得寫成 `$TITLE$·$NAME$`，除非經確認音界號本來就是該完整專名的一部分。

中文詞組例如：

`$ESTATE$ [culture|e]`
→ `$ESTATE$[culture|e]`

若兩個 token 在執行時可能展開為不同文化的姓名，固定使用音界號、無分隔或 NBSP 都可能出錯。此時必須：

1. 檢查 key、相鄰 localization、token 定義與實際使用範圍，確認是否已限定文化。
2. 優先沿用既有的完整姓名 getter 或文化感知格式，但不得擅自改寫 protected token。
3. 若無法可靠判定且現有結構不能依文化切換，使用 NBSP 作為中性顯示退路，並將此項保留為需人工確認；不得宣稱其符合所有姓名慣例。

### D. 已確認 UI 模板中的結構性空格

若 localization value 是圖示、名稱、數值、旗幟或其他 UI 元件的組合，且元件間需要可見間距，
一律以真正的 NBSP 取代 Source 的普通空格，使相關元件保有間距但不在該邊界斷行。

例如 Source：

`game_concept_with_icon: "$ICON$ $NAME$"`

譯文改為：

`"$ICON$ $NAME$"`

其中 `$ICON$` 與 `$NAME$` 之間必須是真正的 `U+00A0`，不能是普通空格。

其他例子：

`@blue_left! $AMOUNT$ [GOODS.GetIcon][GOODS.GetName]`
→ `@blue_left! $AMOUNT$ [GOODS.GetIcon][GOODS.GetName]`

`[FROM.GetFlagIcon] [FROM.GetName] @blue_left! [TO.GetFlagIcon] [TO.GetName]`
→ `[FROM.GetFlagIcon] [FROM.GetName] @blue_left! [TO.GetFlagIcon] [TO.GetName]`

不得為了保留 Source 外觀而留下普通空格，也不得把需要的視覺間距完全刪除，例如：

`"$ICON$$NAME$"`

若 Source 本來沒有空格，且元件間也不需要可見間距，例如：

`"$ICON$$NAME$"`

則維持無空格，不得自行加入 NBSP。

### E. 自動換行與 `\n`

中文內容超過 UI 寬度時交由遊戲自動換行，不得為了模擬英文空格換行而保留普通空格。

`\n` 是固定強制換行，只能用於：

* Source 原本存在且必須保留的換行。
* 標題、內文、清單或段落等語意上明確需要固定分行的結構。
* 已確認特定 UI 必須固定分行的情況。

不得只因預測文字可能過長，就自行加入 `\n`。同一 localization 可能出現在不同面板寬度、解析度或字體設定下，
一般寬度溢出應交由遊戲自動處理。

### F. 清單、項目符號與指示標記後的空格

當 `•`、行首 `-`、`▪`、`◦`、`‣`、編號（如 `1.`、`1)`）或其他圖形符號確實作為清單／項目標記時，
標記與第一個可見內容或 token 之間必須保留視覺間距，並將 Source 的普通空格改為一個真正的 `U+00A0` NBSP。
這能避免項目符號單獨留在上一行。

例如：

`• $SIZE|Y$`
→ `• $SIZE|Y$`

`\n- [ShowModifier('winter_none')]`
→ `\n- [ShowModifier('winter_none')]`

`#indent_newline:2 • Source text`
→ `#indent_newline:2 • 中文內容`

上例中 `#indent_newline:2` 後的普通 ASCII 空格屬 formatting/control 語法，必須保留；
只有 `•` 與玩家可見內容之間的分隔空格改為 NBSP。

若 localization 本身只提供可重複引用的項目符號與尾端分隔，例如：

`BULLET: "• "`

其尾端普通空格也應改為真正的 NBSP：

`BULLET: "• "`

一般清單標記後原則上統一為一個 NBSP。只有確認多個空格屬於特定 UI 的對齊結構時，才保留其結構，
不得在未確認用途時機械保留多個普通空格。

本規則只適用於確定具有清單／指示功能的標記，不得只看符號字形套用：

* `#G +100#!` 的 `+` 是正號，不是清單標記。
* `-10%` 的 `-` 是負號，不是清單標記。
* `A - B` 中的 `-` 是內容分隔符，應依中文語意改用冒號、破折號或其他合適標點。
* `→$TAB$$DIPLOMACY$` 的箭頭後原本沒有空格，不得自行加入 NBSP。
* Source 中標記與內容原本無空格，且不需要視覺間距時，不得自行新增 NBSP。

因此必須先判斷空格是：

1. 英文正文詞間空格。
2. formatting/control 必要空格。
3. protected token 內部空格。
4. 多個 token 組成名稱或中文詞組時的語意邊界。
5. 玩家可見的 UI/token-template 分隔空格。
6. 清單或指示標記與首項內容之間的分隔空格。

再分別決定刪除、保留 ASCII 空格、加入音界號或中文連接成分、調整語序，或改用 NBSP。

---

## 二十一、人名、歷史人物、作品與 music_player

歷史人物、君主、宗教人物、事件人物：

* glossary 有語義適用固定譯名 → 使用 glossary。
* glossary 未固定時，先確認人物實際身分。
* 有台灣繁中通行譯名 → 優先採用台灣通行譯名。
* 中文維基若用於台灣譯名判斷，必須確認臺灣正體（zh-tw）。
* 無既有譯名 → 依原語、歷史語境與台灣慣例音譯。
* 不得只做簡體轉繁體。
* 不得把無法確認的歷史人物硬套成另一位同名人物。

漢字文化圈人物：

* 能可靠確認歷史漢字姓名者，優先原有漢字姓名。
* 不得把已有漢字姓名的人物重新按外語發音音譯。
* 無法確認漢字原名時才保守音譯。

多個動態 token 組成人名時，同樣適用第二十節的多 token 語意判斷：

* 外國音譯姓名只有在確認完整姓名慣例後才於 token 之間加入 `·`，音界號前後不得留空格。
* 採漢字姓名的漢字文化圈人物，其姓名 token 直接相連。
* 不得把 Source 姓名片段間的空格機械改成普通空格、NBSP 或音界號。
* 完整人物 glossary 或既有通行全名優先於對 given name、surname、頭銜或粒子的個別猜測。
* `de`、`von`、`al-` 等姓名粒子是否獨立、連寫、音譯或省略，依完整姓名的既有譯法判斷，不得只按 token 邊界處理。
* 若同一動態格式可能產生多種文化姓名，必須先確認使用範圍；無法可靠判定時依第二十節採中性退路並保留人工確認。

music_player 中所有玩家可見曲名、版本名、作曲家、演奏者、樂器、曲目介紹均翻成繁中。

---

## 二十二、不確定項目的自行處理

遇到不確定的專名、制度、官職、宗教詞、詞義、glossary contextual 適用性或英文工程句型：

不得直接猜測，也不要僅因不確定就停止整個 Batch。

處理順序：

1. 檢查最新版 glossary。
2. localization key 與相鄰同組 key。
3. 完整事件組／NAME-DESC／positive-negative 配對。
4. placeholder 與 scope 類型。
5. 依第九節先確認實際指涉。
6. 再確認台灣既有譯名。
7. 必要時用原語、第一手、學術、專業或 EU5 機制資料交叉驗證。
8. 仍無法完全確認時，選擇最保守、語義透明、最少自行添加資訊的可用譯法。

不得為追求「精確歷史名稱」而假裝已考證成功。

若 Source 疑似有問題：

* 不得僅因外部資料不同就自行大幅改寫。
* 先確認證據是否足夠。
* glossary 已裁定則依 glossary。
* glossary 未裁定則採最保守且不製造錯誤歷史資訊的譯法。

若原文語意已可靠確認，只是存在多種都正確的中文寫法，優先較自然、清楚、流暢、少翻譯腔且歷史語域適切者。

---

## 二十三、每個 Batch 必做 QA

所有 QA 必須實際執行，但除非使用者另有要求，不在最終回覆顯示 QA 內容。

### A. key／集合／順序

* 本批輸出 key 與實際 `missing_keys` 一致。
* key 數一致。
* Source 順序一致。
* 不漏、不重複、不混入已翻譯 key。
* 本批後重新計算 remaining missing。

### B. 行與結構

* YAML/localization 結構未破壞。
* 語言標頭、縮排與引號合理。
* parser 格式差異未造成漏 entry。

### C. token／placeholder

逐 entry 分類比較 Source 與 Target token。

#### 必須嚴格一致的資料型／內容型 token

包括但不限於：

* localization reference `$...$`
* game concept／動態實體 `[...]`
* `@...!`
* 數值與 script token
* 名稱、地名、國名、modifier、effect 等動態資料 token

其內容與必要數量不得改變。

#### 語法型／語法關係型 placeholder

若 `GetHerHis`、`GetHerselfHimself`、`GetSheHe`、`GetHerHim` 等語法型 placeholder 數量與 Source 不一致：

**不得直接判定為 token mismatch，也不得直接放行。**

必須逐一確認：

1. 是否為第十五節允許的自然中文語意吸收。
2. 原人物指涉是否仍唯一。
3. 所有格／反身／人稱／性別／強調語意是否完整。
4. 是否沒有因不同動態輸出而遺失實質資訊。
5. 是否確實不是漏譯或誤刪。

未能證明者，一律視為 token 錯誤並修正。

### D. formatting tag

檢查：

* tag 類型。
* 開啟／關閉數量。
* `#!`。
* 巢狀結構。
* 控制語法。
* 必要空格。
* tag 內玩家可見文字沒有漏翻。
* 開啟標記後的必要 ASCII 空格仍存在，例如 `#T 標題#!`，不得變成 `#T標題#!`。
* 玩家可見內容與 `#!` 之間沒有殘留普通空格或 NBSP，例如不得出現 `#T 標題 #!` 或 `#T 標題 #!`。
* `#!` 後若需要與下一個 UI 元件保持間距，該間距位於標記外側並使用真正的 NBSP。
* `\n` 後沒有直接沿用英文正文開頭空格，例如使用 `#!\n內容`，不得使用 `#!\n 內容`。

### E. glossary

建立 glossary 命中與 contextual 判斷，避免：

* 漏套固定核心術語。
* 詞族誤判。
* 不同實體因表面相似被錯誤統一。
* contextual 使用被誤當成永久修改 glossary。

### F. 專名／台灣譯名 QA

高風險專名確認：

* 實際指涉。
* 原語。
* 台灣既有譯名。
* zh-tw 是否確認。
* 簡中是否被誤當台灣標準。
* nomad、nomadic、nomadism 及其衍生概念是否統一使用「游牧」，沒有混入「遊牧」。

### G. 語意 QA

優先抽查多義詞、歷史制度、冷門專名、因果句、長 desc、複雜 placeholder、comparator trigger 等。

確認無：

* 摘要。
* 漏句。
* 主受詞反轉。
* 因果／條件／程度改變。
* 自行增加資訊。
* 歷史制度現代化。
* 為追求歷史感自行文言化。
* 將定義句或泛指句中的 `a/an` 機械翻成「一個」。
* 在 `a/an` 確實表示單一數量、引入對象、任選其一或子類關係時，誤將其語意省略。
* 對人物、地點、建築、船艦、制度或類型使用不自然的通用量詞；遇到 token 時應代入實際中心名詞檢查。

### H. 特殊 placeholder QA

#### `GetHerHis`／`GetHisHer`

先判斷 placeholder 是否依第十五節需要顯式保留。

`|U`、`|L` 等顯示修飾不會改變本項檢查；`[...GetHerHis|U]` 與未帶修飾符的形式
必須套用相同的所有格 QA。

若保留：

* 分別替換成「他」「她」閱讀完整繁中。
* `他頭顱`、`她性命`、`他忠誠`、`他作品`、`她筆下文字` 等 → 必須修正。
* `在他手中`、`在她肩上`、`在他眼前` 等 → 可省略「的」。
若省略：

* 必須確認其所有關係等語意已由中文完整吸收，不得以「中文可以省略代詞」為由直接刪 token。

#### 動詞型概念 token

* 確認 `[...|e]` token 原樣保留，沒有因英文詞形而改寫 token 名稱。
* 暫時將 token 代入其中文原形譯名，重新閱讀完整句子。
* 檢查英文的過去、完成、被動、進行、分詞、動名詞及修飾關係是否已由中文自然表達。
* `是佔領`、`佔領的地點`、`透過正在佔領領土` 等因缺少語法成分或機械對應英文詞形而不自然的結構，必須修正。
* 不得看到 `-ed` 就一律補「被／遭」，也不得看到 `-ing` 就一律補「正在」。

#### `GetFlavorRank`

* 不得出現 `我國[...GetFlavorRank]`、`國家[...GetFlavorRank]`、`政權[...GetFlavorRank]` 等可能中心名詞重複結構。
* 暫時代入「王國／帝國／公國／共和國／蘇丹國」等不同合理稱號，確認句子均自然。
* `GetFlavorRank` 本身屬資料型／內容型動態稱號，不得依第十五節刪除。

#### 其他

檢查：

* 語言／方言 placeholder。
* 文化名稱 placeholder。
* 一般概念 token 中心名詞。

### I. 排版／空格 QA

依下列項目檢查：

1. **內容型 token ↔ 中文正文外部邊界**
   * 不得殘留 Source 英文式半形空格。
   * 例如不得有 `$desc$ 如今……`。

2. **formatting/control 內部必要空格**
   * `#G 中文#!` 等不得變成 `#G中文#!`。

3. **protected token 內部空格**
   * 原樣保留普通 ASCII 空格。
   * 不得刪除、增加或改成 NBSP。

4. **多 token 名稱與中文詞組**
   * 先判斷 token 展開後是姓名片段、頭銜、中文複合詞或獨立 UI 元件，不得只看 `$...$ $...$` 外形。
   * 外國音譯姓名依完整姓名的台灣慣例決定是否使用 `·`；不得把所有 Source 姓名空格都改成音界號。
   * 採漢字姓名的漢字文化圈人物，其姓名 token 直接相連，不得插入普通空格、NBSP 或音界號。
   * 頭銜與姓名依中文語序重組；中文複合詞移除空格或補入必要中文成分。
   * 將 token 暫時代入至少一組合理展開值，確認分隔符與語序自然且不會產生重複符號。

5. **玩家可見的 UI／token-template 分隔空格**
   * 需要可見間距時，使用真正的 `U+00A0` NBSP。
   * `$ICON$ $NAME$` 應改為 `$ICON$ $NAME$`。
   * `@blue_left! $AMOUNT$` 應改為 `@blue_left! $AMOUNT$`。
   * 不得留下普通空格，也不得寫成 `&nbsp;` 或字面上的 `\u00A0`。
   * Source 原本無空格且不需要視覺間距者，不得自行新增 NBSP。

6. **換行**
   * 一般寬度溢出交由遊戲自動換行。
   * 不得為了提供換行點而保留普通空格。
   * `\n` 只用於明確的固定分行或 Source 原有換行，不得依預估寬度任意新增。

7. **清單、項目符號與指示標記**
   * `•`、行首 `-`、編號或其他確定用作清單標記的符號，與首項內容之間使用一個真正的 NBSP。
   * `• $SIZE|Y$` 應改為 `• $SIZE|Y$`，不得保留普通空格或刪除全部間距。
   * `#indent_newline:2 • Source` 中 formatting/control 所需 ASCII 空格仍須保留，只有 `•` 後改用 NBSP。
   * 正負號、內容分隔符及原本無空格的 `→$TAB$` 不得誤套本規則。
   * `\n` 後的清單標記可以保留，但標記以外的英文行首空格不得機械沿用。

8. **Token／localization reference 外側標點**
   * Token 本體保持不變，但 token 外的玩家可見英文標點必須轉為中文全形標點。
   * 特別檢查 `$...$.`、`[...].`、`#!.` 等容易被誤認為完整 protected 結構的形式。
   * 可解析 reference 時，檢查被引用譯文結尾，避免展開後形成重複句末標點。
   * 時間、小數、版本號、網址、檔名與程式語法中的半形標點不得誤改。

另檢查：

* 中文標點全形。
* 不應出現不必要全形斜線 `／`。
* 不出現中心名詞重複。
* 音界號 `·` 未因原文空格而機械濫用。

### J. 首版中文母語品質 QA

本 Batch 所有長 desc、事件敘述、歷史敘事、短文章與複雜完整句，在輸出前都必須完成此檢查。

暫時遮住英文 Source，只閱讀繁中譯文：

* 語序是否像自然中文。
* 是否有明顯英文介系詞／關係子句骨架。
* 是否名詞化過多。
* 是否「的」堆疊。
* 是否代詞重複。
* 是否資訊焦點不自然。
* 是否使用不合時代的現代術語。
* 是否為追求古典感而過度文言。
* 是否出現「文法沒錯但明顯是翻譯稿」的句子。

若有，直接修改尚未輸出的首版譯文，再回查 Source 確認沒有語意損失。

### K. 事件組整體中文品質

同一事件組的 title、desc、option、tooltip、follow-up、policy explanation 等作為同一組中文文本閱讀。

檢查：

* 文體、人稱、稱呼與術語一致。
* 上下文自然銜接。
* 沒有某句成熟、某句明顯直譯的品質落差。
* 歷史語域一致。
* 沒有大量批量翻譯造成的相同英文式句型。

---

## 二十四、完成判定

每完成一個 Batch，都必須從目前完整翻譯 key 集合重新計算真正進度。

不得使用：

`前一批累計 + 本批輸出行數`

直接推算。

必須計算：

`remaining_missing_keys = source_keys - current_translated_keys`

當所有 Batch 編號看似完成時，仍必須做：

`source_keys - final_translated_keys`

只有結果為空集合，才能宣告：

`本檔全部 Batch 已完成`

最終確認：

* `final_translated_keys` 涵蓋全部 `source_keys`。
* formatting tag 內無無合理原因殘留的漏翻外語。
* 資料型／內容型 token 結構完整。
* 語法型 placeholder 的任何數量差異均已依第十五、二十三節通過語意吸收 QA。
* 所有本次補翻 missing key 都存在於成果中。

---

## 二十五、批次進度追蹤

每完成一個 Batch，內部更新：

* 本次完成 Batch。
* 累計已完成 Batch。
* 尚未處理 Batch。
* 本次 key 範圍。
* 本次 key 數。
* 累計 missing key 完成數。
* 尚未完成 missing key 數。
* 整體進度百分比。

累計 key 進度必須依實際集合計算。

若 Batch 重拆：

* 更新完整 Batch 清單。
* 更新範圍與總批次數。
* 不得沿用失效總數。

---

## 二十六、最終回覆限制

所有 parser、glossary、研究、翻譯、token QA、格式 QA、語意 QA、歷史語境判斷、台灣繁中術語查證及首版母語品質控制仍必須完整執行。

完成一個實際翻譯 Batch 後，最終回覆只顯示：

1. 進度追蹤。
2. 本次產生的下載檔案連結。

不要在最終回覆輸出：

* 翻譯全文。
* 第二版翻譯。
* QA 報告。
* glossary 命中表。
* 語意分析。
* 中文潤稿分析。
* 研究過程。
* 專名考證過程。
* 外部資料查證過程。
* 其他補充。

所有品質控制必須在**第一次寫入輸出檔案之前**完成。

不得採：

> 先輸出較保守／較直譯版本，再另做第二輪 review 或第二版修訂

作為常規流程。

首版輸出本身即應是可直接使用的成熟翻譯。

若本次只是建立 Batch 規劃，則只回覆 Batch 規劃與進度，不產生虛假翻譯檔。

若使用者要求的是單一術語討論、譯名比較、專名考證、Prompt 討論或翻譯理由，而不是實際 Batch 翻譯，不受本節限制。

---

## 二十七、最終原則摘要

任何時候都不得以：

* 格式省事。
* Batch 編號。
* 單一 regex。
* 官方簡中字面。
* 簡體直接轉繁體。
* 未確認地區版本的中文維基頁面。
* 英文表面詞義。
* 英文表面句法。
* 英文原句資訊順序。
* glossary 單字字面命中。
* glossary 完全字串一致比對。
* 粗糙 stemming。
* 現代中文直譯。
* 原文空格直接轉成音界號。
* 「看起來差不多」。
* 「中文文法沒錯」。
* 「意思大致看得懂」。
* 「所有 token 數量一律必須機械相同」。
* 「語法型 token 都可以省略」。
* 「現代台灣人日常比較常這樣說」。

取代對：

* 完整 source key universe。
* 實際遊戲機制。
* 原文真正指涉。
* 完整事件上下文。
* 歷史文化語域。
* 原語與文化內部語境。
* glossary 語義適用性。
* glossary 詞形／詞族關係。
* 台灣既有譯名。
* 臺灣正體（zh-tw）用語。
* 資料型／內容型 token 的完整性。
* 語法型／語法關係型 placeholder 的實際語意功能。
* formatting/control 與 UI 模板的結構性空格。
* 台灣繁中母語自然度。
* 完整句子的中文資訊結構。
* 同事件組的文體一致性。
* 前現代制度與文化身分的時代適切性。

的實際判斷。

glossary 的目的不是要求正文必須與 glossary key 在英文表面形式完全一致，而是確保同一核心概念及其合理詞形／詞族變體能被辨識並一致處理。

固定 glossary 的目的也不是取代實體辨識。

最終翻譯流程必須是：

> **先確認實際語意與指涉 → 套用適用的 glossary／台灣既有譯名 → 以自然中文重構 → 保護遊戲結構 → 執行語意與 token QA → 以成熟首版輸出**

對 token 必須理解：

> **資料與內容不可因追求流暢而消失；純語法資訊若已由中文完整且無歧義吸收，也不必為了表面 token 數量一致而硬造不自然句子。**

對空格必須理解：

> **中文正文不沿用英文詞間空格；控制語法與 protected token 內部保留必要的 ASCII 空格；玩家可見且需要保留的 UI/token 分隔改用真正的 NBSP；一般溢出交由遊戲自動換行。**

最終原則：

> **忠實的是意思，不是英文句型。**

> **自然的是中文句法，不是把歷史文本現代化。**

> **歷史感來自正確的制度詞彙、文化語域與原文文體，不是刻意文言化。**

> **第一版就必須是完成品。**
