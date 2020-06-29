from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd

name = 'it'
page = 3
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/81.0.4044.138 YaBrowser/20.6.2.195 Yowser/2.5 Safari/537.36', 'Accept': '*/*'}

mail_link = 'https://www.superjob.ru/'

response = requests.get(mail_link + f'vacancy/search/?keywords={name}&geo%5Bt%5D%5B0%5D=4&page={page}',
                        headers=header)

soup = bs(response.text, 'html.parser')

vacancy_block = soup.find('div', {'class': '_1ID8B'})

vacancy_list = vacancy_block.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL'})

res_min = []
res_max = []

b = []
res = []
vacancy = []

for vac in vacancy_list:
    vacancy_data = {}
    vacancy_name = vac.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).getText()  # _3mfro PlM3e _2JVkc _3LJqf
    vacancy_url = mail_link + vac.find('a')['href']
    vacancy_salary = vac.find('span', {'_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
    curr = vacancy_salary.split()
    try:
        for i in vacancy_salary.split('—'):
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
    res = []
    res_max = []
    res_min = []

table_pd = pd.DataFrame(vacancy)
pprint(table_pd[['name', 'salary_min', 'currency']])
