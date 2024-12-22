import requests
import os
from bs4 import BeautifulSoup as bs
from database import async_session, create_item
from dotenv import load_dotenv

load_dotenv()
page = requests.get('https://www.mvideo.ru/naushniki-54/naushniki-3967?f_tolko-v-nalichii=da&f_brand=akg,apple,audio-technica,beyerdynamic,bose,jbl,logitech,marshall,sony&showCount=24')
soup = bs(page.text, 'html.parser')
all_items = soup.findAll('div', class_='product-cards-layout__item ng-star-inserted')
print(all_items)

for item in all_items:
    data = item.find('div', class_='product-card--list__description')
    item_name = data.find('a', class_='product-title__text')
    print(item_name)

