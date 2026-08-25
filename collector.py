import re
import requests
from bs4 import BeautifulSoup

# کانال‌های مدنظر شما
CHANNELS = [
    "SOSkeyNET",
    "another_channel_id"
]

CONFIG_PATTERNS = [
    r"vmess://[a-zA-Z0-9+/=]+",
    r"vless://[a-zA-Z0-9\-]+@[a-zA-Z0-9\.\-_]+:\d+\?[^\s<]+",
    r"trojan://[a-zA-Z0-9\-]+@[a-zA-Z0-9\.\-_]+:\d+\?[^\s<]+",
    r"ss://[a-zA-Z0-9\-_+=/]+@[a-zA-Z0-9\.\-_]+:\d+#[^\s<]+",
    r"tuic://[^\s<]+",
    r"hysteria2?://[^\s<]+"
]

# تعداد صفحات به عقب (هر صفحه حدود ۲۰ پیام است؛ مثلاً عدد ۳ یعنی حدود ۶۰ پیام آخر)
PAGES_TO_FETCH = 4

def fetch_configs():
    all_configs = set()

    for channel in CHANNELS:
        before_id = None
        for _ in range(PAGES_TO_FETCH):
            url = f"https://t.me/s/{channel}"
            if before_id:
                url += f"?before={before_id}"

            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                text_content = soup.get_text()

                for pattern in CONFIG_PATTERNS:
                    matches = re.findall(pattern, text_content)
                    for match in matches:
                        all_configs.add(match.strip())

                # پیدا کردن ID اولین پیام صفحه برای بارگذاری پیام‌های قبل‌تر
                messages = soup.find_all("div", class_="tgme_widget_message")
                if not messages:
                    break
                
                # استخراج ID اولین پیام موجود در صفحه
                first_msg_data = messages[0].get("data-post")
                if first_msg_data and "/" in first_msg_data:
                    before_id = first_msg_data.split("/")[-1]
                else:
                    break

            except Exception as e:
                print(f"Error fetching from {channel}: {e}")
                break

    with open("sub_link.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))

if __name__ == "__main__":
    fetch_configs()
