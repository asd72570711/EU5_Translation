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

請將 `status: cont` 視為「要求 AI 重新複核」，不是預先決定必須建立
`contextual`。請根據 source key、完整上下文與必要的其他用法判斷：

- 所有實際用法都能明確使用同一譯名，且沒有需要保留語境彈性的理由：將 status 改為 `fixed`，保留使用者已填的 translation。
- 不同實際用法需要不同譯法，或 AI 判斷保留語境彈性較安全：保留 status `cont`，建立 `contextual`。
- 上下文不足或無法高信心判斷：保留 status `cont`，不要匯入 glossary。

對每個有 translation 的 `cont`，必須先回答「它真的需要 contextual 嗎？」：

1. 使用者提供的 translation 是至少要保留的譯義，不是完整答案。
2. AI 必須檢查來源上下文、同一 term 的其他用法，以及詞性、專名派生或遊戲機制差異，
   自行判斷是否存在其他實際需要的譯義。
3. 若確認需要 contextual，除了保留使用者提供的譯義外，補上 AI 根據實際語境高信心判斷出的其他譯義；
   不要只因字典列有可能意思就任意擴充。
   對國名、地名、族群名與語言名的派生形式，必須額外檢查詞性：
   高信心的形容詞／居民名要分別考慮「X 的」與「X 人」；只有來源上下文
   或術語本身明確指向語言時，才加入「X 語」。例如 `Cypriot` 應判斷為
   「賽普勒斯的」與「賽普勒斯人」，但不能僅因它是地域派生詞就補「賽普勒斯語」。
4. 若所有已確認用法其實是同一意思，且沒有合理的語境不確定性，即使 translation 中有多個同義譯名，
   也改為 `fixed`，不要為了保留多個同義詞而建立 contextual。
5. 即使目前只有一種 translation，只要 term 仍可能因詞性、專名派生、頭銜或遊戲語境而產生不同譯法，
   AI 可以判斷保留 `cont` 較安全；此時建立只有一個 sense 的 `contextual` 也是有效結果，不必為了湊出多個譯義而擴充。
6. 若沒有 translation，或資料不足以判斷，保留 `cont`，不得自行填寫翻譯。

不得因為 term 未列在腳本內建清單而直接判定為 `fixed` 或 `contextual`。
只有 `status: cont` 的 translation 才能依語意將「、」、中文或英文逗號、分號視為多個 contextual senses；
其他 status 的翻譯必須保留完整原文。不要機械拆分本身就是單一譯名的標點內容，例如
`Left and Right Chancellor: 左、右丞相`。

不得僅因 term 看起來像地名派生詞、族群名、宗教名或語言名，
就自動補上「人」或「語」。只有 review translation 明確提供，或來源上下文
明確指向人物、居民、族群或語言時，才建立對應 sense；沒有充分證據時省略該 sense。
AI 完成上述 `cont` 複核後，才可更新該 `cont` 的 status 與 translation；不得修改其他受保護欄位。
匯入腳本不得再改寫 review translation，也不得用預設規則覆蓋 AI 或使用者確認的內容。
匯入腳本只負責寫入 review 最終確認的值：`todo`/`ai` 原樣進入 `fixed`，
`cont` 依 AI 最終保留的 status 與 translation 建立 `fixed` 或 `contextual`；
不得依英文 term、詞性、字尾或內建詞表自行新增、刪除、翻譯或改寫任何 sense。

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
- 匯入 fixed 或 contextual 時，只匯入 term 與 translation；不要將 review 的 `note` 或可選 `review_comment` 複製成 glossary 註解。
- `note` 保留為既有 review 欄位以維持格式相容；若需要留下審查說明，可使用可選的 `review_comment` 欄位，但該欄位也不得匯入 glossary。

## 四、review 清理

glossary_refs 更新並成功完成後：

- 移除已匯入的 todo。
- 移除已確認並匯入的 ai。
- 移除 skip 前，先將每筆 skip 的 `term` 與 `keys` 寫入
  `work/glossary_review/skip_history.json`，再移除 skip。
- 將 `status: drop` 的完整 term 加入 `glossary_drop_terms.yml` 後移除。
- 保留尚未確認的 todo、ai 與 cont。
- 不要因為更新 glossary_refs 而刪除尚未確認的項目。

## 四之一、來源覆蓋率檢查

在移除 `skip` 前，必須先執行來源覆蓋率檢查：

```powershell
python scripts/audit_glossary_review_coverage.py --review work/glossary_review/review.json --glossary translation_glossary.yml --source-root source/english --skip-history work/glossary_review/skip_history.json --write-report
```

此腳本會使用 `review.json` 的 `source_file` 清單，重新掃描實際來源檔，
並將候選與 `translation_glossary.yml` 及目前 review 項目比對，
報告可能完全漏收的候選至：

```text
work/glossary_review/coverage_audit.json
```

腳本只產生報告，不會修改 `review.json`、glossary、來源檔或翻譯檔。

覆蓋率檢查必須使用 `skip_history.json`：相同 term 在已記錄的相同來源 key
再次出現時，不列為疑似漏收；若同一 term 出現在尚未審查的新 key，仍須回報，
而且報告中只保留尚未審查的 keys。`skip_history` 不得影響一般 Scan，
也不等同於全域排除 term 的 `drop`。

若需要為新增候選或審查結果留下說明，使用可選的 `review_comment` 欄位；
`note` 與 `review_comment` 都只屬於 review metadata，任何匯入流程都不得將它們寫入 glossary。

請檢查報告中的 `high` 與 `normal` 信心候選，僅在審查報告中列出判斷結果，
不要因覆蓋率檢查自動新增、修改或刪除 `review.json` 項目。

若發現可能漏收的專有名詞、制度名、宗教概念、人物、作品名或可重複使用術語，
只報告 term、來源 key、判斷理由與建議處理方式；是否新增 review 項目，
由使用者另行執行 Scan 或明確要求後處理。

若候選只是一般語言或一次性片語，也只在報告中標記為疑似可忽略，
不得直接改成 `skip`。

不要因為候選只出現一次、位於句首、含縮寫、頭銜、重音符號或小寫姓名片段，
就直接判定為漏收或 `skip`。

## 五、glossary_refs 更新

所有已確認項目完成匯入 translation_glossary.yml 後，
必須先使用最新的 translation_glossary.yml 更新 review.json，
再進行 review 清理。

必須實際執行以下腳本，不得只在回覆中描述「已更新 refs」：

```powershell
python scripts/import_glossary_review.py --review work/glossary_review/review.json --glossary translation_glossary.yml --drop-terms glossary_drop_terms.yml --skip-history work/glossary_review/skip_history.json --resolved-only --include-cont --keep-review --write

python scripts/update_review_glossary_refs.py --review work/glossary_review/review.json --glossary translation_glossary.yml --max-refs 12 --core-max-refs 3 --write

python scripts/import_glossary_review.py --review work/glossary_review/review.json --glossary translation_glossary.yml --drop-terms glossary_drop_terms.yml --skip-history work/glossary_review/skip_history.json --resolved-only --include-cont --write
```

執行順序必須是：

1. 先將 `status: drop` 的 term 寫入 `glossary_drop_terms.yml`，確認成功後從 review 移除；不得加入 glossary 或 refs。
2. 完成已確認的 todo 與 cont 匯入，並保留 review 供後續 refs 更新。
3. 執行「來源覆蓋率檢查」，只報告疑似漏收候選，不修改 review。
4. 執行上述 refs 腳本，更新仍在 review 中的項目之 `glossary_refs`。
5. 確認 refs 腳本成功完成後，先把 skip 的 term 與 keys 合併寫入
   `skip_history.json`，成功後再移除已匯入項目與 skip。
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
  - Iceland → Icelandic
  - Europe → European
- 若 review term 是國名、地名、文化名或政體名的形容詞、居民、族群或語言派生形式，必須加入其基本專名作為 glossary_ref。
- 不得只依賴字面包含或共享普通單字；Sea、Cost、Type、Treaty、System 等泛用字不要任意加入。
- `glossary_drop_terms.yml` 只排除完整 term；例如 `Edict` 不得排除 `Edict of Worms`。
- 比對 drop 清單時忽略大小寫、重音符號、標點、連字號、空格與所有格差異，但仍須是完整 term 吻合。
- 無法高信心確認為同一 lemma、派生詞或直接相關詞條時，不要加入。
- reference_terms 只能作為翻譯參考，不得當作強制固定譯名。
- 在 glossary_refs 更新階段，不得修改 term、translation、status、keys、note 或上下文；
  `cont` 的 status 與 translation 只能在前面的 AI 語意複核階段依本節規則更新。
- 若 glossary_ref 來自 contextual，translation 必須列出該 contextual
  的所有 `senses[].zh`，依原順序以「、」合併在同一字串中。
- contextual 的 `default` 若已包含在 senses 中，不要重複列出。
- contextual glossary_ref 不得留下空的 translation。
- 例如：
  German → "德意志的、德意志人、德意志語"
- aliases glossary_ref 使用該 aliases 群組的 `zh` 翻譯。
- reference_terms 可列出其 suggestions，並以「、」合併；仍只能作為參考。
- 完成後必須回報腳本輸出的 `items`、`updated_refs` 與 `max_refs`。
- 同時回報 `skip_history_terms_added`、`skip_history_keys_added`、
  `skip_history_filtered_candidates` 與 `skip_history_filtered_keys`。

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
- 不要修改 review 項目的 term、keys、note、review_comment 或上下文。
- `category` 是舊版 review metadata；不要修改既有項目的 `category`，新增候選時也不要建立 `category` 或 `category: unknown`。
- glossary_refs 可依第五節規則更新，包含 status: skip 項目。
