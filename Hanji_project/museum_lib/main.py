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


def get_id_post(html_dir='html/'):
    url = 'https://www.museum.go.kr/librarybook/ajax/booksearch.do'
    d_dict = {
        "book_type_sel": "bo",
        "search_option_1": "",
        "search_value_1_v": "",
        "search_condition_1": "AND",
        "search_option_2": "title",
        "search_value_2_v": "",
        "search_condition_2": "AND",
        "search_option_3": "author",
        "search_value_3_v": "",
        "search_condition_3": "AND",
        "search_option_pub_year_begin": "1000",
        "search_option_pub_year_end": "1945",
        "search_condition_pub_year": "AND",
        "search_option_standard": "isbn",
        "search_option_standard_value": "",
        "search_condition_standard": "AND",
        "search_value_1": "",
        "search_value_2": "",
        "search_value_3": "",
        "pageno": "1",
        "display": "50",
        "book_type": "bo",
        "searchFront": "Y",
        "before_book_type": "#innerSearch_tbl"}
    for i in range(1, 43):
        d_dict['pageno'] = str(i)
        r = requests.post(url, data=d_dict, verify=False)
        with open(html_dir + str(i) + '.test.html', 'w') as fp:
            fp.write(r.content.decode())


def get_post_id(html_dir='html/'):
    key_list = []
    for i in os.listdir(html_dir):
        for item in open(html_dir + i):
            buf = json.loads(item)
            for elem_list in buf['bo_book_list']:
                key_list.append(elem_list['KEY'])
    post_dict_list = []
    with open('key_id.file', 'w', encoding='utf8') as fp:
        for key in key_list:
            post_dict = {}
            fp.write(str(key) + '\n')
            post_dict['book_type'] = 'bo'
            post_dict['rec_key'] = str(key)
            post_dict_list.append(post_dict)
    json.dump(post_dict_list, open('post.list.json', 'w'))


def get_data_json(post_list, index, json_dir='json/', url='https://www.museum.go.kr/librarybook/ajax/bookdetailinfo.do'):
    for post in tqdm(post_list):
        r = requests.post(url, data=post, verify=False).content.decode()
        json.dump(json.loads(r), open(json_dir + '-' + str(index) + '-' + post['rec_key'] + '.test.json', 'w'))


def main1(thread):
    all_url = json.load(open('post.list.json'))
    mono_list = [[] for i in range(thread)]
    for i, e in enumerate(all_url):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, post_list in enumerate(mono_list):
        p.apply_async(get_data_json, args=(post_list, index))
    p.close()
    p.join()


if __name__ == '__main__':
    # get_id_post()
    # get_post_id()
    # get_data_json(url='https://www.museum.go.kr/librarybook/ajax/bookdetailinfo.do')
    main1(thread=8)