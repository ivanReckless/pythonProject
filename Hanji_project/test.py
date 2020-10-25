import urllib.request
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


# def get_start_point():


def get_all_origin_url():
    for i in range(1, 22):
        original_url = 'http://jsg.aks.ac.kr/search/list?q=&secId=' + 'IMG&pageIndex=' + str(i) + '&pageUnit=1000'
        url = urllib.request.urlopen(original_url).read()
        soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
        res = soup.find_all('a')
        for book_id in res:
            if 'data-rec-type' in str(book_id):
                # print(str(book_id))
                book_id_list = '|'.join(str(book_id).split('">')[-1].split('_')[0:2])
                # print(book_id_list)
                with open('./1.txt', 'a', encoding='utf8') as fp:
                    fp.write(book_id_list + '\n')


if __name__ == '__main__':
    get_all_origin_url()