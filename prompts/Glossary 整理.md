# Glossary 整理

請對整份 `translation_glossary.yml` 做完整結構檢查與整理。

不要只檢查最近新增的條目，請檢查整份 glossary。
只修改 `translation_glossary.yml`，不要修改 `source/english/` 下的來源檔或任何翻譯檔。

本次整理只處理 glossary 的結構、語意、冗餘與分類問題。
**不要執行字母排序。**
排序將由另一個獨立 Prompt 處理。

## 一、Aliases 檢查

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

## 二、Contextual 檢查

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

## 三、Reference Terms 檢查

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

## 四、完整片語優先規則

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

## 五、衝突與一致性檢查

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

## 六、排序與版面保護

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

## 七、修改與套用規則

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

## 八、修改前回報

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

## 九、驗證

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
