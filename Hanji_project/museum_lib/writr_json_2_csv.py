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

title_dict = {}
for file in os.listdir('/home/ivan/PycharmProjects/pythonProject/Hanji_project/museum_lib/json'):
    book_info = {}
    file_path = os.path.join('/home/ivan/PycharmProjects/pythonProject/Hanji_project/museum_lib/json', file)
    book_inf = json.load(open(file_path))['book_info']
    for key_book_inf, value_book_inf in book_inf.items():
        book_info[key_book_inf] = str(value_book_inf)
    hold_inf_list = json.load(open(file_path))['hold_info']
    for hold_inf in hold_inf_list:
        for key_hold_inf, value_hold_info in hold_inf.items():
            book_info[key_hold_inf] = str(value_hold_info)
    for key, value in book_info.items():
        if key not in title_dict:
            title_dict[key] = len(title_dict)
    write_line = [''] * len(title_dict)
    for key, value in book_info.items():
        ind = title_dict[key]
        write_line[ind] = value.replace(',', '，')
    with open('test.flie.csv', 'a', encoding='utf8') as fp:
        fp.write(','.join(write_line) + '\n')
json.dump(title_dict, open('title.dict.json', 'w'))
