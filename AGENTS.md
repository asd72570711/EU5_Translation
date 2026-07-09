# EU5 繁體中文在地化專案

## 目標

將 Europa Universalis V 的 Paradox localization 檔案由英文翻譯為繁體中文。

## 來源與輸出

- 將 `source/english/` 視為唯讀來源資料。
- 產生的翻譯檔只能寫入 `output/traditional_chinese/`。
- 不要將 `Full/` 當作翻譯來源；它是扁平化參考資料夾，可能遺失同名檔案。
- 產生輸出時必須保留原始資料夾結構。

## Localization 編輯規則

- 不修改 localization key。
- 不修改縮排、註解、檔案結構、language header 或版本號。
- 只翻譯人類可讀的 value 文字。
- 完整保留所有 placeholder、scripted localization、variable、formatting tag、escape sequence 與 code-like token。
- 盡可能保留原始換行格式與檔案編碼。
- 保留 quote 樣式，以及 key 與 value 周圍的空白。

## 語氣與用語

- 翻譯目標為繁體中文，並以台灣用語為主。
- 避免簡體中文直轉繁體的語感。
- UI 文字應簡潔自然。
- 事件、描述與敘事文字可以較有文學感，但仍需清楚。
- 歷史名詞、國名、地名、人名、宗教名詞與制度名詞優先遵守 `translation_glossary.yml`。

## 絕對不能翻譯的 Token

範例包含：

- `[ROOT.GetCountry.GetName]`
- `[target_character.GetName]`
- `$variable$`
- `{name}`
- `%s`
- `\n`
- `<color=red>`
- `#bold`
- `#!`

## Accent / Diacritic 規則

- 對含有 accent/diacritic 的拉丁字母術語，翻譯時可將去除符號後的形式視為同一候選詞。
- 例如 `Überlingen` 與 `Uberlingen` 可視為同一候選詞。
- 若 glossary 已有明確譯名，含符號與不含符號形式原則上使用同一譯名。
- 若去除符號後可能造成歧義，必須依上下文判斷，不可硬套。
- 不要修改原文中的 key、placeholder 或 code-like token。

## 名詞、形容詞與派生詞規則

- 不要將 glossary 中的名詞譯名機械套用到形容詞、族群名、語言名或其他派生詞。
- 例如 `England` 可固定譯為「英格蘭」，但 `English` 必須依上下文譯為「英格蘭的」、「英格蘭人」、「英語」或其他自然用法。
- 例如 `Iberia` 可依語境譯為「伊比利亞」，但 `Iberian` 必須依上下文譯為「伊比利亞的」、「伊比利亞人」、「伊比利亞文化」或其他自然用法。
- 只有專案明確指定的例外才放入 `translation_glossary.yml` 的 `contextual` 區。
- 其他一般派生詞由翻譯時依上下文判斷，避免讓 glossary 過度膨脹。

## 人名規則

- 人名可在 glossary 中登錄完整姓名，並拆分 given name、surname、title 或 dynasty 等部分。
- 若文本只出現名或姓，且上下文明確指向 glossary 中的同一人物，可以使用該人物對應的部分譯名。
- 例如 glossary 若有 `Baltasar Gracián` 譯為「巴爾塔薩·格拉西安」，則上下文明確指同一人時，`Baltasar` 可譯為「巴爾塔薩」，`Gracián` 可譯為「格拉西安」。
- 若同一 given name 或 surname 可能對應多個人物，不可只因字面相同就硬套，必須依上下文判斷。
- 人名中的 accent/diacritic 也適用 Accent / Diacritic 規則。

## 人名變體規則

- 常見歐洲人名不可只依英文拼法固定翻譯，必須依人物、語言、國家、時代與上下文判斷。
- 完整人物 glossary 優先於一般 given name、surname 或 name variant 規則。
- 若只出現 given name 或 surname，只有在上下文明確指向同一人物時，才可套用該人物譯名。
- 語言或文化常見譯名只能作為候選，例如 `Charles` 可能依語境譯為「查爾斯」、「查理」、「夏爾」、「卡爾」等。
- 若無法判斷人物或語言文化來源，應標記為需人工確認，不要硬套。

## 術語表

- 固定術語以 `translation_glossary.yml` 為準。
- 如果 glossary term 出現在人類可讀文字中，必須一致使用術語表翻譯。
- 不要在 protected token 或 code-like fragment 裡套用術語替換。

## 新術語確認規則

- 翻譯時若遇到未收錄於 `translation_glossary.yml` 的專有名詞、國名、地名、人名、宗教名、文化名、制度名或遊戲術語，應優先標記並向使用者確認。
- 經確認後，將固定譯名加入 `translation_glossary.yml`。
- 高頻 UI term 與 mechanic term 應優先加入 glossary，確保全專案一致。
- 不確定的術語不要自行定案；可先在報告中列為 `needs_glossary_review`。

## 工作流程

- 批量處理優先使用 Python script，不要手動大量修改檔案。
- 寫入翻譯檔前，先使用 dry-run/report mode。
- 翻譯前後必須驗證 key 與 protected token 是否一致。
- 每次批量產生結果後，都要檢查 `git diff`。
