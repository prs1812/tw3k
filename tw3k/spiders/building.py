import scrapy, os

import pandas as pd

from urllib.parse import urlparse, urlencode, parse_qs

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


class BuildingSpider(scrapy.Spider):
    name = 'building'

    def __init__(self):
        self.link = f'https://www.honga.net/totalwar/three_kingdoms/{self.name}.php?%s'
        self.meta = {'l': 'en'}

    # Read Playable Faction from file
    def start_requests(self):
        current_path = os.getcwd()
        # filePath = os.path.join(os.getcwd()+'/Data')
        # df = pd.read_excel(filePath+'/tw3k.xlsx', sheet_name='faction_en')
        # filtered_df = df[df['Playable'] == 1]
        # for index, row in filtered_df.iterrows():
        #     print(row['GameItemID']+'*********'+eval(row['FactionGroup']).get('en'))
        # self.meta['f'] = row['GameItemID']
        # yield Request(self.link % urlencode(self.meta), meta={'SubCulture': eval(row['FactionGroup']).get('en')})

        yield Request(
            'https://www.honga.net/totalwar/three_kingdoms/building.php?l=en&v=three_kingdoms&f=3k_main_faction_zhang_yan',
            meta={'FactionGroup': 'Bandits & Outlaws'})

    def parse(self, response, **kwargs):
        page = HtmlResponse(body=response.text, url=response.url, encoding='utf-8')

        response.meta.get('FactionGroup')

        table = page.xpath('.//div[@id="article_body"]').extract()[0]
        table = table.replace('\r', '').replace('\n', '').replace('\t', '')
        table = Selector(text=table)

        groups = [i.strip() for i in table.xpath('.//h3/text()').getall() if
                  len(i.strip()) > 1]
        print(sorted(groups))
