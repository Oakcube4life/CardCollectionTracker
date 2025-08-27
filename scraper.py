#As the title suggests, this if for scraping the pricecharting.com website
import requests
from bs4 import BeautifulSoup

def build_card_url(name, set_name, card_number):
    # Convert spaces to hyphens and lowercase everything (depends on site)
    name_slug = name.replace(" ", "-").lower()
    set_slug = set_name.replace(" ", "-").lower()
    number_slug = card_number.split("/")[0]
    
    url = f"https://www.pricecharting.com/game/pokemon-{set_slug}/{name_slug}-{number_slug}"
    return url

#combine these to reduce the ammount of calls to the site
def get_card_price(name, set_name, card_number):

    url = build_card_url(name, set_name, card_number)

    headers = {
        "User-Agent": "Mozilla/5.0"  # pretend to be a browser
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    
    # Example: find price in HTML
    price_element = soup.find("span", class_="price js-price")
    if price_element:
        price_text = price_element.get_text(strip=True)
        #CONVERT TO CAD?
        # Remove $ sign and convert to float
        return float(price_text.replace("$", "").replace(",", ""))
    return None

def get_img_link(name, set_name, card_number):

    url = build_card_url(name, set_name, card_number)

    headers = {
        "User-Agent": "Mozilla/5.0"  # pretend to be a browser
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # Example: find price in HTML
    img_element = soup.find("img", class_="js-show-dialog")
    if img_element:
        img_link = img_element["src"] if img_element else None
        #CONVERT TO CAD?
        # Remove $ sign and convert to float
        return img_link
    return None