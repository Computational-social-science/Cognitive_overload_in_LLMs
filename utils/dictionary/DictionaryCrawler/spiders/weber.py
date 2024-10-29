import scrapy
from bs4 import BeautifulSoup
from DictionaryCrawler.items import WeberItem
from DictionaryCrawler.utils import get_latin_phrases, clean_file, get_phrases_from_csv
import os


current_path = os.getcwd()
# print(current_path)

clean_file('./spiders/data/spider.csv')
# words = ['ut dictum', 'de facto', 'res ipsa loquitur']
words = get_phrases_from_csv('./spiders/data/English/English phrases.csv')
# print(words)
base_url = "https://www.merriam-webster.com/dictionary/"


class WeberrSpider(scrapy.Spider):
    name = "weber"
    allowed_domains = ["www.merriam-webster.com"]
    start_urls = [base_url + word.replace(' ', '%20') for word in words]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.handle_error, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'})

    def parse(self, response):
        item = WeberItem()
        print(response.url)
        # phrase = str(response.url).replace(base_url, '').replace('%20', ' ')
        phrase = str(response.url).split('/')[-1].replace('%20', ' ')
        item['phrase'] = phrase
        # 获取状态码
        status_code = response.status
        if status_code == 200:
            # 处理成功的响应
            item['inDict'] = 1
        yield item

    def handle_error(self, failure):
        response = failure.value.response
        item = WeberItem()
        print(response.url)
        # phrase = str(response.url).replace(base_url, '').replace('%20', ' ')
        phrase = str(response.url).split('/')[-1].replace('%20', ' ')
        item['phrase'] = phrase

        response = failure.value.response
        if response.status == 404:
            item['inDict'] = 0
        yield item


# run in cmd: scrapy crawl weber -o ./spiders/data/spider.csv
