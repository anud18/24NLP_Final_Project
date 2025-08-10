# ArXiv 論文摘要與實驗方法數據集報告

## 專案概述

本專案旨在建立一個用於訓練大型語言模型（LLM）的數據集，該數據集包含學術論文的摘要及其對應的實驗方法。透過此數據集，我們希望能夠訓練模型自動從論文摘要中擷取實驗方法的相關資訊。

## 數據需求定義

### 研究目標
- **主要目標**：建立一個高品質的論文摘要與實驗方法配對數據集
- **應用場景**：訓練LLM自動識別和擷取學術論文中的實驗方法
- **目標領域**：涵蓋計算機科學與其他學科領域

### 數據要求
- **數據源**：ArXiv學術論文庫
- **數據類型**：論文摘要（Abstract）與實驗方法（Methods）的配對
- **數據品質**：使用GPT-3.5進行方法擷取，確保標註品質
- **數據規模**：目標收集600篇論文的摘要與方法配對

## Level 2: 數據收集

### 爬蟲實作 (`get_arxiv_paper.py`)

我們開發了一個ArXiv API爬蟲程式，具有以下特點：

#### 核心功能
```python
def fetch_arxiv_data(start_date, end_date, max_results=300):
    query = f'submittedDate:[{start_date}0000 TO {end_date}2359]'
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return search.results()
```

#### 數據收集策略
- **時間範圍**：2020年1月1日至2020年12月1日
- **採樣策略**：每月收集5篇CS領域論文 + 5篇非CS領域論文
- **領域平衡**：確保CS與非CS領域的平衡分佈
- **品質控制**：過濾包含數學公式（$符號）的摘要，避免格式問題

#### 收集結果
- **總數據量**：600篇論文
- **CS論文**：300篇（50%）
- **非CS論文**：300篇（50%）
- **時間分佈**：2024年1月30日至2024年6月7日的論文

### 領域分佈分析
| 領域類別 | 數量 | 佔比 |
|---------|------|------|
| cs.LG (Machine Learning) | 56 | 9.3% |
| cs.CV (Computer Vision) | 55 | 9.2% |
| cs.CL (Computational Linguistics) | 55 | 9.2% |
| quant-ph (Quantum Physics) | 28 | 4.7% |
| cs.RO (Robotics) | 25 | 4.2% |
| cs.AI (Artificial Intelligence) | 16 | 2.7% |
| 其他領域 | 365 | 60.8% |

## Level 3: 數據處理

### 實驗方法擷取 (`extracy_method.py`)

#### GPT-3.5 方法擷取
我們使用OpenAI GPT-3.5-turbo模型自動擷取論文摘要中的實驗方法：

```python
def extract_methods(abstract: str) -> str:
    prompt = (
        "Extract the sentences that describe the methods used in the research from the following abstract. "
        "Only provide the sentences related to the methods, nothing else.\n\n"
        f"Abstract:\n{abstract}"
    )
    # ... GPT API 調用
```

#### 數據清洗與處理
- **錯誤處理**：實作異常處理機制，確保處理過程的穩定性
- **數據驗證**：檢查擷取結果的完整性
- **格式統一**：確保所有數據的格式一致性

### 數據集統計分析

#### 基本統計資訊
| 指標 | 摘要 (Abstract) | 方法 (Methods) |
|------|----------------|----------------|
| 平均長度 | 1,176 字符 | 550 字符 |
| 標準差 | 391 字符 | 229 字符 |
| 最小長度 | 180 字符 | 54 字符 |
| 最大長度 | 1,920 字符 | 1,324 字符 |
| 中位數 | 1,156 字符 | 527 字符 |


### 檔案結構
```
├── get_arxiv_paper.py      # ArXiv API爬蟲主程式
├── extracy_method.py       # GPT方法擷取程式
├── arxiv_dataset.csv       # 原始數據集
├── updated_arxiv_dataset.csv # 包含方法標註的最終數據集
└── README.md               # 專案說明
```


### 數據集格式
```csv
Id,Abstract,Date,Primary_category,Methods
論文ID,論文摘要,發表日期,主要類別,擷取的方法
```

---
