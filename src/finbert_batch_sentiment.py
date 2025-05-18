import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import datetime

# モデル準備
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
labels = ['negative', 'neutral', 'positive']

# 分析対象ティッカー
tickers = ["AAPL", "GOOGL", "META", "AMZN", "MSFT"]

# 日付取得（最新ファイルを見つけるため）
today = datetime.today().strftime("%Y%m%d")

# 感情判定関数
def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return labels[pred]

# 各ティッカーに対して処理
for ticker in tickers:
    input_path = f"data/{ticker}_news_finnhub_{today}.csv"
    output_path = f"data/{ticker}_news_with_sentiment.csv"

    if not os.path.exists(input_path):
        print(f"入力ファイルが見つかりません: {input_path}")
        continue

    print(f"▶ {ticker} を処理中...")

    df = pd.read_csv(input_path)
    df['text'] = df['headline'].fillna('') + '. ' + df['summary'].fillna('')
    df['sentiment_finbert'] = df['text'].apply(get_sentiment)
    df['sentiment_score'] = df['sentiment_finbert'].map({'positive': 1, 'neutral': 0, 'negative': -1})
    df.to_csv(output_path, index=False)

    print(f"感情分析完了: {output_path}\n")

print("all processes completed")
