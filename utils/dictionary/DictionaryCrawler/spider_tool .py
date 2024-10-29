import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import re


# 得到一个指定的网页url的内容
def ask_url(url):
    headers = {  # 模拟浏览器头部信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    # 用户代理：表示告诉服务器，我们是什么类型的机器，浏览器（本质上是告诉浏览器，我们可以接收什么样的文件内容）
    req = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = html + response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 返回一个词频的float列表
def get_frequency(phrase, start_year, end_year, lang, smoothing):
    baseurl = 'https://books.google.com/ngrams/graph?content=' + phrase.replace(' ',
                                                                                '+') + '&year_start=' + str(
        start_year) + '&year_end=' + str(end_year) + '&corpus=' + lang + '&smoothing=' + str(
        smoothing) + '&case_insensitive=true'
    print(baseurl)
    # 1.获取网页源码内容
    html = ask_url(baseurl)
    # 2.逐一解析数据
    frequencies = []
    soup = BeautifulSoup(html, "html.parser")

    f_all_string = soup.select('#ngrams-data')[0].get_text(strip=True)
    # 词频查找不到的词组，词频全部设为0
    if f_all_string == '[]':
        frequencies = [0] * (end_year + 1 - start_year)
    else:
        f_string = re.findall(re.compile(r'{(.*?)}', re.S), f_all_string)[0]
        frequency_list = re.findall(re.compile(
            r'[[](.*?)[]]', re.S), f_string)[0].split(',')
        for f in frequency_list:
            f = float(f.strip())
            # print(type(f), f)
            if type(f) != float:
                print('格式错误！', phrase)
            frequencies.append(f)
    return frequencies
