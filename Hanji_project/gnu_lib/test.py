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


def get_json():
    header = {"Cookie": "JSESSIONID=C3D2B742B6D281914ABBD8E7E37F5850.pyxis-api1; _ga=GA1.3.979558955.1598236785; NG_TRANSLATE_LANG_KEY=%22ko%22; "
                        "PYXIS2_UUID=%22ff5ba917-dcb9-4359-8ef0-e010e66aed0c%22Connection: keep-alive"}
    for i in range(0, 92):
        json_url = 'https://lib.gnu.ac.kr/pyxis-api/1/collections/1/search?language=78&max=100&offset=' + str(i) + '00&rq=PUBLISH_YEAR%3D%5B1090%20TO%201945%5D'
        r = requests.get(json_url, headers=header, verify=False)
        with open(str(i) + 'test.file.json', 'w') as fw:
            fw.write(r.content.decode())


def get_id():
    id_list = []
    for file in os.listdir('/home/ivan/PycharmProjects/pythonProject/Hanji_project/gnu_lib'):
        if '.json' in file:
            file_dict = json.load(open(os.path.join('/home/ivan/PycharmProjects/pythonProject/Hanji_project/gnu_lib', file)))
            for item_dict in file_dict['data']['list']:
                id_value = item_dict['id']
                id_list.append(str(id_value))
    with open('id_value.file', 'a', encoding='utf8') as fp:
        for id_num in id_list:
            fp.write('https://lib.gnu.ac.kr/pyxis-api/1/biblios/' + id_num + '\n')


def divide_target_url(num):
    url_list = []
    for url in open('id_value.file'):
        url_list.append(url)
    mono_list = [[] for i in range(num)]
    for i, e in enumerate(url_list):
        mono_list[i % num].append(e)
    return mono_list


def get_inf_json(url_list, index):
    header = {"Cookie": "JSESSIONID=C3D2B742B6D281914ABBD8E7E37F5850.pyxis-api1; _ga=GA1.3.979558955.1598236785; NG_TRANSLATE_LANG_KEY=%22ko%22; "
                        "PYXIS2_UUID=%22ff5ba917-dcb9-4359-8ef0-e010e66aed0c%22Connection: keep-alive"}
    for ind, json_url in tqdm(enumerate(url_list)):
        r = requests.get(json_url, headers=header, verify=False)
        with open(str(index) + '-' + str(ind) + 'test.file.json', 'w') as fw:
            fw.write(r.content.decode())


def main_1(thread):
    all_url = divide_target_url(num=thread)
    p = Pool(thread)
    for index, url_list in enumerate(all_url):
        p.apply_async(get_inf_json, args=(url_list, index))
    p.close()
    p.join()


if __name__ == '__main__':
    # get_json()
    # get_id()
    main_1(thread=8)
