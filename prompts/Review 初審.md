# Review 初審

請對 work/glossary_review/review.json 做 AI 預審。

請以 AI 語意與語法判斷執行預審。
不要依賴固定動詞清單，也不要要求事先列出所有可能的動詞。

本次語意與詞性判斷必須由 AI 完成。
scripts/prescreen_glossary_review.py 不得作為語意分類依據，
也不要使用會自行修改 status 的 `--write` 模式。

直接檢查並更新：

work/glossary_review/review.json

## 一、預審範圍

請檢查所有現有 status: todo 與 status: cont 的項目。

已有 status: skip 的項目不要重新判斷或修改。

已有 status: drop 的項目不要重新判斷或修改；它們會由「Review 審查」加入永久排除清單。

若使用者確認某個完整 term 永久不需要加入 glossary，可將該項目的 status 手動改為 `drop`；
不要填寫 translation，也不要直接刪除該項目。

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

## 一之一、必要時查閱來源上下文

先使用 review.json 已提供的 term、source key 與上下文判斷。
若上下文不足，或 term 可能同時是普通用語與固定術語，
請依 source_file 到 source/english/ 搜尋該 term，
只讀取命中行及前後短片段，不要讀取或輸出完整來源檔。

若在來源片段中發現尚未收錄的人名、地名、組織名、制度名、
宗教概念、作品名、歷史名詞或可重複使用術語，
應新增獨立 review 項目，使用 status: todo，
保留原始 key、上下文與 glossary_refs，且 translation 保持空白。

不得因掃描器原本沒有建立候選，就直接認定來源中沒有需要收錄的術語。
若需要執行來源掃描，先確認實際命中的檔案清單；
若指定路徑沒有命中檔案，應先回報並停止，不得寫入 review.json。
不得掃描 Full/ 或其他非指定來源目錄，
review.json 的 source_file 只記錄實際成功掃描的來源檔案。

## 二、標記為 skip 的項目

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

### 一般單字判斷

請依完整上下文判斷，不要因為 Title Case 或大寫開頭就保留候選。

若單獨出現的詞只是一般語言，且不是專有名詞、歷史名詞、固定遊戲機制或正式 UI term，應標記為 `skip`，包括：

- 一般副詞：Historically、Recently、Currently、Eventually、Originally、Then、There、Thus
- 一般名詞：History、Services、Actions、Benefits、Response、Treatment
- 一般動詞及其高信心的時態、分詞或第三人稱變化：Hire、Hired、Hiring、Hires、Recall 等
- 一般形容詞及其普通派生形式：Setting、Sellout 等

例如：

- `Historically` → `skip`
- `History` → 通常 `skip`；只有明確指向固定 UI、遊戲機制或正式系統名稱時才保留
- `Services` → 通常 `skip`；只有明確是固定遊戲制度或 UI term 時才保留
- `Hire`、`Hired` → 通常 `skip`；只有明確是固定職位、招募機制或正式 UI term 時才保留

不要建立龐大的固定排除清單，應由 AI 根據詞性、上下文、source key 與是否具備可重複使用價值判斷。

若無法確定是否為固定術語，則保留 `todo` 或 `cont`，不要自行標記為 `skip`。

## 三、動詞片語與結果狀態片語

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

介系詞、連接詞或時間副詞開頭的普通敘事片段，若沒有形成正式名稱或固定術語，也應標記為 `skip`。
例如 `After Maximilian` 若只是上下文中的時間片段，應標記為 `skip`；
但 `After the Battle of Ukmergė` 若指向歷史事件，則保留歷史事件或拆出其中的專有名詞。

`Adopted Nordic Culture` 這類完整的 V+N 或結果描述片語應標記為 `skip`；
只有其中另含明確且可獨立重複使用的專有名詞、制度名或固定遊戲術語時，才依專有名詞拆分規則另行保留子詞條。

完整片語不需要作為 glossary 詞條固定收錄，
交由翻譯 AI 根據完整上下文翻譯。

固定遊戲機制或正式 UI term 的單一 term 可以保留，
但完整 V+N、N+V 或結果狀態片語仍依本節標記為 skip。

## 四、必須保留的項目

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

頭銜加姓名、全大寫縮寫與小寫語言粒子開頭的名稱，
不要因格式特殊或詞很短就標記為 skip。
例如 `Sultan Suleiman` 可分別檢查完整人物名、`Suleiman` 與 `Sultan`；
`al-Andalus`、`ibn Khaldun`、`de Medici` 等也應視為可能的完整專有名詞。
`HRE`、`MING`、`EU4` 等縮寫則應依上下文判斷是否為組織、政體、文化或遊戲術語。

## 五、一次性標題與敘事中的專有名詞

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

## 六、完整敘事句與普通敘事

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

## 七、按鈕與教學指示

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

## 八、cont 項目規則

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

## 八之一、既有 glossary 詞形變化

### 既有姓名加頭銜

若完整候選只是「一般頭銜／職稱 + 已收錄的完整人名或專名」，
且上下文中的頭銜只是描述身分，不是名稱本身的一部分，應標記為 `skip`。
例如 glossary 已有 `Ferdinand III` 時，`Emperor Ferdinand III` 應標記為 `skip`。
只有移除頭銜後與既有 glossary term 完全吻合時才適用；
若頭銜是正式名稱的一部分、用來區分不同人物，或完整詞組本身是獨立歷史名稱，
則保留給 AI 判斷，不得僅因包含既有姓名就跳過。

若 todo 或 cont 項目只是 translation_glossary.yml 已有 term 的高信心詞形變化，
且不需要不同的中文譯法，應標記為 status: skip，交由 Review 審查移除。
這類項目不要加入 drop 清單，也不要修改 translation。

請優先檢查：

- 規則複數：`-s`、`-es`
- `子音+y` 變為 `-ies`，例如 `Country` → `Countries`
- 所有格：`'s`、`s'`
- 複合詞中任一詞的上述詞形變化，例如 `Sofa Levy` → `Sofa Levies`
- 高信心的不規則複數，例如 `Person` → `People`
- 部分高信心的拉丁或希臘複數，例如 `Bishopric` → `Bishoprics`
- 明確只是大小寫、重音符號、連字號或空格差異的同一 term
- 只有句尾標點或多餘空白差異的同一 term，例如 `Corsica.` → `Corsica`

例如 glossary 已有 `Huguenot`，候選 `Huguenots` 若上下文只是該術語的複數，
應標記為 `skip`，不必再次建立 glossary 詞條。

若 glossary 已有基本 term，且候選只是該 term 的高信心詞形變化、
不需要新的中文翻譯決策，也應標記為 `skip`。例如：

- `Ottoman` → `Ottomans`
- `Huguenot` → `Huguenots`
- `Akritai` → `Akritais`
- `Bishopric` → `Bishoprics`
- `Road` → `Roads`
- `Country` → `Countries`
- `Person` → `People`
- `Hire` → `Hired`、`Hiring`

上述規則也適用於複合詞中任一詞的詞形變化。
但 `Ottoman Empire`、`Ottoman Turks` 等完整複合詞不可只因含有 `Ottoman` 就排除；
只有完整 term 本身確認只是既有詞條的詞形變化時，才可標記為 `skip`。

上述判斷必須依 term、source key 與上下文確認，不得只依字尾機械分類。
例如 `Worms` 可能是 `Worm` 的複數，也可能是地名；無法確認時應保留原本的 todo 或 cont。

若候選 term 去除句尾的 `.`, `,`, `;`, `:`, `!`, `?` 與多餘空白後，
與既有 glossary term 完全相同，且標點不是名稱本身的一部分，
應標記為 `skip`。不得修改 review 中原本保留的 term。

例如 `Corsica.`、`Tsushima.`、`Vienna.` 應分別視為既有
`Corsica`、`Tsushima`、`Vienna` 的表面標點差異。
但 `St. Louis`、`U.S.` 等標點屬於名稱本身，或去除標點後可能造成歧義時，
應保留給 AI 判斷。

以下通常不是可直接跳過的詞形變化，應保留給 AI 或 glossary 判斷：

- 國名與形容詞、居民或語言派生，例如 `Germany` → `German`、`Italy` → `Italian`
- `-ian`、`-an`、`-ese`、`-ish`、`-ic`、`-al` 等語意派生
- `-ism` 與 `-ist`
- `-ed`、`-ing` 等可能改變詞性或語意的形式；只有已確認是單純詞形變化、且不需要新中文決策時，才可依上述規則標記為 `skip`

## 八之二、skip 二次複核

完成第一輪分類後，對所有準備標記為 skip 的項目再複核一次。
優先複核短詞、只出現一次的詞、Title Case 詞、縮寫、頭銜、
含重音符號的詞，以及可能是人名或地名的項目。

若複核時發現它可能是人名、地名、組織名、制度名、歷史名詞、
宗教概念、作品名、頭銜、正式 UI term 或固定遊戲術語，
不得標記為 skip；無法確定時保留原本的 todo 或 cont。

只有確認為普通用語、一般敘事、操作指示或一次性描述，
且沒有獨立的專有名詞或固定術語意義時，才可維持 skip。

## 九、保留疑義項目

無法確定是否為固定術語、專有名詞、
歷史名詞或可重複使用術語時：

- todo 項目保留 status: todo
- cont 項目保留 status: cont
- 不要填寫或修改 translation
- 不要自行加入 translation_glossary.yml
- 不要修改來源檔
- 不要修改 term、keys、note 或上下文
- 保留既有 glossary_refs

若 term 可能是專有名詞、歷史名詞、制度名、宗教概念、
固定遊戲術語或正式 UI term，即使只出現一次、很短、採普通單字形式，
也不要因為不確定而標記為 skip；應保留 todo 或 cont。

只有在確認它是普通用語、一般敘事、操作指示或一次性描述，
且沒有獨立的專有名詞或固定術語意義時，才標記為 skip。

## 十、檔案限制

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

## 十一、完成後驗證

完成 AI 判斷並更新 review.json 後，
只能使用下列腳本驗證 JSON 結構與欄位完整性：

```powershell
python scripts/prescreen_glossary_review.py --review work/glossary_review/review.json
```

這個腳本只做結構驗證，不會進行語意分類或寫入檔案。
不得使用 `--write`，也不得執行其他會依固定規則修改 status 的命令：

```powershell
python scripts/prescreen_glossary_review.py --write
```

初審時必須逐一檢查所有 status: todo 與 status: cont，
不可只依賴固定單字清單。像 Then、There 這類單獨普通功能詞，
若上下文沒有專有名詞或固定術語意義，應標記為 skip；
若屬於專有名詞或固定片語的一部分，則保留。

驗證完成後回報：

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
