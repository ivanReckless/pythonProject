import requests
from bs4 import BeautifulSoup
import re
import os
from tqdm import tqdm
from multiprocessing import Pool
import json


def get_html(index, post_list):
    headers = {
        'Host': 'kyudb.snu.ac.kr',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://kyudb.snu.ac.kr/book/list.do?mid=GDS',
        'Cookie': '_ga=GA1.3.1551200306.1603017629; _gid=GA1.3.1915172572.1603017629; JSESSIONID=oNq6iC1v9LQR5pvNaialYuTdN1S1V31qZ779N1tYbN1T5h8vVDprdQBSGlJ9iJ3X.sol10-web01_servlet_engine1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    url = 'http://kyudb.snu.ac.kr/book/list.do'
    file_path = '/media/ivan/Data/PyProject_Data/Kyu_db_data/new'
    for i in tqdm(post_list):
        data = {
            'prevSearchString': '',
            'bookCateRebrowsing': 'Y',
            'dbBookCdRebrowsing': 'N',
            'searchArea': '-1',
            'viewType': '1',
            'pageIndex': str(i),
            'recordIndex': '0',
            'mid': 'MOK',
            'book_cate': '',
            'focus': '',
            'book_cd': '',
            'target': '',
            'heje_seq': '0',
            'selSortInfo': 'sortCallNum',
            'selCallNum': 'ALL',
            'selSearchArea': 'okTitle',
            'totalSearchString': '',
            'pageUnit': '100'
        }
        r = requests.post(url, data=data, headers=headers).content.decode()
        with open(os.path.join(file_path, 'data_process_' + str(index) + '_' + str(i) + '.html'), 'w', encoding='utf8') as fp:
            fp.write(r)


def main(thread):
    data_list = [[] for i in range(thread)]
    # for idx in range(1, 435):
    #     data_list[idx % thread].append(idx)
    # p = Pool(thread)
    # for index, post_list in enumerate(data_list):
    #     p.apply_async(get_html, args=(index, post_list))
    # p.close()
    # p.join()


def get_image_book_id():
    file_path = '/media/ivan/Data/PyProject_Data/Kyu_db_data/new'
    data_path = []
    for item in os.listdir(file_path):
        data_path.append(file_path + '/' + item)
    for path in tqdm(data_path):
        r = BeautifulSoup(open(path), 'html.parser', from_encoding='utf8').find_all('div', class_='btn_img_txt')
        with open('test_image_book_id.txt', 'a', encoding='utf8') as fp:
            fp.write(str(r) + '\n')


def get_txt_content():
    data = []
    item_data_list = []
    id_content_list = []
    for content in open('/home/ivan/Desktop/pythonProject/Hanji_project/Kyu_db/get_image_book_id/test_image_book_id.txt'):
        re_content = r'<a(.*?)<\/a>'
        r = re.findall(re_content, content)
        if len(r) == 0:
            pass
        else:
            data.append(r)
    for item_data in data:
        for i in item_data:
            item_data_list.append(i)
    for id_content in item_data_list:
        id_content_list.append(id_content.split(',')[1].split(')')[0].replace("'", '').replace(' ', ''))
    for i in set(id_content_list):
        with open('id_index_file.file', 'a', encoding='utf8') as fp:
            fp.write(i + '\n')


def main_1(thread):
    data_list = []
    mono_list = [[] for i in range(thread)]
    for i in open('/home/ivan/Desktop/pythonProject/Hanji_project/Kyu_db/get_image_book_id/id_index_file.file'):
        data_list.append(i.replace('\n', ''))
    for i, e in enumerate(data_list):
        mono_list[i % thread].append(e)
    p = Pool(thread)
    for index, post_list in enumerate(mono_list):
        p.apply_async(get_target_json_data, args=(index, post_list))
    p.close()
    p.join()


def get_target_json_data(index, post_list):
    headers = {
        'Host': 'kyudb.snu.ac.kr',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://kyudb.snu.ac.kr/book/list.do?mid=GDS',
        'Cookie': '_ga=GA1.3.1551200306.1603017629; _gid=GA1.3.1915172572.1603017629; JSESSIONID=oNq6iC1v9LQR5pvNaialYuTdN1S1V31qZ779N1tYbN1T5h8vVDprdQBSGlJ9iJ3X.sol10-web01_servlet_engine1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    url = 'http://kyudb.snu.ac.kr/ajax/book/getBookPreViewInfo.do'
    for i in tqdm(post_list):
        data = {
            'book_cd': i.replace('\n', '')
        }
        r = requests.post(url, data=data, headers=headers).content.decode()
        content = json.loads(r)
        with open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json', 'processing_' + str(index) + '_' + i.replace('\n', '') + '.json'), 'w', encoding='utf8') as fp:
            json.dump(content, fp)


def get_missing_data_id():
    data = []
    for i in os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json'):
        data.append('_'.join(i.replace('.json', '').split('_')[2:]))
    for i in open('/home/ivan/Desktop/pythonProject/Hanji_project/Kyu_db/get_image_book_id/id_index_file.file'):
        if i.replace('\n', '') in data:
            pass
        else:
            with open('missing_book_id_file.file', 'a', encoding='utf8') as fp:
                fp.write(i)


def get_missing_data():
    headers = {
        'Host': 'kyudb.snu.ac.kr',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://kyudb.snu.ac.kr/book/list.do?mid=GDS',
        'Cookie': '_ga=GA1.3.1551200306.1603017629; _gid=GA1.3.1915172572.1603017629; JSESSIONID=oNq6iC1v9LQR5pvNaialYuTdN1S1V31qZ779N1tYbN1T5h8vVDprdQBSGlJ9iJ3X.sol10-web01_servlet_engine1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    url = 'http://kyudb.snu.ac.kr/ajax/book/getBookPreViewInfo.do'
    post_list = []
    for i in open('/home/ivan/Desktop/pythonProject/Hanji_project/Kyu_db/get_image_book_id/missing_book_id_file.file'):
        post_list.append(i.replace('\n', ''))
    for i in tqdm(post_list):
        data = {
            'book_cd': i.replace('\n', '')
        }
        r = requests.post(url, data=data, headers=headers).content.decode()
        content = json.loads(r)
        with open(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json', 'no_processing_' + i + '.json'), 'w', encoding='utf8') as fp:
            json.dump(content, fp)


def get_and_write_json_data():
    json_file_path = []
    title_dict = {}
    data_to_write = []
    for item in os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json'):
        json_file_path.append(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json', item))
    for file_path in tqdm(json_file_path):
        for r in json.load(open(file_path)).items():
            if r[0] not in title_dict:
                title_dict[r[0]] = len(title_dict)
            else:
                pass
    with open('title_image_data_json.json', 'w', encoding='utf8') as fp:
        json.dump(title_dict, fp)
    for i in title_dict.keys():
        data_to_write.append(i)
    with open('image_data_file_csv.csv', 'a', encoding='utf8') as fp:
        fp.write(','.join(data_to_write) + '\n')
    for file_path in tqdm(json_file_path):
        data_list = ['' for i in range(len(title_dict))]
        for r in json.load(open(file_path)).items():
            data_list[title_dict[r[0]]] = (r[1].replace(',', '，').replace('\t', ''))
        with open('image_data_file_csv.csv', 'a', encoding='utf8') as fp:
            fp.write(','.join(data_list) + '\n')


def get_index():
    json_file_path = []
    data_dict = {}
    for item in os.listdir('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json'):
        json_file_path.append(os.path.join('/media/ivan/Data/PyProject_Data/Kyu_db_data/new/new_json', item))
        data_dict['_'.join(item.replace('.json', '').split('_')[2:])] = len(data_dict)
    for file_path in json_file_path:
        # print('_'.join(file_path.split('/')[-1].replace('.json', '').split('_')[2:]))
        for i in json.load(open(file_path)).items():
            if 'ori_tit' in i:
                data_dict['_'.join(file_path.split('/')[-1].replace('.json', '').split('_')[2:])] = i[1]
    with open('id_title_index_json.json', 'w', encoding='utf8') as fp:
        json.dump(data_dict, fp)


def get_image():
    url = 'http://kyudb.snu.ac.kr/ImageServlet.do?imgFileNm=GK13743_00_IH_0001_001b.jpg&path=/data01/stream/GAE/IMG/GK13743_00/GK13743_00_0001/GK13743_00_IH_0001_001b.jpg'
    # 'http://kyudb.snu.ac.kr/ImageServlet.do?imgFileNm=GK13743_00_IH_0001_001a.jpg&path=/data01/stream/GAE/IMG/GK13743_00/GK13743_00_0001/GK13743_00_IH_0001_001a.jpg'
    # 'http://kyudb.snu.ac.kr/ImageServlet.do?imgFileNm=GC02452_00_IL_0001_000a.jpg&path=/data01/stream/MJR/IMG/GC02452_00/GC02452_00_0001/GC02452_00_IL_0001_000a.jpg'


if __name__ == '__main__':
    # main(thread=8)
    # get_image_book_id()
    # get_txt_content()
    # main_1(thread=8)
    # get_missing_data_id()
    # get_missing_data()
    # get_and_write_json_data()
    # get_index()
    get_image()