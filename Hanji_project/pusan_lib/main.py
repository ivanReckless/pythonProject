import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import json
from multiprocessing import Pool
import time
import ssl
import os


def get_url():
    url_list = []
    for i in tqdm(range(1, 67)):
        request_url = 'https://lib.pusan.ac.kr/resource/catalog/?app=solars&mod=list&request_query=a%253A2%253A%257Bs%253A12%253A%2522publish_year%2522%253Bs%253A14%253A%2522%255B1000%2BTO%2B1945%255D%2522%253Bs%253A5%253A%2522facet%2522%253Ba%253A2%253A%257Bi%253A0%253Ba%253A2%253A%257Bs%253A5%253A%2522field%2522%253Bs%253A13%253A%2522MATERIAL_TYPE%2522%253Bs%253A5%253A%2522value%2522%253Bs%253A8%253A%2522%25281%2BOR%2B7%2529%2522%253B%257Di%253A1%253Ba%253A2%253A%257Bs%253A5%253A%2522field%2522%253Bs%253A8%253A%2522LANGUAGE%2522%253Bs%253A5%253A%2522value%2522%253Bs%253A11%253A%2522%252878%2BOR%2B230%2529%2522%253B%257D%257D%257D&q_ti&q_au&q_pu&field_code=ALL&query&material%5B0%5D&language&publish_s_year&publish_e_year&record_per_page=100&orderby=relevance&order=asc&facet&remove_query&add_action=page&page_number=' + str(i)
        url = urllib.request.urlopen(request_url)
        res = BeautifulSoup(url, 'html.parser', from_encoding='utf8').find_all('strong', class_='title')
        for content in res:
            research_content = r'href=\"(.*?)\"\>'
            result = re.findall(research_content, str(content))
            for result_url in result:
                url_list.append(result_url)
    with open('url.file', 'w', encoding='utf8') as fp:
        for url in url_list:
            fp.write(url.split('&amp;beforelink')[0].replace('amp;', '') + '\n')


def divide_url_list(num):
    url_list = []
    for i in open('url.file'):
        url_list.append(i)
    mono_list = [[] for i in range(num)]
    for i, e in enumerate(url_list):
        mono_list[i % num].append(e)
    return mono_list


def main1(thread):
    all_url = divide_url_list(num=thread)
    p = Pool(thread)
    for index, url_list in enumerate(all_url):
        p.apply_async(get_target_inf, args=(url_list, index))
    p.close()
    p.join()
    # for index, url_list in enumerate(all_url):
    #     get_target_inf(url_list, index)


def get_target_inf(url_list, index):
    title_dict = {}
    for url in tqdm(url_list):
        url = urllib.request.urlopen(url)
        res = BeautifulSoup(url, 'html.parser', from_encoding='utf8').find_all('dl', class_='rd-list colon info')
        result_list = []
        for content in str(res).split('/dd>'):
            research_content = r'\>(.*?)\<'
            result = re.findall(research_content, str(content))
            while '' in result:
                result.remove('')
            if len(result) <= 0:
                continue
            if len(result) > 2:
                result = [result[0], '-'.join(result[1: -1])]
            if result[0] not in title_dict:
                title_dict[result[0]] = len(title_dict)
            result_list.append(result)
        json.dump(title_dict, open('title.dict.json', 'w'))
        write_target_inf(result_list, title_dict, index)


def write_target_inf(result_list, title_dict, index):
    write_line = [''] * len(title_dict)
    for line in result_list:
        if len(line) > 1:
            line[1] = line[1].replace(',', '，')
            ind = title_dict[line[0]]
            write_line[ind] = line[1]
    with open(str(index) + '.test.csv', 'a', encoding='utf8') as fp:
        fp.write(','.join(write_line) + '\n')


if __name__ == '__main__':
    # get_url()
    main1(thread=4)
