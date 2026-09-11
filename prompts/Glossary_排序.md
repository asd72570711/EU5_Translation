# Glossary 排序

## EU5 Glossary 純排序

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
