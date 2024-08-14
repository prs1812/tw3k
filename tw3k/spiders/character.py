import scrapy
from urllib.parse import urlencode
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

from tw3k.items import CharItem


class CharacterSpider(scrapy.Spider):
    name = "character"

    # Initilized Parameters
    def __init__(self, *args, **kwargs):
        self.link = f'https://www.honga.net/totalwar/three_kingdoms/{self.name}.php?'
        self.meta = {'l': 'en', 'page': 1}

        # Check Language
        super(CharacterSpider, self).__init__(*args, **kwargs)
        if 'l' in self.meta and kwargs.get('l') == 'zh-CN':
            self.meta['l'] = 'zh-CN'

    def start_requests(self):
        for i in range(1, 54):
            self.meta['page'] = i
            yield Request(url=self.link + urlencode(self.meta))

    def parse(self, response, **kwargs):
        page = HtmlResponse(body=response.text, url=response.url, encoding='utf-8')
        table = page.xpath('.//tbody').extract()[0]
        # Remove \n or \t from a given string

        translator = str.maketrans({chr(10): '', chr(9): ''})
        table = table.translate(translator)

        # Remove comment tags in html
        table = table.replace('<!-- ', '').replace(' -->', '')
        for i in Selector(text=table).xpath('.//tr'):
            char_info = [j for j in i.xpath('td/text()').getall()]
            chrItem = CharItem()
            if len(char_info) == 11:
                chrItem['GameItemID'] = char_info[0]
                chrItem['FamilyName'] = {'en': char_info[1]}
                chrItem['GivenName'] = {'en': char_info[2]}
                chrItem['FullName'] = {'en': char_info[1] + ' ' + char_info[2]}
                chrItem['CourtesyName'] = {'en': char_info[3]}
                chrItem['BirthYear'] = char_info[4]
                chrItem['Gender'] = {'en': char_info[5]}
                chrItem['ArtSet'] = char_info[7]
                chrItem['Type'] = char_info[8]
                chrItem['FaceSet'] = char_info[9]

            elif len(char_info) == 10:

                chrItem['GameItemID'] = char_info[0]
                chrItem['FamilyName'] = {'en': char_info[1]}
                chrItem['GivenName'] = {'en': char_info[2]}
                chrItem['FullName'] = {'en': char_info[1] + ' ' + char_info[2]}
                chrItem['BirthYear'] = char_info[3]
                chrItem['Gender'] = {'en': char_info[4]}
                chrItem['ArtSet'] = char_info[6]
                chrItem['Type'] = char_info[7]
                chrItem['FaceSet'] = char_info[8]

            else:

                chrItem['GameItemID'] = char_info[0]
                chrItem['FamilyName'] = {'en': None}
                chrItem['FullName'] = {'en': char_info[1]}
                chrItem['BirthYear'] = char_info[2]
                chrItem['Gender'] = {'en': char_info[3]}
                chrItem['ArtSet'] = char_info[4]
                chrItem['Type'] = char_info[5]
                chrItem['FaceSet'] = char_info[6]
            print('_____________________')

            yield chrItem
            del chrItem
