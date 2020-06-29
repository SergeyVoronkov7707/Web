from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd

name = 'it'
page = 0
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/81.0.4044.138 YaBrowser/20.6.2.195 Yowser/2.5 Safari/537.36', 'Accept': '*/*'}

mail_link = 'https://hh.ru/'

response = requests.get(mail_link + f'search/vacancy?clusters=true&enable_snippets=true&salary=&'
                                    f'st=searchVacancy&text={name}&fromSearch=true&page={page}',
                        headers=header)

soup = bs(response.text, 'html.parser')

vacancy_block = soup.find('div', {'class': 'vacancy-serp'})

vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})

res_min = []
res_max = []

b = []
res = []
vacancy = []
for vac in vacancy_list:
    vacancy_data = {}
    vacancy_name = vac.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).getText()
    vacancy_url = mail_link + vac.find('a')['href']
    vacancy_salary = vac.find('div', {'vacancy-serp-item__sidebar'}).getText()
    curr = vacancy_salary.split()
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

    if res == 'зарплата не указана':
        vacancy_main_url = mail_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['url'] = vacancy_url
        vacancy_data['salary_max'] = None
        vacancy_data['salary_min'] = None
        vacancy_data['main_url'] = vacancy_main_url
    elif len(res) == 1 and vacancy_salary.split()[0].lower() == 'до':

        vacancy_main_url = mail_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary_max'] = res[0]
        vacancy_data['salary_min'] = None
        vacancy_data['currency'] = curr[-1]
        vacancy_data['url'] = vacancy_url
        vacancy_data['main_url'] = vacancy_main_url
    elif len(res) == 1 and vacancy_salary.split()[0].lower() == 'от':

        vacancy_main_url = mail_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary_max'] = None
        vacancy_data['salary_min'] = res[0]
        vacancy_data['currency'] = curr[-1]
        vacancy_data['url'] = vacancy_url
        vacancy_data['main_url'] = vacancy_main_url
    else:

        vacancy_main_url = mail_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary_max'] = res_max
        vacancy_data['salary_min'] = res_min
        vacancy_data['currency'] = curr[-1]
        vacancy_data['url'] = vacancy_url
        vacancy_data['main_url'] = vacancy_main_url
    vacancy.append(vacancy_data)
    # print(res_min[0])
    res = []
    res_max = []
    res_min = []

table_pd = pd.DataFrame(vacancy)

pprint(table_pd[['name', 'salary_min', 'salary_max', 'currency']])
