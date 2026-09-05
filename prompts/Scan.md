# Scan

請掃描：
main_menu\localization\english\events\DHE\flavor_[ghijkl]*_l_english.yml

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
阿拉伯語人名應優先保留完整姓名鏈，不要從完整姓名中拆出 `al-`、`ibn`、`bin`、`bint`、`Abu`、`Umm` 等片段；例如 `Abu al-Qasim al-Zahrawi` 應作為一個完整候選。只有片段在其他上下文中獨立成為明確的人名或術語時，才另外保留。
引號或 `#italic ...#!` 包住的完整作品名、書名、畫作名或其他正式名稱，應優先視為單一術語，不要拆出其中的前綴或子片段；例如 `'De Jure Belli ac Pacis'` 應只保留完整名稱。只有子片段在來源中另行獨立出現時，才另外判斷。
請保留上下文與 glossary_refs。
