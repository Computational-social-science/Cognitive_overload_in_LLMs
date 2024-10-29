import scrapy
from bs4 import BeautifulSoup
from DictionaryCrawler.items import GBNCItem
from DictionaryCrawler.utils import get_latin_phrases, clean_file
import os
import re


current_path = os.getcwd()
print(current_path)

clean_file('./spiders/data/spider.csv')
# words = ['de facto', 'ut dictum']
words = get_latin_phrases(
    './spiders/data/English/top 3000  English words.txt')[:200]
print(words)
base_url = 'https://books.google.com/ngrams/graph?content='


class OxfordSpider(scrapy.Spider):
    name = "gbnc"
    allowed_domains = ["books.google.com"]
    start_urls = [base_url + word.replace(
        ' ', '+') + '&year_start=1500&year_end=2019&corpus=en-2019&smoothing=0&case_insensitive=true' for word in words]

    def parse(self, response):
        item = GBNCItem()
        print(response.url)
        start_year, end_year = 1500, 2019

        word = str(response.url).replace(base_url, '').replace(
            '&year_start=1500&year_end=2019&corpus=en-2019&smoothing=0&case_insensitive=true', '').replace('+', ' ')
        item['word'] = word

        # 使用BeautifulSoup解析html内容
        soup = BeautifulSoup(response.body, 'html.parser')
        frequencies = []
        f_all_string = soup.select('#ngrams-data')[0].get_text(strip=True)
        # 词频查找不到的词组，词频全部设为0
        if f_all_string == '[]':
            frequencies = [0] * (end_year + 1 - start_year)
        else:
            f_string = re.findall(re.compile(
                r'{(.*?)}', re.S), f_all_string)[0]
            frequency_list = re.findall(re.compile(
                r'[[](.*?)[]]', re.S), f_string)[0].split(',')
            for f in frequency_list:
                f = float(f.strip())
                # print(type(f), f)
                if type(f) != float:
                    print('格式错误！', word)
                frequencies.append(f)
        item['frequencies'] = frequencies
        yield item

# run in cmd: scrapy crawl gbnc -o ./spiders/data/spider.csv
