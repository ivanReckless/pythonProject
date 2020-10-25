import json
import os
from tqdm import tqdm

if os.path.exists('test.csv'):
    os.remove('test.csv')

title_dict = {}
for root in tqdm(os.listdir('/home/ivan/PycharmProjects/pythonProject/Hanji_project/gnu_lib/inf_json')):
    path = os.path.join('/home/ivan/PycharmProjects/pythonProject/Hanji_project/gnu_lib/inf_json', root)
    data_dict = json.load(open(path))
    data_2_write = {}
    for item in data_dict['data']['list']:
        if not type(item['content']) is str:
            for content in item['content']:
                elem_list = []
                for i, e in enumerate(content):
                    elem_list.append(e[0])
            title = item['label']
            data_2_write[title] = ''.join(elem_list)
    for key, value in data_2_write.items():
        if key not in title_dict:
            title_dict[key] = len(title_dict)
    write_line = [''] * len(title_dict)
    for key, value in data_2_write.items():
        ind = title_dict[key]
        write_line[ind] = value.replace(',', '，')
    with open('test.csv', 'a', encoding='utf8') as fp:
        fp.write(','.join(write_line) + '\n')

with open('test.csv', 'a', encoding='utf8') as fp:
    title_list = [[val, title] for title, val in title_dict.items()]
    title_list.sort()
    fp.write(','.join([t[1] for t in title_list]) + '\n')
json.dump(title_dict, open('title.dict.json', 'w'))
