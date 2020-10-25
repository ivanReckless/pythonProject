import urllib.request
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


# def get_start_point():



def get_all_origin_url():
    if os.path.exists('/home/ivan/PycharmProjects/pythonProject/1.txt'):
        pass
    else:
        for i in range(1, 22):
            original_url = 'http://jsg.aks.ac.kr/search/list?q=&secId=' + 'IMG&pageIndex=' + str(i) + '&pageUnit=1000'
            url = urllib.request.urlopen(original_url).read()
            soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
            res = soup.find_all('a')
            book_id_list = []
            for book_id in res:
                if 'data-rec-type' in str(book_id):
                    book_id_list += ['|'.join(str(book_id).split('">')[-1].split('_')[0:2])]
        return book_id_list


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(os.path.join('/media/ivan/Data/CSG_Data', name))
    else:
        pass


def get_img_url(original_url, startpoint):
    for book_id in get_all_origin_url():
        mid_url = original_url + book_id
    name = get_name(mid_url)
    print(name)
    # mkdir(name)
    # key_list = []
    # url = urllib.request.urlopen(original_url).read()
    # soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
    # res = soup.find_all('img')
    # for key in res:
    #     if 'thumb/' in str(key):
    #         key_list += [str(key).split('thumb/')[-1].split('"')[0]]
    # for url_key in key_list:
    #     for y in range(0, 10):
    #         for x in range(0, 9):
    #             img_url = 'http://jsgimage.aks.ac.kr/data/images/2019/04/04/dzi/' + url_key + '_files/13/' + str(y) + '_' \
    #                       + str(x) + '.jpg'
    #             try:
    #                 get_img(img_url)
    #                 with open()
    #             except Exception as e:
                    # print(e)


def get_img(url):
    response = requests.get(url).content
    return response


def get_name(url):
    url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url, 'html.parser', from_encoding='utf8')
    res = soup.find_all('header')
    img_name = str(res[0]).split('<h1>')[-1].split('</h1>')[0].split('(')[-1].split(')')[0]
    return img_name


if __name__ == '__main__':
    get_img_url(original_url='http://jsg.aks.ac.kr/viewer/viewIMok?dataId=')