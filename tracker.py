import requests
from bs4 import BeautifulSoup
import os

# Yahan dono cards ke links aur unka target price set hai
CARDS_TO_TRACK = [
    {
        "name": "RX 6600 8GB",
        "url": "https://www.amazon.in/dp/B09H3PY14M",
        "target_price": 20000
    },
    {
        "name": "RTX 3050 8GB",
        "url": "https://www.amazon.in/dp/B09Q919S35",
        "target_price": 18000
    }
]

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    for card in CARDS_TO_TRACK:
        try:
            response = requests.get(card["url"], headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.find(class_="a-price-whole")
            
            if price_element:
                price_str = price_element.text.replace(',', '').replace('.', '').strip()
                current_price = int(price_str)
                
                print(f"{card['name']} Current Price: ₹{current_price}")
                
                if current_price <= card["target_price"]:
                    msg = f"🚨 GPU LOOT ALERT! 🚨\n\n{card['name']} ka price drop ho gaya hai!\nCurrent Price: ₹{current_price}\nTarget Price: ₹{card['target_price']}\n\nLink: {card['url']}"
                    requests.post(f"https://api.telegram.com/bot{TELEGRAM_TOKEN}/sendMessage", 
                                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
                    print(f"Alert sent for {card['name']}!")
            else:
                print(f"{card['name']} ka price tag nahi mila.")
        except Exception as e:
            print(f"Error checking {card['name']}:", e)

if __name__ == "__main__":
    check_price()

