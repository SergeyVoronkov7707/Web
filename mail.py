'''
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client['mail']
news_db = db.mail

# news_db.delete_many({})
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept': '*/*'}

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver')
driver.get(
    'https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%2F&allow_external=1&from=octavius')

login = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'username')))

time.sleep(0.5)
login.send_keys('study.ai_172')
time.sleep(0.5)
login.send_keys(Keys.ENTER)
time.sleep(0.5)

login = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'password')))

login.send_keys('NextPassword172')
time.sleep(0.5)
login.send_keys(Keys.ENTER)

n = 0
login = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'llc__container')))
login.click()
while True:
    try:
        mail_new = {}
        time.sleep(0.5)
        text = driver.find_element_by_class_name('letter-body').text
        time.sleep(0.5)
        autor = driver.find_element_by_class_name('letter-contact').text
        time.sleep(0.5)
        date_time = driver.find_element_by_class_name('letter__date').text

        time.sleep(0.5)
        mail_new['autor'] = autor
        time.sleep(0.5)
        mail_new['time'] = date_time
        time.sleep(0.5)

        time.sleep(0.5)
        mail_new['text'] = str(text).replace('\n', ' ')
        pprint(mail_new)

        news_db.insert_one(mail_new)
        n += 1

        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(1)
    except:
        print(f'обработано {n} писем')
        break
driver.quit()
