# Review 審查

請檢查並處理這份 review.json：

work/glossary_review/review.json

## 一、處理範圍

只對以下項目進行語意判斷與匯入處理：

- status: cont
- status: todo
- status: ai

已有 status: skip 的項目不要重新判斷，也不要修改其 term、translation、status、keys、note 或上下文。

status: skip 項目只允許在「glossary_refs 更新」階段更新 refs，不得重新分類或翻譯。

`status: drop` 表示使用者已確認該完整 term 永久排除。不要翻譯、不要加入 glossary，
只在本次審查中將它加入根目錄的 `glossary_drop_terms.yml`，再從 review 移除。
`drop` 不等同於 `skip`：`skip` 只代表本次審查略過，`drop` 則會影響未來掃描。

## 二、cont 處理

處理 cont 時：

1. 先讀取 review 提供的 source key、英文上下文與既有 translation。
2. 只有在 term 可能有多重詞義、普通用法與遊戲術語可能混淆，或可能與其他遊戲機制產生不同譯法時，才搜尋 source/english/ 下該 term 的其他用法。
3. 搜尋時只讀取命中行及前後短片段，不要讀取或輸出完整檔案。

請根據實際語境判斷：

- 所有用法都能使用同一譯名：匯入 fixed。
- 不同語境需要不同譯法：建立 contextual。
- 無法確定：保留 cont，不要匯入 glossary。

不要因為 status: cont 就一律建立 contextual。

完成後列出所有 cont 的：

- 判定結果
- 譯名
- 匯入 fixed 或 contextual 的理由
- 仍保留 cont 的原因

## 三、todo 與 ai 處理

- 已填寫且已確認的 todo，匯入 fixed 或 contextual。
- ai 項目只有在使用者確認 translation 後，才能匯入 glossary。
- 尚未確認的 todo 或 ai 必須保留。
- 不要自行填寫或修改尚未確認項目的 translation。
- 匯入 contextual 時，保留 review note 作為 glossary 註解。

## 四、review 清理

glossary_refs 更新並成功完成後：

- 移除已匯入的 todo。
- 移除已確認並匯入的 ai。
- 移除 skip。
- 將 `status: drop` 的完整 term 加入 `glossary_drop_terms.yml` 後移除。
- 保留尚未確認的 todo、ai 與 cont。
- 不要因為更新 glossary_refs 而刪除尚未確認的項目。

## 四之一、來源覆蓋率檢查

在移除 `skip` 前，必須先執行來源覆蓋率檢查：

```powershell
python scripts/audit_glossary_review_coverage.py --review work/glossary_review/review.json --glossary translation_glossary.yml --source-root source/english --write-report
```

此腳本會使用 `review.json` 的 `source_file` 清單，重新掃描實際來源檔，
並將候選與 `translation_glossary.yml` 及目前 review 項目比對，
報告可能完全漏收的候選至：

```text
work/glossary_review/coverage_audit.json
```

腳本只產生報告，不會修改 `review.json`、glossary、來源檔或翻譯檔。

請先檢查報告中的 `high` 信心候選：

- 若確認是應保留的專有名詞、制度名、宗教概念、人物、作品名或可重複使用術語，
  讀取來源檔命中行及前後短片段，新增獨立 `todo` review 項目。
- 新增項目必須保留來源 key、短上下文與可取得的 `glossary_refs`，
  `translation` 保持空白，不得直接匯入 glossary。
- 若確認只是一般語言或一次性片語，才可在報告處理後標記為 `skip`。
- `normal` 信心候選需依上下文判斷；無法確定時保留在 review，不能直接刪除。
- 處理報告候選後可重新執行覆蓋率檢查，確認新增項目已被 review 覆蓋。

不要因為候選只出現一次、位於句首、含縮寫、頭銜、重音符號或小寫姓名片段，
就直接判定為漏收或 `skip`。

## 五、glossary_refs 更新

所有已確認項目完成匯入 translation_glossary.yml 後，
必須先使用最新的 translation_glossary.yml 更新 review.json，
再進行 review 清理。

必須實際執行以下腳本，不得只在回覆中描述「已更新 refs」：

```powershell
python scripts/import_glossary_review.py --review work/glossary_review/review.json --glossary translation_glossary.yml --drop-terms glossary_drop_terms.yml --resolved-only --include-cont --keep-review --write

python scripts/update_review_glossary_refs.py --review work/glossary_review/review.json --glossary translation_glossary.yml --max-refs 12 --core-max-refs 3 --write

python scripts/import_glossary_review.py --review work/glossary_review/review.json --glossary translation_glossary.yml --drop-terms glossary_drop_terms.yml --resolved-only --include-cont --write
```

執行順序必須是：

1. 先將 `status: drop` 的 term 寫入 `glossary_drop_terms.yml`，確認成功後從 review 移除；不得加入 glossary 或 refs。
2. 完成已確認的 todo 與 cont 匯入，並保留 review 供後續 refs 更新。
3. 執行「來源覆蓋率檢查」，處理報告中的疑似漏收候選。
4. 執行上述 refs 腳本，更新仍在 review 中的項目之 `glossary_refs`。
5. 確認 refs 腳本成功完成後，再移除已匯入項目與 skip。
6. 若任一腳本執行失敗，不得宣稱來源覆蓋率或 glossary_refs 更新完成，必須回報錯誤。

更新範圍包括所有尚未移除的項目：

- todo
- ai
- cont
- skip

比對範圍包括：

- fixed
- aliases
- contextual
- reference_terms

規則：

- 保留仍存在且仍相關的既有 glossary_refs。
- 移除已不存在或明確不相關的 refs。
- 每個 review 項目最多保留 12 筆 refs；少於 12 筆時不要強行補足。
- 同一共享核心詞（例如 `Levies`、`Sofa`、`Groschen`）最多保留 3 筆相關 refs，避免單一詞族占滿名額。
- 若超過 12 筆，只保留優先度最高且符合上述核心詞上限的項目。
- 候選優先順序：
  1. exact match
  2. aliases 或拼寫變體
  3. 最長完整詞組
  4. 同一 lemma 的單複數、時態或分詞變化
  5. 明確的專名派生形式
  6. 國名、地名、文化名與居民／族群派生形式
  7. 具有直接語意關聯的 fixed 或 contextual term
  8. reference_terms
- 比對時應忽略大小寫、重音符號、標點、連字號、空格與所有格差異。
- 必須辨識高信心的詞形變化，例如：
  - Garrisons → Garrison
  - Bishoprics → Bishopric
  - Assimilated → Assimilate
- 必須辨識相關完整詞組，例如：
  - Prague Groschen → Meißner Groschen
- 必須辨識明確的專名派生，例如：
  - Italy → Italian → Italians
  - Croatia → Croatian → Croatians
  - Abkhazia → Abkhazian → Abkhazians
  - Catalonia → Catalan
  - Venice → Venetian
- 若 review term 是國名、地名、文化名或政體名的形容詞、居民、族群或語言派生形式，必須加入其基本專名作為 glossary_ref。
- 不得只依賴字面包含或共享普通單字；Sea、Cost、Type、Treaty、System 等泛用字不要任意加入。
- `glossary_drop_terms.yml` 只排除完整 term；例如 `Edict` 不得排除 `Edict of Worms`。
- 比對 drop 清單時忽略大小寫、重音符號、標點、連字號、空格與所有格差異，但仍須是完整 term 吻合。
- 無法高信心確認為同一 lemma、派生詞或直接相關詞條時，不要加入。
- reference_terms 只能作為翻譯參考，不得當作強制固定譯名。
- 不得修改 term、translation、status、keys、note 或上下文。
- 若 glossary_ref 來自 contextual，translation 必須列出該 contextual
  的所有 `senses[].zh`，依原順序以「、」合併在同一字串中。
- contextual 的 `default` 若已包含在 senses 中，不要重複列出。
- contextual glossary_ref 不得留下空的 translation。
- 例如：
  German → "德意志的、德意志人、德意志語"
- aliases glossary_ref 使用該 aliases 群組的 `zh` 翻譯。
- reference_terms 可列出其 suggestions，並以「、」合併；仍只能作為參考。
- 完成後必須回報腳本輸出的 `items`、`updated_refs` 與 `max_refs`。

## 六、Glossary 排序規則

本次不要重新排序 translation_glossary.yml。

保留 fixed、aliases、contextual、reference_terms 各區目前的條目順序、空行與註解位置。

匯入新條目時，不要移動或重排既有條目。

只有當我明確要求「排序 glossary」或「重新整理 glossary 順序」時，才執行各區字母排序。

## 七、檔案限制

- 不要修改 source/english/ 下的來源檔。
- 不要修改任何翻譯檔。
- 只在明確需要時修改 translation_glossary.yml。
- 不要修改尚未確認項目的 translation。
- 不要修改 review 項目的 term、keys、note 或上下文。
- glossary_refs 可依第五節規則更新，包含 status: skip 項目。
