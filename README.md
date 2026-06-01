# 🧬 大學課程專題：演化式計算課程的遺傳演算法 (GA) 核心機制與應用研究報告

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13.0-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows%2011-0078d4?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/Topic-Evolutionary%20Computation-emerald?style=for-the-badge" alt="Topic">
  <img src="https://img.shields.io/badge/Academic-Project-orange?style=for-the-badge" alt="Academic">
</p>

## 📌 專案與作者資訊

| 項目 | 詳細資訊 |
| :--- | :--- |
| **課程名稱** | 演化式計算 (Evolutionary Computation) |
| **專題名稱** | 任務排程問題的最佳化求解研究 |
| **授課教師** | 江傳文 教授 |
| **開發作者** | 國立高雄科技大學 電腦與通訊工程系 二甲 - 劉志凌 (C112110130) |
| **製作日期** | 5/31[cite: 7] |

---

## 📖 專案簡介

本專案針對平行運算系統中的 **有向無環圖 (DAG) 任務排程問題 (Task Scheduling Problem)** 進行深入研究。排程問題已被證實屬於 **NP-hard** 限制求解問題，傳統窮舉法在龐大的搜尋空間中難以在有效時間內求得最優解[cite: 7]。

本系統基於 **遺傳演算法 (Genetic Algorithm, GA)** 的核心框架，透過模擬自然界「適者生存」之原理[cite: 7]，並加入**動態突變率調校**、**進階防陷落機制（強制突變）**與**高比例精英保留策略**[cite: 7]，實現在多處理器環境下追求整體排程完成時間（Makespan）最小化的目標[cite: 7]。

---

## 🛠️ 實驗執行環境

為確保評估與數據效能具備可重複性，本專案之基準測試運行於以下硬體及軟體環境：

* **作業系統：** Windows 11 (64位元)[cite: 7]
* **開發語言：** Python 3.13.0 (運行於系統預設環境)[cite: 2, 7]
* **中央處理器 (CPU)：** AMD Ryzen 7 4800H with Radeon Graphics[cite: 7]
* **隨機存取記憶體 (RAM)：** 8 GB DDR4[cite: 7]
* **儲存空間：** 固態硬碟 (SSD)[cite: 7]

---

## ⚙️ 演算法核心機制與參數設計

本演算法針對傳統 GA 易陷入局部最佳解（Local Optima）的缺點進行改進，設計多層次的控制迴圈：

### 1. 染色體編碼方式 (Chromosome Encoding)
* **表示結構：** 解結構由雙元件 `(ss, ms)` 構成。其中 `ss` 代表符合拓撲排序 (Topological Sort) 的任務執行順序序列，而 `ms` 代表長度等於任務總數的處理器分配序列（每個位置對應一個指定處理器 ID）[cite: 2, 7]。
* **適應度評估 (Fitness Function)：** 以模擬排程計算得出的總完成時間 (Makespan) 作為指標[cite: 7]，數值越小代表適應度越佳[cite: 7]。評估過程中精確計入各處理器間因資料傳輸產生的通訊延遲時間[cite: 2, 7]。

### 2. 優化參數設定 (Hyperparameters)
* **族群大小 (Population Size)：** 固定設置為 $90$[cite: 7]。
* **最大迭代世代數 (Generations)：** 固定設置為 $560$ 代[cite: 7]。
* **交配機制 (Crossover)：** 採用單點交叉 (Single-point Crossover) 算子進行基因重組[cite: 2, 7]。
* **精英保留策略 (Elitism)：** 採取極為激進的高比例保留，每代直接篩選前 **$60\%$** 的最佳個體複製至下一代族群，防止優良基因流失[cite: 7]。
* **三階段動態突變率 (Dynamic Mutation Rate)：** 
  * 演化前期：設置為 `0.27`，維持全域搜尋廣度並增加基因多樣性[cite: 7]。
  * 演化中期：降低至 `0.12`，逐步收斂搜尋範圍[cite: 7]。
  * 演化後期：收斂至 `0.02`，進行微調並加速局部最佳化[cite: 7]。
* **強制突變機制 (Forced Mutation)：** 引進連續停滯監控，若族群連續 **5 代** 未能更新最佳解，則對族群後 $40\%$ 的劣質染色體實施強制作業，打破局部陷落僵局[cite: 7]。

---

## 📁 專案檔案架構

```markdown
├── main.py          # 遺傳演算法完整實作程式碼 (包含解析器、選擇、交配、突變與主控迴圈)[cite: 2]
├── n4_00.dag.txt    # 基準測試測試集數據：標準等權重測試資料[cite: 3, 7]
├── n4_02.dag.txt    # 基準測試測試集數據：異值計算成本測試資料一[cite: 4, 7]
├── n4_04.dag.txt    # 基準測試測試集數據：異值計算成本測試資料二[cite: 5, 7]
├── n4_06.dag.txt    # 基準測試測試集數據：異值計算成本測試資料三[cite: 6, 7]
└── README.md        # 專案說明文件
