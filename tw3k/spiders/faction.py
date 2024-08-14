import scrapy
from urllib.parse import urlparse, urlencode, parse_qs
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

from tw3k.items import FacItem


class FactionSpider(scrapy.Spider):
    name = 'faction'

    def __init__(self, *args, **kwargs):
        self.link = f'https://www.honga.net/totalwar/three_kingdoms/{self.name}.php?%s'
        self.meta = {'l': 'en'}

        # Check Language
        super(FactionSpider, self).__init__(*args, **kwargs)
        if 'l' in self.meta and kwargs.get('l') == 'zh-CN':
            self.meta['l'] = 'zh-CN'

    def start_requests(self):
        start_urls = [self.link % urlencode(self.meta)]

        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        page = HtmlResponse(body=response.text, url=response.url, encoding='utf-8')

        for i in page.xpath('.//a[@class="break_word"]/@href').getall():
            yield Request('https://www.honga.net/totalwar/three_kingdoms/' + i, callback=self.getFacInfo)

    def getFacInfo(self, response):
        facItem = FacItem()
        translator = str.maketrans({chr(10): '', chr(9): ''})
        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)

        page = HtmlResponse(body=response.text, url=response.url, encoding='utf-8')

        # Faction Year and Description
        article = page.xpath('..//div[@id="article_body"]').extract()[0]

        # Remove space in str
        article = article.replace('\r', '').replace('\n', '').replace('\t', '')
        article = Selector(text=article)

        # Get Playerable Year
        year = [i for i in article.xpath('.//h3/text()').getall()]

        # Background
        cnt = [i.strip() for i in article.xpath('.//div/text()').getall()
               if len(i.strip()) > 1][:len(year)]

        # Faction Meta Info
        table = page.xpath('.//table[@class="table_stat"]').extract()[0]

        # Remove comment tags in html
        table = table.replace('<!--', '').replace('-->', '')
        table = table.translate(translator)

        facMetaInfo = []

        for i in Selector(text=table).xpath('.//td'):
            if i.xpath('./p/text()').get() == None:
                pass
            else:
                facMetaInfo.append(i.xpath('./text()').get())
        # print(facMetaInfo[6])
        # pass
        facItem['GameItemID'] = query_params.get('f')[0]
        facItem['FactionName'] = {self.meta['l']: facMetaInfo[0]}
        facItem['FactionLeader'] = {self.meta['l']: facMetaInfo[1]}
        facItem['Campaign'] = facMetaInfo[2]
        facItem['Culture'] = {self.meta['l']: facMetaInfo[3]}
        facItem['SubCulture'] = {self.meta['l']: facMetaInfo[4]}
        facItem['MilitaryGroup'] = facMetaInfo[5]
        facItem['FactionGroup'] = {self.meta['l']: facMetaInfo[6]}
        facItem['Playable'] = facMetaInfo[7]
        facItem['PoliticalParty'] = facMetaInfo[8]
        facItem['Year'] = {self.meta['l']: year}
        facItem['Description'] = {self.meta['l']: dict(zip(year, cnt))}

        yield facItem
        del facItem
