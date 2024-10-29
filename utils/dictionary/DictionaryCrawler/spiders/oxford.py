import scrapy
from bs4 import BeautifulSoup
from DictionaryCrawler.items import OxfordItem
from DictionaryCrawler.utils import get_latin_phrases, clean_file, get_phrases_from_csv
import os

current_path = os.getcwd()
print(current_path)

clean_file('./spiders/data/spider.csv')
# words = ['de facto', 'ut dictum']
# words = get_latin_phrases('./spiders/data/latin phrases v2.0.txt')
words = get_phrases_from_csv('./spiders/data/English/English phrases.csv')
print(words)
base_url = "https://www.oed.com/search/dictionary/?scope=Entries&q="


class OxfordSpider(scrapy.Spider):
    name = "oxford"
    allowed_domains = ["www.oed.com"]
    start_urls = [base_url + word.replace(' ', '+') for word in words]

    def parse(self, response):
        item = OxfordItem()
        print(response.url)
        phrase = str(response.url).replace(base_url, '').replace('+', ' ')
        item['phrase'] = phrase
        # 使用BeautifulSoup解析html内容
        soup = BeautifulSoup(response.body, 'html.parser')
        result = soup.select_one('div.searchSummary').get_text().strip()
        inOxford = 1
        if '0 result' in result:
            inOxford = 0
        item['inDict'] = inOxford
        yield item

# run in cmd: scrapy crawl oxford -o ./spiders/data/spider.csv
