import requests
from bs4 import BeautifulSoup
import os

# Yahan jis product ko track karna hai uska link daalein
GPU_URL = "https://www.amazon.in/dp/B0C8VBRS36" 
TARGET_PRICE = 30000  # Apna budget yahan set karein

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(GPU_URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        price_element = soup.find(class_="a-price-whole")
        if price_element:
            price_str = price_element.text.replace(',', '').replace('.', '').strip()
            current_price = int(price_str)
            
            print(f"Current Price: ₹{current_price}")
            
            if current_price <= TARGET_PRICE:
                msg = f"🚨 LOOT ALERT! 🚨\nPrice drop: ₹{current_price}\nLink: {GPU_URL}"
                requests.post(f"https://api.telegram.com/bot{TELEGRAM_TOKEN}/sendMessage", 
                              data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
                print("Alert sent to Telegram!")
        else:
            print("Price nahi mila.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_price()
