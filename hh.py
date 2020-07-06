from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
from pymongo import MongoClient

name = input('введите вакансию: ')
client = MongoClient('localhost', 27017)
db = client['vacancys_db']
search_link = '/search/vacancy'
vacancys = db.vacancys

lnum = 0
n = 0
res_min = []
res_max = []
page = 0
b = []
res = []
vacancy = []
vcid = []
while True:

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            ' Chrome/81.0.4044.138 YaBrowser/20.6.2.195 Yowser/2.5 Safari/537.36', 'Accept': '*/*'}

    mail_link = 'https://hh.ru/'

    params = {'L_is_autosearch': 'false', 'clusters': 'true', 'area': '1', 'enable_snipets': 'true',
              'st': 'searchVacancy', 'text': name,
              'fromSearch': 'true', 'from': 'suggest_post', 'page': page}
    # https://hh.ru/search/vacancy?&area=1&clusters=true&enable_snippets=true&text=Python&page=1

    response = requests.get(mail_link + search_link, headers=header, params=params).text
    soup = bs(response, 'html.parser')

    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})

    vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})

    for vac in vacancy_list:

        vacancy_data = {}

        vacancy_name = vac.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).getText()
        vacancy_url = vac.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']

        vacancy_salary = vac.find('div', {'vacancy-serp-item__sidebar'}).getText()
        curr = vacancy_salary.split()

        # print(vacancy_url)
        try:
            for i in vacancy_salary.split('-'):
                for j in i:
                    if j.isdigit() == True:
                        b.append(j)
                b = list(''.join(b))
                res.append(int(''.join(b)))
                b = []
            if len(res) == 2:
                res_min.append(res[0])
                res_max.append(res[1])
            elif len(res) == 1:
                res_min = res
        except (ValueError, AttributeError):
            res = 'зарплата не указана'
        try:
            if res == 'зарплата не указана':
                vacancy_main_url = mail_link

                vacancy_data['name'] = vacancy_name
                vacancy_data['url'] = vacancy_url
                vacancy_data['salary_max'] = None
                vacancy_data['salary_min'] = None
                vacancy_data['main_url'] = vacancy_main_url
                vacancy_data['vacancyId'] = vacancy_data['url'][30:38]
                vacancys.insert_one({'name': vacancy_data['name'],
                                     '_id': vacancy_data['vacancyId'],
                                     'salary_min': vacancy_data['salary_min'],
                                     'salary_max': vacancy_data['salary_max'],
                                     'main_url': vacancy_data['main_url'],
                                     'url': vacancy_data['main_url']})
            elif len(res) == 1 and vacancy_salary.split()[0].lower() == 'до':

                vacancy_main_url = mail_link
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_max'] = res[0]
                vacancy_data['salary_min'] = None
                vacancy_data['currency'] = curr[-1]
                vacancy_data['url'] = vacancy_url
                vacancy_data['main_url'] = vacancy_main_url
                vacancy_data['vacancyId'] = vacancy_url[30:38]
                vacancys.insert_one({'name': vacancy_data['name'],
                                     '_id': vacancy_data['vacancyId'],
                                     'salary_min': vacancy_data['salary_min'],
                                     'salary_max': vacancy_data['salary_max'],
                                     'main_url': vacancy_data['main_url'],
                                     'url': vacancy_data['main_url']})
            elif len(res) == 1 and vacancy_salary.split()[0].lower() == 'от':

                vacancy_main_url = mail_link
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_max'] = None
                vacancy_data['salary_min'] = res[0]
                vacancy_data['currency'] = curr[-1]
                vacancy_data['url'] = vacancy_url
                vacancy_data['vacancyId'] = vacancy_url[30:38]
                vacancy_data['main_url'] = vacancy_main_url
                vacancys.insert_one({'name': vacancy_data['name'],
                                     '_id': vacancy_data['vacancyId'],
                                     'salary_min': vacancy_data['salary_min'],
                                     'salary_max': vacancy_data['salary_max'],
                                     'currency': vacancy_data['currency'],
                                     'main_url': vacancy_data['main_url'],
                                     'url': vacancy_data['main_url']})
            else:

                vacancy_main_url = mail_link
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_max'] = res_max
                vacancy_data['salary_min'] = res_min
                vacancy_data['currency'] = curr[-1]
                vacancy_data['url'] = vacancy_url
                vacancy_data['vacancyId'] = vacancy_url[30:38]
                vacancy_data['main_url'] = vacancy_main_url
                vacancys.insert_one({'name': vacancy_data['name'],
                                     '_id': vacancy_data['vacancyId'],
                                     'salary_min': vacancy_data['salary_min'],
                                     'salary_max': vacancy_data['salary_max'],
                                     'currency': vacancy_data['currency'],
                                     'main_url': vacancy_data['main_url'],
                                     'url': vacancy_data['main_url']})
        except:
            continue
        vacancy.append(vacancy_data)


        res = []
        res_max = []
        res_min = []

        lnum += 1
    page += 1

    try:
        next_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText()


    except:
        print(f'Всего занесенно {lnum} записей c hh.ru')
        break

# my_dict = dict(vacancy)
# print(vacancy)
# vacancys.insert_many(vacancy, {'_id': vcid})


# table_pd = pd.DataFrame(vacancy)
# table_mg = table_pd.to_dict()


# print(table_pd[['name', 'salary_min', 'vacancyId']])

# table_pd.to_csv("hhvacancy.csv")
