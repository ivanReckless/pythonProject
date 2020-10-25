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

url = urllib.request.urlopen('https://lib.pusan.ac.kr/resource/catalog/?app=solars&mod=detail&record_id=100353631')
res = BeautifulSoup(url, 'html.parser', from_encoding='utf8').find_all('dl', class_='rd-list colon info')
result_list = []
for content in str(res).split('/dd>'):
    research_content = r'\>(.*?)\<'
    result = re.findall(research_content, str(content))
    while '' in result:
        result.remove('')
    if len(result) > 2:
        result = [result[0], '-'.join(result[1: -1])]
    if len(result) <= 0:
        continue
    result_list.append(result)
print(result_list)