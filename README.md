# GAFAMニュース感情と株価リターンの関係分析

## プロジェクト概要

本プロジェクトでは、GAFAM（Google, Apple, Meta, Amazon, Microsoft）のニュース記事を用い、BERTベースのモデル（FinBERT）によって感情を定量化し、株価リターンとの関係を分析しました。

---

## 使用技術

- Python 3.12
- [Finnhub API](https://finnhub.io/)：ニュース取得
- FinBERT（ProsusAI/finbert）：感情分析
- yfinance：株価データ取得
- pandas / matplotlib / seaborn：データ処理と可視化

---

## ディレクトリ構成
```
project/
├── data/ # ニュース＆分析用CSV
├── notebooks/ # 分析・可視化Notebook
├── src/
│ ├── fetch_news_finnhub.py # 過去1年分のニュース取得スクリプト
│ ├── fetch_multiple_news.py # GAFAM全社一括取得スクリプト
│ ├── finbert_batch_sentiment.py # ニュース感情分析
│ └── (その他分析補助コード)
├── README.md
├── pyproject.toml
```

---

## 📈 分析結果サマリ（例）

| Ticker | N_Pos | N_Neg | Mean_Pos | Mean_Neg | Correlation |
|--------|-------|-------|----------|----------|-------------|
| AAPL   | 4     | 2     | 0.0162   | 0.0030   | 0.7689      |
| META   | 7     | 2     | 0.0127   | -0.0092  | 0.3160      |
| MSFT   | 6     | 2     | 0.0028   | 0.0162   | -0.4881     |

- `N_Pos`, `N_Neg`：感情スコアが正・負だった日の数
- `Mean_*`：それらの日の翌日リターン平均
- `Correlation`：感情スコアと翌日リターンの相関係数

---

## 考察

- 感情スコアが株価に与える影響は企業によって異なる
- Metaは感情とリターンにやや正の相関があり、今後深堀りの余地がある
- Microsoftでは逆相関が見られるなど、単純なポジティブ≠上昇とは限らない
- 結果の多くでt検定が成立していないため、サンプルサイズの拡大が必要

---

## 今後の展望

- 期間を2年に拡張し、検定可能なサンプル数の増加を目指す
- 感情スコアの変化量（diff）や極端値を使った異常検知分析
- 他の感情モデル（ChatGPTやTwitter-RoBERTa）との比較

---

## 実行方法（例）

```bash
# ニュース取得（1社）
poetry run python src/fetch_news_finnhub.py (指定する企業のticker名)

# 全社一括取得
poetry run python src/fetch_multiple_news.py

# 感情分析
poetry run python src/finbert_batch_sentiment.py


