# 获取需要爬取的拉丁词词组
import os
import pandas as pd


def clean_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('')
    file.close()


def get_latin_phrases(file_path):
    latin_phrases = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            latin_phrases.append(line.strip())
    file.close()
    return latin_phrases


def get_phrases_from_csv(file_path):
    return list(pd.read_csv(file_path)['phrase'])


def main():
    current_path = os.getcwd()
    print(current_path)

    latin_phrases = get_latin_phrases(
        './utils/Dictionary/DictionaryCrawler/spiders/data/latin phrases v2.0.txt')
    print(latin_phrases[-10:])

    # clean_file('./utils/Dictionary/DictionaryCrawler/spiders/data/spider.csv')


if __name__ == '__main__':
    main()
