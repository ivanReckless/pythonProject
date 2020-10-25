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


# i = 38732
# url = 'http://search.koreastudy.or.kr/search/view?searchKeyword=%E8%A7%A3&searchCondition=FORM_TYPE-0-1&pageIndex=1&schc_data_bnd_id=0000000' + str(
#             '%05d' % i)
# res = requests.get(url).content
# with open('test.html', 'wb') as fp:
#     fp.write(res)


def clean_html(path_dir='/media/ivan/Data/PyProject_Data/koreastudy_lib_data/html'):
    html_list = []
    for root in tqdm(os.listdir(path_dir)):
        path = os.path.join(path_dir, root)
        if len(open(path).read()) > 17211:
            html_list.append(path)
    with open('html.clean.file', 'w', encoding='utf8') as fp:
        for i in html_list:
            fp.write(i + '\n')


def get_target_info():
    title_dict = {}
    html_file_list = []
    for html_file in open('html.clean.file'):
        html_file_list.append(html_file.replace('\n', ''))
    for html in tqdm(html_file_list):
        id = html.split('-')[1]
        # print(id)
        soup = BeautifulSoup(open(html).read(), 'html.parser').find_all('table', class_="table2 mt20")
        for content in soup:
                                # title_research_content = r'\=\"row\"\>(.*?)\<'
                                # title_content = re.findall(title_research_content, str(content))
                                # if len(title_content) <= 1:
                                #     continue
                                # for title in title_content:
                                #     title_dict[title] = len(title_dict)
                                # value_research_content = r'\<td\>([\s\S]*?)\<\/td\>
            value_research_content = r'\<tr\>([\s\S]*?)\<\/tr\>'
            value_content = re.findall(value_research_content, str(content))
            item_dict = {}
            for item in value_content:
                item_list = []
                content = re.findall(r'\>([\s\S]*?)\<', item)
                content.remove('\n')
                while '' in content:
                    content.remove('')
                for i in content:
                    t = i.replace('\n', '').replace('\t', '')
                    item_list.append(t)
                if len(item_list) > 2:
                    item_list = [item_list[0], ';'.join(item_list[1:-1])]
                if '자료ID' in item_list:
                    item_list.append(id)
                if len(item_list) <= 1:
                    continue
                item_dict[item_list[0]] = item_list[1]
            if len(item_dict) <= 1:
                continue
            for key, value in item_dict.items():
                if key not in title_dict:
                    title_dict[key] = len(title_dict)
            write_line = [''] * len(title_dict)
            for key, value in item_dict.items():
                if ',' in value:
                    value = value.replace(',', '，')
                ind = title_dict[key]
                write_line[ind] = value
            with open('test.csv', 'a', encoding='utf8') as fp:
                fp.write(','.join(write_line) + '\n')
        # print(title_dict)


if __name__ == '__main__':
    # clean_html()
    get_target_info()