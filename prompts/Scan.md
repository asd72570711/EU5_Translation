# Scan

請掃描：
main_menu\localization\english\events\DHE\flavor_[def]*_l_english.yml

路徑使用標準 glob 語法：

- `*` 表示任意長度的字串
- `?` 表示單一字元
- `[abc]` 表示符合其中一個字元
- 不要使用正規表示式的 `^` 作為檔名模式的一部分

掃描前先確認實際命中的來源檔案清單。
若沒有命中任何檔案，應先回報並停止，不要寫入 review.json。
只允許掃描 `source/english/` 下指定的來源檔案，不要掃描 `Full/`。


先比對 translation_glossary.yml，將尚未收錄的專有名詞、宗教概念、神祇稱號、人物、作品名、制度名與可重複使用術語整理到：

work/glossary_review/review.json

請不要修改來源檔、不要修改 glossary，也不要翻譯內容。
已有 glossary 的詞不要列入 review。
已列在根目錄 `glossary_drop_terms.yml` 的完整 term 也不要列入 review；例如清單中的 `Edict` 不應排除 `Edict of Worms`。
請保留上下文與 glossary_refs。
