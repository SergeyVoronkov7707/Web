import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from scrapy.loader import ItemLoader


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'helloworld202202202'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595181861:AZJQAHiYqu1OORL/uFxykGUwIjVb/q8iWIHH4d+1NQPz1IAu9ppEM5IXO3YLKtjhK5lZb0LEFZs/e7bIqXitLF3uaCg4wG3oNIeB0bukO9lwgEEdSJA2dgK+kRLZNgULMk4HtKezZykVp6nuD51DuA=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['python.learning', '__pythonworld__']


    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscrip_hash = ['d04b0a864b4b54837c0d870b0e77e076', 'c76146de99bb02f6415203be841dd25a']



    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': self.fetch_csrf_token(response.text)}

        )

    def user_parse(self, response: HtmlResponse):
        try:
            j_body = json.loads(response.text)
            if j_body['authenticated']:
                for value in self.parse_user:
                    yield response.follow(
                        f'/{value}',
                        callback=self.user_data_parse,
                        cb_kwargs={'username': value},

                    )
        except Exception as e:
            print(f'user_parse{e}')

    def user_data_parse(self, response: HtmlResponse, username):
        try:
            user_id = self.fetch_user_id(response.text, username)
            variables = {'id': user_id,
                         'first': 10}
            for value in self.subscrip_hash:
                if value == 'd04b0a864b4b54837c0d870b0e77e076':
                    url_subscrip = f'{self.graphql_url}query_hash={value}&{urlencode(variables)}'
                    yield response.follow(
                        url_subscrip,
                        callback=self.user_posts_parse,
                        cb_kwargs={'username': username,
                                   'user_id': user_id,
                                   'variables': deepcopy(variables)}
                    )
                else:
                    url_subscrip_d = f'{self.graphql_url}query_hash={value}&{urlencode(variables)}'
                    if url_subscrip_d:
                        yield response.follow(
                            url_subscrip_d,
                            callback=self.user_sub_parse,
                            cb_kwargs={'username': username,
                                       'user_id': user_id,
                                       'variables': deepcopy(variables)}
                        )
        except Exception as e:
            print(f'user_data_parse{e}')

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):

        try:
            j_data = json.loads(response.text)
            page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
            if page_info.get('has_next_page'):

                variables['after'] = page_info['end_cursor']
                url_posts = f'{self.graphql_url}query_hash={self.subscrip_hash[0]}&{urlencode(variables)}'
                yield response.follow(
                    url_posts,
                    callback=self.user_posts_parse,
                    cb_kwargs={'username': username,
                               'user_id': user_id,
                               'variables': deepcopy(variables)}
                )

                posts = j_data.get('data').get('user').get('edge_follow').get('edges')

                for post in posts:
                    item = InstaparserItem(
                        user_id=user_id,
                        name_subscription=post['node']['username'],
                        photo_subscription=post['node']['profile_pic_url'],
                        id_subscription=post['node']['id'],
                        name=username,
                        section='подписка'

                    )
                    yield item
            else:
                pass


        except Exception as e:
            print(f'user_posts_parse {e}')

    def user_sub_parse(self, response: HtmlResponse, username, user_id, variables):

        try:
            j_data = json.loads(response.text)
            page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')

            if page_info.get('has_next_page'):

                variables['after'] = page_info['end_cursor']
                url_posts = f'{self.graphql_url}query_hash={self.subscrip_hash[1]}&{urlencode(variables)}'
                yield response.follow(
                    url_posts,
                    callback=self.user_sub_parse,
                    cb_kwargs={'username': username,
                               'user_id': user_id,
                               'variables': deepcopy(variables)}
                )

                sub = j_data.get('data').get('user').get('edge_followed_by').get('edges')

                for post in sub:
                    item = InstaparserItem(
                        user_id=user_id,
                        name_subscription=post['node']['username'],
                        photo_subscription=post['node']['profile_pic_url'],
                        id_subscription=post['node']['id'],
                        name=username,
                        section='подписчик'
                    )
                    yield item
            else:
                pass
        except Exception as e:
            print(f'user_sub_parse {e}')

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
