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


def get_url_id():
    url_id_list = []
    for i in tqdm(range(1, 65)):
        url = urllib.request.urlopen('https://lib.daegu.ac.kr/search/tot/result?pn=' + str(i) + '&commandType=advanced&lmtsn=000000000001&lmtsn=000000000003&lmtsn=000000000006&range=000000000021&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&rf=&inc=TOTAL&b0=and&b1=and&lmtst=OR&lmtst=OR&lmtst=FRNT&st=KWRD&oi=&msc=500&os=&cpp=50&lmt0=TOTAL&lmt2=TOTAL&lmt1=TOTAL&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&si=1&si=2&si=3&weight2=&weight0=&weight1=&q=%EF%BC%9F&q=&q=&bk_0=jttjmjttj&rt=1945')
        soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
        res = soup.find_all('dd', class_='searchTitle')
        for content in res:
            research_content = r'href=\"(.*?)\?mainLink'
            url_id = re.findall(research_content, str(content))
            for id_num in url_id:
                url_id_list.append(id_num)
    with open('url_id.file', 'w', encoding='utf8') as fp:
        for i in url_id_list:
            fp.write(i + '\n')


def gen_url():
    url_list = []
    for i in open('url_id.file'):
        url = 'https://lib.daegu.ac.kr' + i
        url_list.append(url)
    with open('url.file', 'w', encoding='utf8') as fp:
        for i in url_list:
            fp.write(i)


def divide_url(num):
    url_list = []
    for i in open('url.file'):
        url_list.append(i)
    mono_list = [[] for i in range(num)]
    for i, e in enumerate(url_list):
        mono_list[i % num].append(e)
    return mono_list


def main1(thread):
    all_url = divide_url(num=thread)
    p = Pool(thread)
    for index, url_list in enumerate(all_url):
        p.apply_async(get_target_inf, args=(url_list, index))
    p.close()
    p.join()


def get_target_inf(url_list, index):
    title_dict = {}
    for target_url in tqdm(url_list):
        url = urllib.request.urlopen(target_url)
        res = BeautifulSoup(url, 'html.parser', from_encoding='utf8').find_all('table', class_='profiletable')
        result_list = []
        for content in str(res).split('<tr>'):
            if 'th' in content:
                research_content = r'(?<=>).*?(?=<)'
                result = re.findall(research_content, str(content))
                while '' in result:
                    result.remove('')
                if len(result) > 2:
                    result = [result[0], '-'.join(result[1:-1])]
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
    # get_url_id()
    # gen_url()
    main1(thread=8)