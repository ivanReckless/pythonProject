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


url = urllib.request.urlopen('https://lib.daegu.ac.kr/search/detail/CATTOT000000471988')
res = BeautifulSoup(url, 'html.parser', from_encoding='utf8').find_all('table', class_='profiletable')
for content in str(res).split('<tr>'):
    if 'th' in content:
        research_content = r'(?<=>).*?(?=<)'
        result = re.findall(research_content, str(content))
        while '' in result:
            result.remove('')
        if len(result) > 2:
            result = [result[0], '-'.join(result[1:-1])]
        if len(result) > 1:
            result[1] = result[1].replace(',', '，')
        print(result)
