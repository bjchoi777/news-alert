import feedparser
import requests
import os
from datetime import datetime

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

KEYWORDS = [
    "기후에너지환경부",
    "기후에너지환경부 산하",
    "기후에너지환경부 소속기관",
    "한국수자원공사",
    "한국전력",
    "기후부",
    "환경청",
    "환경공단",
    "국립공원공단"
    "매립지공사"
    "한국수력원자력"
    "국립생태원"
    "한국환경기술원"
    "환경보전원"
  
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })

def fetch_news(keyword):
    rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(keyword)}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:3]

def main():
    today = datetime.now().strftime("%Y년 %m월 %d일")
    message = f"📰 <b>{today} 뉴스 알림</b>\n\n"

    for keyword in KEYWORDS:
        entries = fetch_news(keyword)
        if entries:
            message += f"🔍 <b>{keyword}</b>\n"
            for entry in entries:
                message += f"• <a href='{entry.link}'>{entry.title}</a>\n"
            message += "\n"

    send_telegram(message)

if __name__ == "__main__":
    main()
