import os
import sys
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime, timedelta

# ✅ APIキー読み込み
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

# ✅ ティッカーをコマンドライン引数から取得
if len(sys.argv) < 2:
    print("Usage: python fetch_news_finnhub.py TICKER")
    sys.exit(1)

ticker = sys.argv[1].upper()
print(f"Fetching news for: {ticker}")

# 📅 取得期間（過去N日分）
N_DAYS = 90
to_date = datetime.today()
from_date = to_date - timedelta(days=N_DAYS)
from_str = from_date.strftime("%Y-%m-%d")
to_str = to_date.strftime("%Y-%m-%d")

# 🌐 APIリクエスト
url = (
    f"https://finnhub.io/api/v1/company-news"
    f"?symbol={ticker}&from={from_str}&to={to_str}&token={API_KEY}"
)
response = requests.get(url)
articles = response.json()

# 📝 データ整形
df = pd.DataFrame([{
    "datetime": datetime.fromtimestamp(article["datetime"]).strftime("%Y-%m-%d %H:%M"),
    "headline": article["headline"],
    "summary": article["summary"],
    "url": article["url"],
    "source": article["source"]
} for article in articles])

# 💾 保存
today = datetime.today().strftime("%Y%m%d")
output_path = f"data/{ticker}_news_finnhub_{today}.csv"
df.to_csv(output_path, index=False)

print(f"{len(df)} articles saved to {output_path}")