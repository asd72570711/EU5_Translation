# EU5 Translation

Europa Universalis V 繁體中文在地化與翻譯工具專案。

本專案用於管理英文 localization 來源檔、繁體中文翻譯輸出、術語表與翻譯品質檢查，並提供掃描 glossary 候選、審查 review 項目及驗證輸出的 Python 工具。

作者：YA_OAO

## 專案結構

- `source/english/`：官方英文 localization 來源，唯讀，不直接修改。
- `output/traditional_chinese/`：繁體中文 localization 輸出，保留原始資料夾結構。
- `scripts/`：掃描、翻譯、Glossary 匯入與驗證工具。
- `translation_glossary.yml`：專案術語表，包含 `fixed`、`aliases`、`contextual` 與 `reference_terms`。
- `work/glossary_review/review.json`：尚待確認或處理的 glossary 候選項目。
- `translation_notes.md`：翻譯決策與專案備註。
- `Full/`：扁平化參考資料，不作為翻譯來源。

## 開始使用

請從專案根目錄執行指令。需要 Python 3.10 或更新版本。

## 建議工作流程

### 1. 掃描來源檔

將要處理的英文 localization 檔案列在 `Scan → Review` 指令中，並提供來源檔路徑。例如：

```text
請掃描：
main_menu/localization/english/game_concepts_l_english.yml
main_menu/localization/english/interfaces_l_english.yml
```

Codex 會先比對 `translation_glossary.yml`，再將尚未收錄且具有專有名詞、制度名、宗教概念或可重複使用術語價值的候選項目整理到 `work/glossary_review/review.json`。已有 glossary 的詞條不應重複加入。

### 2. Review 初審

對 `review.json` 執行「Review 初審」Prompt，由 AI 根據完整 term、source key 與上下文篩選候選項目：

- 明顯不需要固定收錄的普通片語、操作指示或一次性敘事，標記為 `skip`。
- 人名、地名、制度名、宗教概念、固定遊戲術語等候選保留。
- 不確定的項目不要自行刪除或翻譯。

初審只負責分類，不代表已經確認中文譯名。

### 3. Review 審查

初審後執行「Review 審查」，移除已標記為 `skip` 的項目，並更新仍保留項目的 `glossary_refs`。這一步也可在後續術語確認期間視需要重複執行，以減少 review 檔案內容。

### 4. 確認 review 術語

逐項確認 `review.json` 中的 `todo`、`ai` 與 `cont`：

- `todo`：填寫並確認中文譯名。
- `ai`：先檢查 AI 建議，再決定是否採用。
- `cont`：依 source key 與上下文判斷應使用 `fixed`、`contextual`，或繼續保留待確認。
- 使用者也可以將不需要加入 glossary 的項目標記為 `skip`，再於後續「Review 審查」中移除。

確認期間若需要調整候選、補充上下文或清理已處理項目，可以再次執行「Review 審查」。尚未確認的項目不要匯入 glossary。

### 5. Glossary 整理

當 review 術語都完成確認後，對 `translation_glossary.yml` 執行「Glossary 整理」：

- 檢查 `fixed`、`aliases`、`contextual` 與 `reference_terms` 的分類。
- 清理純單複數、時態或其他一般詞形造成的重複條目。
- 檢查 aliases、contextual 與 reference terms 是否真的符合用途。
- 檢查重複 key、衝突譯名與完整詞組優先規則。

整理時不要同時重新排序，避免結構整理與版面排序混在一起。

### 6. Glossary 排序

若需要統一條目順序，再另外執行「Glossary 排序」。這是獨立步驟，只有明確需要時才執行。

### 7. 翻譯 localization

準備好最新的 `translation_glossary.yml` 後，將 glossary 與要翻譯的英文 source files 一起提供給 ChatGPT，並使用「ChatGPT 翻譯」Prompt。

翻譯時應：

- 使用最新版本的 glossary。
- 保留 localization key、placeholder、formatting tag、script token 與檔案結構。
- 依完整上下文翻譯，不要機械套用普通 reference term。
- 完成後檢查 key、protected token、YAML 格式與翻譯檔差異。

完成一批檔案後，對其他 source files 重複上述流程即可。

### 掃描 Glossary 候選

使用 `--file` 指定要掃描的英文來源檔；需要時可以重複指定多個檔案。

```powershell
python scripts\scan_glossary_candidates.py `
  --file source\english\main_menu\localization\english\game_concepts_l_english.yml `
  --write-review
```

掃描前會先比對既有 `translation_glossary.yml`，已收錄的詞條不應重複加入 review。

### 審查與匯入 Glossary

`work/glossary_review/review.json` 中的 `todo` 項目等待確認譯名，`cont` 項目表示核心譯名已填寫但可能需要依語境分流，`ai` 項目則需要使用者確認 AI 建議。

預審腳本可協助檢查 review 的欄位與資料完整性；語意分類仍應依完整上下文判斷：

```powershell
python scripts\prescreen_glossary_review.py `
  --review work\glossary_review\review.json `
  --existing-only `
  --write
```

只匯入已確認的項目：

```powershell
python scripts\import_glossary_review.py `
  --review work\glossary_review\review.json `
  --glossary translation_glossary.yml `
  --resolved-only `
  --write
```

只有在 `cont` 已完成語境判斷後，才使用 `--include-cont`。尚未確認的 `todo`、`ai` 與 `cont` 不應自行匯入。

### 檢查結果

```powershell
python scripts\check_glossary_review.py `
  --review work\glossary_review\review.json

python scripts\report_glossary_structure.py
```

若需要處理 glossary refs，可使用：

```powershell
python scripts\update_review_glossary_refs.py `
  --review work\glossary_review\review.json `
  --glossary translation_glossary.yml `
  --write
```

## 翻譯原則

- 不修改 `source/english/` 下的來源檔；翻譯輸出寫入 `output/traditional_chinese/`。
- 保留 localization key、placeholder、formatting tag、script token 與原始檔案結構。
- 完整詞組優先於其中的單字，`reference_terms` 只提供參考，不是強制翻譯規則。
- `fixed`、`aliases` 與 `contextual` 的整理應以翻譯決策與實際語境為依據，不要只為一般單複數或時態變化建立重複詞條。
- Glossary 字母排序是獨立工作；除非明確要求，整理 glossary 時不應重新排序。
- 產生或修改輸出後，應檢查 key、protected token 與格式是否仍與來源一致。

## 授權

本專案中由 YA_OAO 創作的原創腳本、工具與文件採用 MIT License，詳見 [LICENSE](LICENSE)。

遊戲官方檔案、遊戲資產及其衍生的在地化內容不包含在上述原創內容授權範圍內，相關權利與使用條款仍以其各自權利人為準。
