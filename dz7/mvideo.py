from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
# from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError

# client = MongoClient('127.0.0.1', 27017)
# db = client['db_mvideo']
# mvideo_in_trend_goods = db.mvideo_in_trend_goods

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(4)
# driver.maximize_window()
driver.get('https://www.mvideo.ru/')

step = 500
while True:
    driver.execute_script(f"window.scrollTo(0, {step})")
    step += 500
    try:
        if driver.find_element(By.XPATH, "//span[contains(text(), 'В тренде')]"):
            in_trend_button = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
            in_trend_button.click()
        break
    except:
        pass

print()


goods = driver.find_elements(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]')

names = [i.text for i in goods[0].find_elements(By.XPATH, ".//div[@class='product-mini-card__name ng-star-inserted']")]
prices = [int(i.text[0:i.text.find('₽')].replace(' ', '')) for i in goods[0].find_elements(By.XPATH, ".//div[@class='product-mini-card__price ng-star-inserted']")]
links = [i.get_attribute('href') for i in goods[0].find_elements(By.XPATH, ".//div[@class='product-mini-card__name ng-star-inserted']//a")]
print(len(names))
in_trend_goods = {'_id': [],
                  'name': [],
                  'price': [],
                  'link': []
                  }
for i in range(len(names)):
    in_trend_goods['_id'].append(links[i]),
    in_trend_goods['name'].append(names[i]),
    in_trend_goods['price'].append(prices[i]),
    in_trend_goods['link'].append(links[i])

with open('result.json', 'w') as f:
    json.dump(in_trend_goods, f)
#     try:
#         mvideo_in_trend_goods.insert_one(in_trend_goods)
#     except DuplicateKeyError:
#         print(f'товар {names[i]} уже есть в базе')
