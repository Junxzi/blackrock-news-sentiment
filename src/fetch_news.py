from datetime import datetime, timedelta
import requests
import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def safe_parse_datetime(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError, OSError):
        return None
    

API_KEY = os.getenv("FINNHUB_API_KEY")

ticker = sys.argv[1] if len(sys.argv) > 1 else "BLK"

def fetch_news(ticker, from_date, to_date):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={from_date}&to={to_date}&token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ Error {response.status_code} for {from_date} ~ {to_date}")
        return []

# ✅ ターゲット期間を1年間に設定
today = datetime.today()
start_date = today - timedelta(days=365)

# ニュースをまとめて格納
all_news = []

# ✅ 90日ずつ分割して取得
window_size = 90
current_start = start_date

while current_start < today:
    current_end = min(current_start + timedelta(days=window_size - 1), today)
    from_str = current_start.strftime("%Y-%m-%d")
    to_str = current_end.strftime("%Y-%m-%d")
    
    print(f"📦 Fetching: {from_str} → {to_str}")
    news_batch = fetch_news(ticker, from_str, to_str)
    all_news.extend(news_batch)

    current_start += timedelta(days=window_size)

# ✅ CSV保存
df = pd.DataFrame(all_news)
save_path = f"data/{ticker}_news_finnhub_full.csv"
df.to_csv(save_path, index=False)
print(f"✅ 保存完了: {save_path}（記事数: {len(df)}）")


# 📝 データ整形
df = pd.DataFrame([{
    "datetime": safe_parse_datetime(article.get("datetime")),
    "headline": article.get("headline"),
    "summary": article.get("summary"),
    "url": article.get("url"),
    "source": article.get("source")
} for article in all_news])

# 💾 保存
today = datetime.today().strftime("%Y%m%d")
output_path = f"data/{ticker}_news_finnhub_{today}.csv"
df.to_csv(output_path, index=False)

print(f"{len(df)} articles saved to {output_path}")