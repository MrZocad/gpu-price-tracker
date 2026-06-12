import requests
from bs4 import BeautifulSoup
import os

# Sabhi PC components ke links, target price aur website set hai
ITEMS_TO_TRACK = [
    # --- GRAPHICS CARDS ---
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
    },
    # --- CPU (RYZEN 5 5600) ---
    {
        "name": "Ryzen 5 5600 (Amazon)",
        "url": "https://www.amazon.in/dp/B09VCHR1VH",
        "target_price": 13000,
        "site": "amazon"
    },
    {
        "name": "Ryzen 5 5600 (Flipkart)",
        "url": "https://www.flipkart.com/amd-ryzen-5-5600-3-5-ghz-uarto-core-processor/p/itm3d73507340b02",
        "target_price": 13000,
        "site": "flipkart"
    },
    # --- MOTHERBOARD (MSI B550M PRO-VDH WIFI) ---
    {
        "name": "MSI B550M Pro-VDH WiFi (Amazon)",
        "url": "https://www.amazon.in/dp/B08965Y8R9",
        "target_price": 9500,
        "site": "amazon"
    },
    {
        "name": "MSI B550M Pro-VDH WiFi (Flipkart)",
        "url": "https://www.flipkart.com/msi-b550m-pro-vdh-wifi-motherboard/p/itm674eb884a6c8e",
        "target_price": 9500,
        "site": "flipkart"
    },
    # --- NVME GEN 4 SSD (500GB / 512GB) ---
    {
        "name": "Crucial Gen4 NVMe 500GB SSD (Amazon)",
        "url": "https://www.amazon.in/dp/B0CKTQNX9G",
        "target_price": 6000,
        "site": "amazon"
    },
    {
        "name": "WD Black Gen4 NVMe 500GB SSD (Flipkart)",
        "url": "https://www.flipkart.com/wd-black-sn770-500-gb-desktop-laptop-internal-solid-state-drive-wds500g3x0e/p/itmd5f788b776263",
        "target_price": 6000,
        "site": "flipkart"
    },
    # --- DDR4 8GB 3200MHZ RAM ---
    {
        "name": "Corsair Vengeance 8GB 3200MHz RAM (Amazon)",
        "url": "https://www.amazon.in/dp/B07Y4GG7N5",
        "target_price": 3500,
        "site": "amazon"
    },
    {
        "name": "G.Skill Ripjaws 8GB 3200MHz RAM (Flipkart)",
        "url": "https://www.flipkart.com/g-skill-ripjaws-v-ddr4-8-gb-desktop-dram-f4-3200c16s-8gvkb/p/itme9g8gy6gwhm7g",
        "target_price": 3500,
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
    
    for item in ITEMS_TO_TRACK:
        try:
            response = requests.get(item["url"], headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            current_price = None
            
            if item["site"] == "amazon":
                price_element = soup.find(class_="a-price-whole")
                if price_element:
                    price_str = price_element.text.replace(',', '').replace('.', '').strip()
                    current_price = int(price_str)
                    
            elif item["site"] == "flipkart":
                price_element = soup.find(class_="Nx9w9m") or soup.find(class_="_10EHIb")
                if price_element:
                    price_str = price_element.text.replace('₹', '').replace(',', '').strip()
                    current_price = int(price_str)
            
            if current_price:
                print(f"{item['name']} Current Price: ₹{current_price}")
                
                if current_price <= item["target_price"]:
                    msg = f"🚨 PRICE DROP ALERT! 🚨\n\n{item['name']} ka price drop ho gaya hai!\nCurrent Price: ₹{current_price}\nTarget Price: ₹{item['target_price']}\n\nLink: {item['url']}"
                    requests.post(f"https://api.telegram.com/bot{TELEGRAM_TOKEN}/sendMessage", 
                                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
                    print(f"Alert sent for {item['name']}!")
            else:
                print(f"{item['name']} ka price tag nahi mila.")
                
        except Exception as e:
            print(f"Error checking {item['name']}:", e)

if __name__ == "__main__":
    check_price()
