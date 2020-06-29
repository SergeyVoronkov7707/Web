from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://www.kinopoisk.ru'
response = requests.get(main_link + '/popular/films/?quick_filters=serials&tab=all').text
soup = bs(response,'html.parser')

serials_block = soup.find('div',{'class':'selection-list'})

serials_list = serials_block.find_all('div',{'class':'desktop-rating-selection-film-item'})
# serials_list = serials_block.findChildren(recursive=False)

# pprint(len(serials_list))
serials = []
for serial in serials_list:
    serial_data = {}
    serial_name = serial.find('p').getText()
    serial_link = main_link + serial.find('a',{'class':'selection-film-item-meta__link'})['href']
    serial_genre = serial.find_all('span',{'class':'selection-film-item-meta__meta-additional-item'})[-1].getText()
    serial_rating = serial.find('span',{'class':'rating__value'})
    if serial_rating:
        serial_rating = serial_rating.getText()
    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['genre'] = serial_genre
    serial_data['rating'] = serial_rating
    serials.append(serial_data)

pprint(serials)