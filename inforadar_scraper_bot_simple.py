
import time
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = "7604446870:AAHpQRJQfMKCPsCt6CG86hPMZtsh24jevts"
CHAT_ID = "719052415"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def check_inforadar(url, sport):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("tr")
        for row in rows:
            text = row.get_text()
            if "Alg.1" in text:
                parts = text.split()
                for i, part in enumerate(parts):
                    if part == "Alg.1" and i+1 < len(parts):
                        try:
                            value = float(parts[i+1])
                            if abs(value) >= 0.1:
                                send_telegram_message(f"🚨 <b>{sport} ALERT</b>\nAlg.1 = {value}\n{row.get_text(strip=True)}")
                        except:
                            continue
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        check_inforadar("https://inforadar.live/#/dashboard/soccer/live", "⚽ Soccer")
        check_inforadar("https://inforadar.live/#/dashboard/basketball/live", "🏀 Basketball")
        time.sleep(60)

if __name__ == "__main__":
    main()
