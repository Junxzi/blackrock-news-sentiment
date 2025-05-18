import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# GAFAMティッカー一覧
tickers = ["AAPL", "GOOGL", "META", "AMZN", "MSFT"]

# 実行コマンドを順に走らせる
for ticker in tickers:
    print(f"▶ ニュース取得中: {ticker}")
    exit_code = os.system(f"poetry run python src/fetch_news.py {ticker}")
    if exit_code != 0:
        print(f"⚠️ エラーが発生しました: {ticker}")
    else:
        print(f"✅ {ticker} 完了\n")

print(f"🕓 終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")