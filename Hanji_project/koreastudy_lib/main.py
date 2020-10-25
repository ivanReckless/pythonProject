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


def get_html(id_list, index, save_dir='html/'):
    for i in tqdm(id_list):
        url = 'http://search.koreastudy.or.kr/search/view?searchKeyword=%E8%A7%A3&searchCondition=FORM_TYPE-0-1&pageIndex=1&schc_data_bnd_id=0000000' + str(
            '%05d' % i)
        res = requests.get(url).content
        with open(save_dir + str(index) + '-' + str(i) + '-' + 'test.html', 'wb') as fp:
            fp.write(res)


def main1(thread):
    all_list = []
    for i in range(1, 100000):
        all_list.append(i)
    mono_list = [[] for i in range(thread)]
    for i, e in enumerate(all_list):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, id_list in enumerate(mono_list):
        p.apply_async(get_html, args=(id_list, index))
    p.close()
    p.join()


if __name__ == '__main__':
    main1(thread=32)
    # get_html()