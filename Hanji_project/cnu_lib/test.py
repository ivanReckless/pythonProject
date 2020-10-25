import urllib.request
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

# for i in tqdm(range(1, 175)):
#     ori_url = 'http://library.cnu.ac.kr/search/tot/result?pn=' + str(i) + '&st=KWRD&si=TOTAL&websysdiv=TOT&q=%EF%BC%9F&bk_rf=&bk_rt=1945&oi=DISP03&os=DESC&cpp=100'
#     url = urllib.request.urlopen(ori_url).read()
#     soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
#     res = soup.find_all('dd', class_="searchTitle")
#     title_content = r'href=\"(.+?)\?mainLink='
#     title = re.findall(title_content, str(res))
#     with open('url.mid.file', 'a', encoding='utf8') as fp:
#         for i in title:
#             fp.write(str(i)+ '\n')

#
# content = open('url.mid.file')
# for mid in content:
#     with open('url.file', 'a', encoding='utf8') as fp:
#         url = 'http://library.cnu.ac.kr' + mid
#         fp.write(url)

# title_dict = {}
# url = urllib.request.urlopen('http://library.cnu.ac.kr/search/detail/CATTOT000000593247').read()
# soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
# res = soup.find_all('table', class_="profiletable")
# result_list = []
# for content in str(res).split('<tr>'):
#     if 'th' in content:
#         research_content = '(?<=>).*?(?=<)'
#         result = re.findall(research_content, content)
#         while '' in result:
#             result.remove('')
#         if len(result) > 2:
#             result = [result[0], "-".join(result[1:-1])]
#         result_list.append(result)
#         if result[0] not in title_dict:
#             title_dict[result[0]] = len(title_dict)
# write_line = [''] * len(title_dict)
# for cont in result_list:
#     if len(cont) > 1:
#         result_list = [cont[1].replace(',', '，')]
#         ind = title_dict[cont[0]]
#         write_line[ind] = cont[1]
# with open('error.csv', 'a', encoding='utf8') as fp:
#     fp.write(','.join(write_line) + '\n')

import os
import json


def gene():
    list_i = []
    content = []
    for i in os.listdir('/home/ivan/PycharmProjects/pythonProject/Hanji_project/cnu_lib'):
        if '.csv' in i:
            list_i.append(i)
    for path in list_i:
        for i in open(path, encoding='utf8'):
            content.append(i)
    with open('finalfile_new.csv', 'w', encoding='utf8') as fp:
        for i in content:
            fp.write(i)


def struct_build():
    with open('finalfile_new.csv', 'a', encoding='utf8') as fp:
        title_dict = json.load(open('title.dict.json'))
        title_list = [[val, key] for key, val in title_dict.items()]
        title_list.sort()
        title_list = [unit[1] for unit in title_list]
        fp.write(','.join(title_list))


if __name__ == '__main__':
    struct_build()