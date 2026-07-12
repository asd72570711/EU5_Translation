# 翻譯備忘錄

這份文件只記錄少量需要人工留意的特殊詞條或檔案位置。

## 特殊詞條

- `name_frederick.german_language`：譯為「腓特烈」。

## 人名特殊處理

- `Georgia` 作人名時譯為「喬治婭」。
- 需留意以下詞條：
  - `main_menu/localization/simp_chinese/character_names_l_english.yml` 的 `Georgia:`
  - `main_menu/localization/simp_chinese/character_names_dynamic_l_english.yml` 的 `name_georgia.greek_language:`

## 格式與 UI 特殊處理

- `loading_screen/localization/clausewitz/text_utils/cw_text_utils_l_english.yml` 的 `AND_LIST` 原文為 `", and "`，繁中試譯採用「，以及」而非直譯逗號加「和」，用於清單最後一項前的正式連接。
- 同檔的 `COMMA` 原文為 `", "`，繁中試譯先採用全形逗號「，」而非頓號「、」，讓一般清單與英文逗號語氣較接近；若日後遊戲內清單顯示過密或不自然，再回頭審查。
- `main_menu/localization/jomini/credits/credits_l_english.yml` 的 `CREDITS_SLOWER` / `CREDITS_FASTER` 採用「減緩」/「加快」，以按鈕動作語氣處理，而非狀態形容「較慢」/「較快」。
- `loading_screen/localization/jomini/ticktask_debugger_l_english.yml` 的 `JOMINI_TICKTASK_PRIO_EARLY` / `JOMINI_TICKTASK_PRIO_LATE` 目前暫譯為「早期」/「晚期」；官方中文似為「優先」/「推後」，但因缺少實際 UI 前後文，需待實機或更多語境確認。
- 同檔的 `JOMINI_TICKTASK_TIMES_EXECUTED_HEADER` 原文為 `## executions`，`##` 含義未確認；目前先保留為 `## 執行次數`，待實機畫面確認是否可移除或改寫。
