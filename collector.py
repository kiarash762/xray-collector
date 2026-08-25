import re
import requests
from bs4 import BeautifulSoup

# لیست آیدی عمومی کانال‌های مدنظرتان بدون @
CHANNELS = [
    "SOSkeyNET",
    "",
]

CONFIG_PATTERNS = [
    r"vmess://[a-zA-Z0-9+/=]+",
    r"vless://[a-zA-Z0-9\-]+@[a-zA-Z0-9\.\-_]+:\d+\?[^\s<]+",
    r"trojan://[a-zA-Z0-9\-]+@[a-zA-Z0-9\.\-_]+:\d+\?[^\s<]+",
    r"ss://[a-zA-Z0-9\-_+=/]+@[a-zA-Z0-9\.\-_]+:\d+#[^\s<]+",
    r"tuic://[^\s<]+",
    r"hysteria2?://[^\s<]+"
]

def fetch_configs():
    all_configs = set()
    for channel in CHANNELS:
        url = f"https://t.me/s/{channel}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text_content = soup.get_text()
                for pattern in CONFIG_PATTERNS:
                    matches = re.findall(pattern, text_content)
                    for match in matches:
                        all_configs.add(match.strip())
        except Exception as e:
            print(f"Error reading {channel}: {e}")

    with open("sub_link.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))

if __name__ == "__main__":
    fetch_configs()
