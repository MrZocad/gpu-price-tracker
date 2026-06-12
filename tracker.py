import requests
from bs4 import BeautifulSoup
import os

# Isme Amazon aur Flipkart dono ke links aur unka target price set hai
CARDS_TO_TRACK = [
    {
        "name": "RX 6600 8GB (Amazon)",
        "url": "https://www.amazon.in/dp/B09H3PY14M",
        "target_price": 20000,
        "site": "amazon"
    },
    {
        "name": "RX 6600 8GB (Flipkart)",
        "url": "https://www.flipkart.com/sapphire-amd-radeon-rx-6600-8-gb-gddr6-graphics-card/p/itm6c9b3fc01ff7d",
        "target_price": 20000,
        "site": "flipkart"
    },
    {
        "name": "RTX 3050 8GB (Amazon)",
        "url": "https://www.amazon.in/dp/B09Q919S35",
        "target_price": 18000,
        "site": "amazon"
    },
    {
        "name": "RTX 3050 8GB (Flipkart)",
        "url": "https://www.flipkart.com/msi-nvidia-geforce-rtx-3050-ventus-2x-xs-8g-oc-8-gb-gddr6-graphics-card/p/itm5a1804b407bfa",
        "target_price": 18000,
        "site": "flipkart"
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
            current_price = None
            
            if card["site"] == "amazon":
                price_element = soup.find(class_="a-price-whole")
                if price_element:
                    price_str = price_element.text.replace(',', '').replace('.', '').strip()
                    current_price = int(price_str)
                    
            elif card["site"] == "flipkart":
                # Flipkart ke price tag ko dhoondne ke liye class code
                price_element = soup.find(class_="Nx9w9m") or soup.find(class_="_10EHIb")
                if price_element:
                    price_str = price_element.text.replace('₹', '').replace(',', '').strip()
                    current_price = int(price_str)
            
            if current_price:
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
