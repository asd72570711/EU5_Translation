# EU5 繁體中文在地化專案

## 目標

將 Europa Universalis V 的 Paradox localization 檔案由英文翻譯為繁體中文。

## 來源與輸出

- 將 `source/english/` 視為唯讀來源資料。
- 產生的翻譯檔只能寫入 `output/traditional_chinese/`。
- 不要將 `Full/` 當作翻譯來源；它是扁平化參考資料夾，可能遺失同名檔案。
- 產生輸出時必須保留原始資料夾結構。
- 遊戲實際使用輸出目標為覆蓋官方簡中 localization：輸出檔名 suffix 應由 `_l_english.yml` 改為 `_l_simp_chinese.yml`，language header 應由 `l_english:` 改為 `l_simp_chinese:`，路徑中的語言資料夾 `english/` 也應改為 `simp_chinese/`。

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
- key 以 `.title` 或 `_title` 結尾時，value 應翻譯為簡潔的標題形式；不可自行加入「有人」等敘事主語或完整敘事句。即使原文是事件描述，也要依 key 的標題用途調整為標題，例如 `d008_orthodox_events.13.title` 應使用「宣稱大分裂已彌合」這類標題式譯法。
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

## Placeholder 與中文排版

- 不要在 placeholder、variable、數字 token 與中文單位之間自動加入空格。
- 若遊戲 UI 可能因空格造成不必要換行，應將中文文字與 token 貼合。
- 例如日期應使用 `西元$YEAR$`、`西元前$YEAR$`、`$YEAR$年$MONTH$$DAY$日`，不要寫成 `西元 $YEAR$ 年` 或 `$YEAR$ 年 $MONTH$ $DAY$ 日`。
- 只有在原文格式、遊戲語法或可讀性明確需要空格時，才保留或加入空格。
- placeholder 可依中文語序調整位置，但不可增減或改寫；驗證時應確認同一組 token 都完整保留。
- 不要刪除 formatting tag 內部的必要空格，例如 `#G +100#!` 應保留為 `#G +100#!`，不要改成 `#G+100#!`。
- `#G`、`#R`、`#Y`、`#bold`、`#!` 等 formatting token 及其周圍語法應原樣保留，除非已確認遊戲語法允許修改。
- `$...$` placeholder、comparator、數值或變數作為中文句子成分時，前後原則上不主動加空格，例如 `西元$YEAR$`、`$VAL|Y$次`、`目前$CURRENT|V$項`。
- `#tag` 類 formatting 開始標記後面通常保留一個語法空格，因為它與後方內容共同構成 formatting span，例如 `#variable $AMOUNT$#!`、`#G +100#!`、`#italic $TEXT$#!`。
- `#!` 是 formatting closing tag，後面是否留空白依中文語句決定；若後面直接接中文文字或單位，通常不留空白，例如 `#variable $AMOUNT$#!項`。
- 中文句子中若 placeholder、comparator 或 formatting span 是句子成分，原則上不要在 token 外側另外加空格，例如使用 `有$COMPARATOR$#variable $AMOUNT$#!項`，不要寫成 `有 $COMPARATOR$ #variable $AMOUNT$#! 項`。
- 英文 code-like term、script key 或 debug term 嵌入中文句子時，前後原則上不主動加空格，以避免 UI 換行，例如 `trigger_if不可用於未求值的context`、`請改用custom_description或custom_tooltip`。
- 技術欄位名稱 `id` 在一般可翻譯文字中統一寫為大寫 `ID`；但原始 API、script key 或 placeholder 的大小寫必須原樣保留，例如 `modId`、`activationSetId` 與 `$ID$`。
- 相鄰的 placeholder、script token 或數值 token 若以斜線等標點連接，標點兩側原則上不保留多餘空格，例如 `[A]/[B]`，不要寫成 `[A] / [B]`；除非原文語法或 UI 可讀性明確要求留空格。
- 非遊戲語法、非 protected token 的一般標點應使用中文全形標點；例如普通括號使用 `（$NAME$）`，不要寫成 `($NAME$)`。若括號屬於格式標記、狀態符號或原文特殊語法，才保留原樣。
- 複合地名、人名片段或 UI 連接符若需要避免換行，可使用不斷行連字號 `‑`；若連字號前後需要空白，可使用不斷行空格以避免 UI 在符號兩側斷行。
- 英文 dash 作為分類與標題之間的中文分隔符時，使用中文破折號 `——`，例如 `拜占庭——聖歌旋律`；年份範圍、複合人名或需要避免斷行的連接符仍可使用不斷行連字號 `‑`。

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
- 遊戲術語、機制名、UI 系統名與可重複出現的專案用語，放入 `translation_glossary.yml` 的 `game_terms` 區。
- 如果 glossary term 出現在人類可讀文字中，必須一致使用術語表翻譯。
- 不要在 protected token 或 code-like fragment 裡套用術語替換。
- 大寫開頭且看起來像系統名、單位名、勢力名、機制名、品牌名、平台服務名或 UI term 的詞，不要直接當普通名詞處理；若尚未收錄，應先列為遊戲術語候選並向使用者確認。
- 已確認且不需要特殊審查的遊戲術語，只需加入 glossary，不需要另外寫入 `translation_notes.md`。

## 新術語確認規則

- 翻譯時若遇到未收錄於 `translation_glossary.yml` 的專有名詞、國名、地名、人名、宗教名、文化名、制度名或遊戲術語，應優先標記並向使用者確認。
- 經確認後，將固定譯名加入 `translation_glossary.yml`。
- 高頻 UI term 與 mechanic term 應優先加入 glossary，確保全專案一致。
- 不確定的術語不要自行定案；可先在報告中列為 `needs_glossary_review`。
- AI 預審 review 候選時，應將明顯不是固定遊戲術語、專有名詞、歷史名詞、人名、地名、制度名或可重複使用術語的項目標為 `skip`，但不得直接刪除 review 項目。
- 一次性的事件標題或一般敘事標題，即使採 Title Case，只要不是歷史事件、作品名、制度、神祇、宗教概念或遊戲機制，就應標為 `skip`；有疑義時保留候選，不要硬設為 `skip`。
- 翻譯含有歷史引文、事件、書名、人名或地名的檔案前，應先掃描並列出疑似專有名詞候選，不要直接整檔翻譯。
- 疑似專有名詞候選包含連續 Title Case 詞組、人名格式、`X of Y` / `X de Y` / `X von Y` 類型詞組、引號或斜體中的作品名，以及事件、會議、條約、戰役、頭銜與組織名。
- 例如 `Diet of Worms`、`Order of the Garter`、`Battle of Pavia`、`The Wealth of Nations` 這類詞組若尚未收錄，必須先列為 `needs_glossary_review` 或向使用者確認譯名。
- 術語掃描時應先比對既有 `translation_glossary.yml`；已收錄的 term 不放入 review。
- 未收錄的候選 term 可寫入固定臨時檔 `work/glossary_review/review.json`，讓使用者手動填入 `translation`。
- `review.json` 中的候選項應盡量附上 `glossary_refs`，列出既有 glossary 中可能相關的完整詞組或部分詞組，供使用者避免譯名不一致。
- `review.json` 的 `status` 使用短值：`todo` 表示等待使用者填寫 `translation`，`ai` 表示請 Codex 先把建議譯名填回 `review.json` 供使用者檢查，`skip` 表示忽略且不收錄。
- `review.json` 的 `status: cont` 表示使用者已填入核心譯名，但該 term 需依語境採用不同譯法。處理 `cont` 時，Codex 必須讀取來源 key 與上下文，提出或建立 `translation_glossary.yml` 的 `contextual` 規則；不可機械匯入為 `fixed`。
- `cont` 項目的 `translation` 是使用者確認的核心用法，不一定是 contextual 的 default。Codex 應依來源用例判斷 default 與其他 senses，並在寫入前先提供草案供使用者確認。
- review 項目的 `note` 是長期翻譯理由。匯入 fixed 或 contextual glossary 時，應以 term 上方的 YAML 註解保留 note。
- 當使用者要求進行 review 確認與 ai 建議時，應先以 `scripts/import_glossary_review.py --resolved-only --write` 匯入已填譯名的 `todo`，並從 review 移除這些項目與所有 `skip`。`ai` 與 `cont` 項目必須保留，供後續建議或 contextual 草案處理。
- `ai` 不應直接跳過使用者檢查匯入 glossary；Codex 只先補上 `translation`，使用者保留或修改該譯名後，才進行 glossary 匯入。
- 若 review term 與既有 glossary term 疑似為名詞、形容詞、族群名或語言名等派生關係，且使用者填入譯名與既有中文譯名相同或高度相關，應優先建立或調整 `contextual` 條目，而不是直接加入 `fixed`。
- 例如 `Catalonia` 已固定為「加泰隆尼亞」時，`Catalan` 若使用者也填「加泰隆尼亞」，應視上下文建立 `Catalan` 的 contextual 規則，區分「加泰隆尼亞的」、「加泰隆尼亞人」、「加泰隆尼亞語」等用法。
- `review.json` 完成匯入 `translation_glossary.yml` 後即可刪除，不作為長期紀錄；長期固定譯名以 `translation_glossary.yml` 為準。
- 使用者確認譯名後，若屬於會重複出現的固定名詞，應加入 `translation_glossary.yml`；若只是單檔特殊判斷，才寫入 `translation_notes.md`。

## 工作流程

- 批量處理優先使用 Python script，不要手動大量修改檔案。
- PowerShell 只作為腳本啟動器；不要用 PowerShell here-string、`python -c` 或命令列字串直接承載大量中文、`$...$` placeholder、撇號姓名或其他 localization 內容。
- 複雜文字處理應寫入 `.py` 腳本後以簡單參數呼叫，例如 `python scripts\scan_glossary_candidates.py --file ...`。
- 手動修改文字檔優先使用 `apply_patch`，避免 PowerShell 對 UTF-8、`$`、引號或撇號做額外解析。
- Python 腳本原始碼盡量保持 ASCII；若需要非 ASCII 字元範圍或特殊標點，優先使用 `\uXXXX` escape。中文譯文與資料應保存在 JSON/YML/MD 資料檔中。
- 寫入翻譯檔前，先使用 dry-run/report mode。
- 對大型檔案或含大量專有名詞的檔案，翻譯前先產生術語候選報告，確認後再分批翻譯。
- 翻譯前後必須驗證 key 與 protected token 是否一致。
- 產生 YAML 前，必須用 `scripts/check_translation_glossary.py` 比對來源詞條、工作 JSON 與最新 `translation_glossary.yml`；若發現 glossary 譯名未出現在對應翻譯中，先修正工作 JSON，不得直接產生輸出。
- 產生 YAML 前應執行 `scripts/check_translation_style.py`，檢查中文與英文、數字、placeholder 或 code-like token 之間的多餘空格，以及半形括號等排版問題。
- 若風格檢查失敗，不得寫入輸出 YAML；應先修正 translation JSON，再重新執行 glossary 與 style 檢查。
- 每次批量產生結果後，都要檢查 `git diff`。
