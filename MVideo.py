'''
Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины можно выбрать свои.
Главный критерий выбора: динамически загружаемые товары
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
import time

client = MongoClient('localhost', 27017)
db = client['mvideo_sale']
mvideo_db = db.mvideo_sale

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru')
wind = driver.find_element_by_class_name('wrapper')

time.sleep(1)
n = 0
try:
    menu = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-approve-city'][@href]")))
    menu.click()
    menu.send_keys(Keys.ENTER)
except:
    print('')

time.sleep(1)

buttons = driver.find_elements_by_xpath("//div[@class='gallery-layout']")
button = buttons[1]
button.click()

time.sleep(2)

n = 0
while True:
    try:
        time.sleep(2)
        list_sale = button.find_elements_by_xpath(".//li[@class='gallery-list-item height-ready']")
        for item in list_sale:
            my_dict = {}
            name = item.find_element_by_class_name('sel-product-tile-title').text
            my_dict['name'] = name
            price = item.find_element_by_class_name('c-pdp-price__current').text
            price = str(price.replace('¤', '').replace(' ', ''))
            if price.isdigit() == True:
                my_dict['price'] = price
            else:
                continue
            # new_price = item.find_element_by_class_name('u-font-bold c-pdp-price__trade-price')
            # print(new_price)
            mvideo_db.insert_one(my_dict)

        bclick = button.find_element_by_xpath(".//a[@class='sel-hits-button-next'][@href]")
        bclick.click()
        n += 1
    except:
        
        break

for i in mvideo_db.find():
    print(i)

driver.quit()
