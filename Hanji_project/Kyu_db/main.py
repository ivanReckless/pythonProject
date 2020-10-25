import os
import re
import requests
from bs4 import BeautifulSoup
import urllib
from multiprocessing import Pool
import json
from tqdm import tqdm


def get_data_html(index, post_list):
    url = 'http://kyudb.snu.ac.kr/book/list.do'
    data = {
        "prevSearchString": "",
        "bookCateRebrowsing": "Y",
        "dbBookCdRebrowsing": "N",
        "searchArea": "-1",
        "viewType": "1",
        "pageIndex": "i",
        "recordIndex": "0",
        "mid": "MOK",
        "book_cate": "",
        "focus": "",
        "book_cd": "",
        "target": "",
        "heje_seq": "0",
        "selSortInfo": "sortCallNum",
        "selCallNum": "ALL",
        "selSearchArea": "okTitle",
        "totalSearchString": "",
        "pageUnit": "100"
    }
    headers = {
        "Cookie": "JSESSIONID=IcaTOcOXIkwVMhAStas7lMI80PtK5jOP80Mr19l1x2UHw0RrV4K76EvG00GvqjJ7.sol10-web01_servlet_engine1Upgrade-Insecure-Requests: 1"
    }
    for i in tqdm(post_list): #435
        data["pageIndex"] = str(i)
        res = requests.post(url, data=data, headers=headers).content.decode()
        with open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data', 'test_page_' + str(index) + '_' + str(i) + '.html'), 'w', encoding='utf8') as fp:
            fp.write(res)


def main_0(thread):
    index_list = []
    for i in range(1, 435):
        index_list.append(i)
    mono_list = [[] for i in range(thread)]
    for i, e in enumerate(index_list):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, post_list in enumerate(mono_list):
        p.apply_async(get_data_html, args=(index, post_list))
    p.close()
    p.join()


def get_book_list():
    file_path_list = []
    for i in os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data'):
        file_path = os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data', i)
        file_path_list.append(file_path)
    for i in tqdm(file_path_list):
        res = BeautifulSoup(open(i).read(), 'html.parser').find_all('div', class_='list_tbl list_tbl_default')
        re_content = r'onclick\=\"(.*?)\;\"'
        result = re.findall(re_content, str(res))
        with open('item.file', 'a', encoding='utf8') as fp:
            for item in result:
                fp.write(item + '\n')


def get_book_id():
    book_id_list = []
    json_index_list = []
    # for i in open('item.file'):
    #     book_id_list.append(i)
    #     with open('book_id.file', 'a', encoding='utf8') as fp:
    #         fp.write(i.split(',')[1].replace(' ', '') + '\n')
    for i in open('book_id.file'):
        book_id_list.append(i)
    json_index_list = list(set(book_id_list))
    with open('json_ind.file', 'a', encoding='utf8') as fp:
        for i in json_index_list:
            fp.write(i.replace(');returnfalse', ''))


def get_data_json(index, post_list):
    url = 'http://kyudb.snu.ac.kr/ajax/book/getBookPreViewInfo.do'
    data = {
        "book_cd": "i",
    }
    headers = {
        "Cookie": "JSESSIONID=IcaTOcOXIkwVMhAStas7lMI80PtK5jOP80Mr19l1x2UHw0RrV4K76EvG00GvqjJ7.sol10-web01_servlet_engine1Upgrade-Insecure-Requests: 1"
    }
    for i in tqdm(post_list):
        data["book_cd"] = i
        res = requests.post(url, data=data, headers=headers).content.decode()
        with open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data', 'test_page_json_data_' + str(index) + '_' + str(i) + '.json'), 'w', encoding='utf8') as fp:
            fp.write(res)


def main_1(thread):
    index_list = []
    for i in open('json_ind.file'):
        index_list.append(i.replace('\n', '').replace("'", ''))
    mono_list = [[] for i in range(thread)]
    for i, e in enumerate(index_list):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, post_list in enumerate(mono_list):
        p.apply_async(get_data_json, args=(index, post_list))
    p.close()
    p.join()


def get_json_data():
    # print(len(os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data')))
    title_dict = {}
    for i in tqdm(os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data')):
        res = open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data', i)).read()
        item = json.loads(res)
        data_list = []
        for key, value in item.items():
            if key not in title_dict:
                title_dict[key] = len(title_dict)
        json.dump(title_dict, open('title.data.json', 'w', encoding='utf8'))
        for item in item.items():
            data_list.append(item)
        write_line = [''] * len(title_dict)
        for line in data_list:
            content = line[1].replace('\t', '').replace(' ', '').replace(',', '，')
            index = title_dict[line[0]]
            write_line[index] = content
        with open('data.csv', 'a', encoding='utf8') as fp:
            fp.write(','.join(write_line) + '\n')


def get_missing_data():
    id_list = []
    old_id_list = []
    file_id = os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data')
    for item in file_id:
        id_list.append('_'.join(item.split('_')[5:7]).replace('.json', ''))
    for i in open('book_id.file'):
        old_id_list.append(i.replace('\n', '').replace("'", '').replace(';returnfalse', '').replace(')', ''))
    old_id_list = list(set(old_id_list))
    new_id_list = list(set(old_id_list) - set(id_list))
    with open('missing_data.file', 'a', encoding='utf8') as fp:
        for i in new_id_list:
            fp.write(i + '\n')


def main_2(thread):
    id_list = []
    for i in open('missing_data.file'):
        id_list.append(i.replace('\n', ''))
    mono_list = [[] for i in range(thread)]
    for i, e in enumerate(id_list):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, post_list in enumerate(mono_list):
        p.apply_async(get_missing_json, args=(index, post_list))
    p.close()
    p.join()


def get_missing_json(index, post_list):
    url = 'http://kyudb.snu.ac.kr/ajax/book/getBookPreViewInfo.do'
    data = {
        "book_cd": "i",
    }
    headers = {
        "Cookie": "JSESSIONID=IcaTOcOXIkwVMhAStas7lMI80PtK5jOP80Mr19l1x2UHw0RrV4K76EvG00GvqjJ7.sol10-web01_servlet_engine1Upgrade-Insecure-Requests: 1"
    }
    for i in tqdm(post_list):
        data["book_cd"] = i
        res = requests.post(url, data=data, headers=headers).content.decode()
        with open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data_missing', 'test_page_json_data_' + str(index) + '_' + str(i) + '.json'), 'w', encoding='utf8') as fp:
            fp.write(res)


def get_new_csv():
    title_dict = {}
    for i in os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data_missing'):
        res = open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/json_data_missing', i)).read()
        item = json.loads(res)
        for key, value in item.items():
            if key not in title_dict:
                title_dict[key] = len(title_dict)
        json.dump(title_dict, open('title.missing.data.json', 'w', encoding='utf8'))
        data_list = []
        for item in item.items():
            data_list.append(item)
        write_line = [''] * len(title_dict)
        for line in data_list:
            content = line[1].replace('\t', '').replace(' ', '').replace(',', '，')
            index = title_dict[line[0]]
            write_line[index] = content
        with open('data.missing.csv', 'a', encoding='utf8') as fp:
            fp.write(','.join(write_line) + '\n')


if __name__ == '__main__':
    # main_0(thread=8)
    # get_book_list()
    # get_book_id()
    # main_1(thread=16)
    # get_json_data()
    # get_missing_data()
    # main_2(thread=8)
    get_new_csv()