import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):

    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'voronkov7707@mail.ru'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595171193:AdVQAN7d7TLgKJIE2XPaEiWAW8qTbA5GvkGJqtLivj56cqkCMAYkwBoiQtH/TalwClDal6gKcQDr1I4vB6PpL5nQuBiCfttTut3mKhpmhRJ2V6Fps9EO/8a6KCoACLBoCvdPnwTzZnzokLYBGFPGRxjz1A=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'python.hunt'
    #
    # graphql_url = 'https://www.instagram.com/graphql/query/?'
    # posts_hash = '15bf78a4ad24e33cbd838fdb31353ac1'     #hash для получения данных по постах с главной страницы

    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        # csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken': self.fetch_csrf_token(response.text)}

        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}

            )

    def user_data_parse(self, response: HtmlResponse, username):
        print(1)
        # user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        # variables = {'id': user_id,  # Формируем словарь для передачи даных в запрос
        #              'first': 12}  # 12 постов. Можно больше (макс. 50)
        # url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о постах
        # yield response.follow(
        #     url_posts,
        #     callback=self.user_posts_parse,
        #     cb_kwargs={'username': username,
        #                'user_id': user_id,
        #                'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        # )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')