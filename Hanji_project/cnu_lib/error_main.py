import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import json
import re
from multiprocessing import Pool


def get_error_url():
    error_list = []
    for i in open('errorurl.file', encoding='utf8'):
        if not i == '\n':
            error_list.append(i)
    return error_list


def get_error_inf(error_url_list, ind):
    title_dict = {}
    for target_url in tqdm(error_url_list):
        try:
            url = urllib.request.urlopen(target_url).read()
            soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
            res = soup.find_all('table', class_="profiletable")
            result_list = []
            for content in str(res).split('<tr>'):
                if 'th' in content:
                    research_content = '(?<=>).*?(?=<)'
                    result = remove_none(re.findall(research_content, content))
                    if len(result) > 2:
                        result = [result[0], "-".join(result[1:-1])]
                    result_list.append(result)
                    if result[0] not in title_dict:
                        title_dict[result[0]] = len(title_dict)
            json.dump(title_dict, open('title.error.dict.json', 'w'))
            write_error_inf(result_list, title_dict, ind)
            time.sleep(1)
        except Exception as e:
            print(e)
            with open('errorurl_new.file', 'a', encoding='utf8') as fp:
                fp.write(target_url)


def remove_none(target_list):
    while '' in target_list:
        target_list.remove('')
    return target_list


def write_error_inf(result_list, title_dict, index):
    write_line = [''] * len(title_dict)
    for line in result_list:
        if len(line) > 1:
            line[1] = line[1].replace(',', '，')
            ind = title_dict[line[0]]
            write_line[ind] = line[1]
    with open(str(index) + 'error.csv', 'a', encoding='utf8') as fp:
        fp.write(','.join(write_line) + '\n')


def main_1(thread=4):
    all_url = divide_error_url_list(n=thread)
    p = Pool(thread)
    for ind, url_list in enumerate(all_url):
        p.apply_async(get_error_inf, args=(url_list, ind))
    p.close()
    p.join()


def divide_error_url_list(n):
    url_list = get_error_url()
    num = n
    mono_list = [[] for i in range(num)]
    for i, e in enumerate(url_list):
        mono_list[i % num].append(e)
    return mono_list


if __name__ == '__main__':
    main_1()