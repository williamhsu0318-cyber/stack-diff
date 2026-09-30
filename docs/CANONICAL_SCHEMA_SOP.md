# StackDiff Canonical Data & Comparison Architecture SOP

本文件定義 **StackDiff (getstackdiff.com)** 的核心資料標準、命名規則與新增工具的標準作業程序（SOP）。所有未來的工程師、AI 代理或編輯者**皆必須嚴格遵守以下準則**，以確保全站資料品質、SEO 永續性與商業轉化力。

---

## 1. 核心原則 (Core Philosophy)

1. **極致品質重於數量 (Quality over Quantity)**：
   寧可只索引 20 款真正被市場高頻搜尋的主流旗艦工具，也不要索引 500 個未經驗證、充滿 AI 幻覺或過期資料的邊緣工具。
2. **絕對客觀接地 (Zero-Hallucination Grounding)**：
   所有價格、免費額度與限制（Gotchas）必須來自**官方定價頁面或官方開發者文件**（透過 Jina Reader `https://r.jina.ai/{url}` 查核），嚴禁 AI 隨意推測。
3. **無版本污染的永續網址 (Evergreen URLs)**：
   工具的「實體識別名稱 (Brand/Product Entity)」必須與「底層模型版本 (Model/Version)」嚴格解耦。

---

## 2. Entity 命名與 Slug 規範

| 元素 | 規範 | 正確範例 | 錯誤反例 (嚴格禁止) |
| :--- | :--- | :--- | :--- |
| **Tool Slug** | 純小寫、短網址、不帶版本號 | `cursor`, `runway`, `midjourney`, `claude` | `runway-gen3`, `midjourney-v6`, `claude-3-5-sonnet` |
| **Tool Name** | 純品牌/產品名稱 | `Runway`, `Midjourney`, `Claude Pro` | `Runway Gen-3 Alpha`, `Midjourney v6.1`, `Ideogram 2.0` |
| **Model Version** | 收斂在 `current_models` 陣列中 | `["Gen-3 Alpha", "Gen-3 Turbo"]` | 把模型名稱填在 Tool Name 欄位 |
| **Comparison URL** | 兩個乾淨 Slug 的小寫組合 | `/compare/chatgpt-vs-claude` | `/compare/chatgpt-vs-claude-3-5-sonnet` |

---

## 3. Field-Level Freshness 規範

1. **禁止假冒全頁驗證**：
   嚴格禁止使用任何自動抓當前月份的「Verified for [Month Year]」Badge。
2. **欄位級別的透明時間戳記**：
   * 定價區塊：清楚標註 `Pricing Checked: YYYY-MM-DD`，並緊鄰 `[Official Pricing ↗]` 外鏈按鈕。
   * 規格矩陣：清楚標註 `Specs Checked: YYYY-MM-DD`。
   * 只有在所有核心規格真的來自該次更新時，才允許更新此日期。

---

## 4. 對決靈魂：Pair-Specific Differentiator (Why the Difference Matters)

在比較頁面上，**嚴格禁止**只是單純把「Tool A 的通用介紹」與「Tool B 的通用介紹」硬拼在一起。每一組重點對決必須提供 **對決核心差異 (PairDifferentiator)**：

```typescript
export interface PairDifferentiator {
  coreBattle: string;         // 例如："Composer 2.5 Multi-File Agent vs. Cascade Collaborative Flow State"
  whyItMatters: {
    title: string;            // 例如："Multi-File Editing Architecture"
    description: string;      // 直擊工程細節、額度陷阱與使用場景的深度剖析
  }[];
  decisiveQuestion: string;   // 幫助開發者在 5 秒內做出選擇的決定性問題
}
```

---

## 5. 新增工具之標準工作流 (Workflow)

當需要新增或更新任何工具時，遵循以下 4 步：

1. **查核官方資訊**：
   透過官方定價頁或使用管線腳本：
   ```bash
   python scripts/research_pipeline.py --tool <tool-slug> --url <official-pricing-url>
   ```
2. **審查終端 Audit Card**：
   比對新舊模型、定價模式與隱藏限制（Gotchas），確認無幻覺後再同意寫入資料庫。
3. **補充 Pair Differentiator**：
   若為重要同類競品對決，在 `src/utils/specEngine.ts` 中的 `PAIR_DIFFERENTIATORS` 加入該對決的關鍵差異。
4. **本機驗證**：
   ```bash
   npm run build
   ```
   確保所有頁面 prerender 成功無破圖，再發起 Pull Request 或推播至遠端。
