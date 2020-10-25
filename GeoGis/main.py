from geojson import FeatureCollection, Feature, Point
import csv
import json
import os
import re


# {"type":"Feature",
#     "geometry": {
#     "type":"Point","coordinates":[127.7156,47.5683] },
#     "properties":{"AREA":54.4471,"PERIMETER":68.4888,"?????":2,"????_1":23,"ADCODE93":230000,"ADCODE99":230000,"NAME":"????","POLYGONID":2,"SCALE":1.0,"ANGLE":0.0},
#     "id":"?????_label.1"
# }


# features = []
# csv_path = 'final.new.data.csv'
# with open(csv_path, newline='', encoding='utf8') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for line in reader:
#         coordinates = float(line[1]), float(line[2])
#         features.append(
#             Feature(
#                 geometry=Point(coordinates),
#                 properties={
#                     "name": line[0].split(':')[-1],
#                     # "textFill": "#ff0000",
#                     # "textHaloFill": "#ff0000",
#                     # "textHaloRadius": 0,
#                     # "textSize": 26,
#                     # "icon": "point",
#                     # "textOpacity": 0,
#                     "位置": line[3].split(':')[-1],
#                     "遗址": line[4].split(':')[-1],
#                     "遗物": line[5].split(':')[-1],
#                     "火葬": line[6].split(':')[-1],
#                     "遗迹的内容与性质": line[6].split(':')[-1],
#                     "时代": line[7].split(':')[-1],
#                     "年代": line[8].split(':')[-1],
#                     "类型": line[9].split(':')[-1],
#                     "调查年": line[10].split(':')[-1],
#                     "调查机关": line[11].split(':')[-1],
#                     "负责调查的人": line[12].split(':')[-1],
#                     "有关文献": line[13].split(':')[-1]
#                 }
#             )
#         )
#     print(features)
# collection = FeatureCollection(features)
# with open("geo_neo.json","w") as f:
#     f.write(json.dumps(collection, sort_keys=False, indent=4))


# features = []
# csvpath = '高句丽上传数据1.csv'
# with open(csvpath, newline='', encoding='utf8') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for line in reader:
#         coordinates = float(line[1]), float(line[2])
#         features.append(
#             Feature(
#                 geometry=Point(coordinates),
#                 properties={
#                     "name": line[0],
#                     "位置": line[3],
#                     "时代": line[4],
#                     "类型": line[5],
#                     "有关文献": line[6]
#                 }
#             )
#         )
# collection = FeatureCollection(features)
# with open("geo.json","w") as f:
#     f.write(json.dumps(collection, sort_keys=False, indent=4))


# data = []
# file_data = csv.reader(open('高句丽上传数据1.csv', encoding='utf8'))
# for row in file_data:
#     if row[-1].replace('\n', '') == '':
#         pass
#     elif row[-1].replace('\n', '') == '无':
#         pass
#     else:
#         if row[-1].replace('\n', '').replace('·', '') not in data:
#             data.append(row[-1].replace('\n', '').replace('·', ''))
# for i in data:
#     with open('data.csv', 'a', encoding='utf8') as fp:
#         fp.write(i + '\n')


# data = []
# path = 'C:\\Users\\Wyf06\\Downloads\\四库全书文本'
# file_name_list = os.listdir(path)
# for file_name in file_name_list:
#     with open(os.path.join(path, file_name), 'r', encoding='UTF16') as fp:
#         data.append(fp.read())
# for i in data:
#     with open('test_data.txt', 'a', encoding='UTF16') as fp:
#         fp.write(i)


# csv_path = 'data.csv'
# if os.path.exists(csv_path) is True:
#     os.remove(csv_path)
# r = json.load(open('渤海遗迹地图.json', encoding='utf-8-sig'))
# # print(r)
# for i in r['features']:
#     data_list = []
#     # for k, v in i['properties'].items():
#     #     print(k, v)
#     for data_content in i['properties'].items():
#         data_list.append(':'.join(data_content).replace('\n', ''))
#     if len(i['geometry']['coordinates']) == 3:
#         del i['geometry']['coordinates'][2]
#     for geo_content in i['geometry']['coordinates']:
#         data_list.append(str(geo_content))
#     with open('data.csv', 'a', encoding='utf8') as fp:
#         fp.write(','.join(data_list) + '\n')


# csv_path = 'old.data.test.csv'
# if os.path.exists(csv_path) is True:
#     os.remove(csv_path)
# r = csv.reader(open('data.csv', encoding='utf8'))
# for line in r:
#     data = []
#     for i in line:
#         data.append(i.replace('\n', '').replace(' ', ''))
#     with open('old.data.test.csv', 'a', encoding='utf8') as fp:
#         fp.write(','.join(data) + '\n')


# name_list = []
# data_list = []
# target_csv_path = 'data.test.csv'
# original_csv_path = 'old.data.test.csv'
# for line in open(original_csv_path, 'r', encoding='utf8'):
#     name_list.append(line.split(',')[-3])
#     data_list.append(line.split(','))
# # for i in data_list:
# #     print(','.join(i))
# for x in open(target_csv_path, 'r', encoding='utf8'):
#     if x.split(',')[0] in name_list:
#         for i in data_list:
#             if x.split(',')[0] in i:
#                 data_list.remove(i)
#                 data_list.append(x)
#             else:
#                 data_list.remove(i)
#                 data_list.append(','.join(i))
#     else:
#         data_list.append(x)
# print(data_list)
# # with open('final.data.csv', 'a', encoding='utf8') as fp:
# #     for i in data_list:
# #         fp.write(i)


# if os.path.exists('name.csv'):
#     os.remove('name.csv')
# all_data = []
# csv_path = '1.csv'
# for content in open(csv_path, 'r', encoding='utf8'):
#     data = []
#     if '；' in content:
#         data.append(content.split('；')[0].replace('\n', '').replace('\ufeff', '').replace('"', ''))
#         data.append(content.split('；')[-1].replace('\n', '').replace('\ufeff', '').replace('"', ''))
#     else:
#         data.append(content.replace('\n', '').replace('"', '').replace('\ufeff', ''))
#     all_data.append(data)
# data_list = []
# for item in all_data:
#     item_list = []
#     for i in item:
#         dy_search_content = r'\(.*?\)'
#         dynasty_content = re.findall(dy_search_content, i)
#         if i != '' and '(' in i:
#             name_content = [i.split(')')[0].split('(')[0] + i.split(')')[1]]
#         else:
#             name_content = [i]
#         string = dynasty_content + name_content
#         item_list.append(string)
#     data_list.append(item_list)
# for i in data_list:
#     i_list = []
#     if len(i) == 1:
#         for content in i:
#             i_list.append(''.join(content))
#     else:
#         for content in i:
#             i_list.append(''.join(content))
#     with open('name.csv', 'a', encoding='utf8') as fp:
#         fp.write('；'.join(i_list) + '\n')


# all_data = []
# csv_path = 'C:\\Users\\Wyf06\\Desktop\\1.csv'
# for content in open(csv_path, 'r', encoding='utf8'):
#     if content.replace('\n', '').replace('"', 'r') == 'r':
#         continue
#     else:
#         all_data.append(content.replace('\n', '').replace('"', '').replace('\ufeff', ''))
# print(all_data)
# with open('1.csv', 'a', encoding='utf8') as fp:
#     for i in all_data:
#         fp.write(i + '\n')


# r = open('渤海遗迹地图.ageeye', 'r', encoding='utf8').read()
# dict_r = json.loads(r)
# with open('test_data.json', 'w', encoding='utf8') as fp:
#     fp.write(json.dumps(dict_r))


# # print(json.load(open('test_data.json')))
# data_id_list = []
# data_dict = json.load(open('test_data.json'))['layers']
# for data_id in data_dict:
#     data_id_list.append(data_id)
# for data_id in data_id_list:
#     print(data_id_list[254])
#     data_properties = data_dict[data_id]["style"] = {"icon": "heart", "textFill": "#ff0000", "textHaloFill": "#ff0000"}
#     if 'next' not in data_dict[data_id]:
#         data_dict[data_id]['next'] = data_id_list[data_id_list.index(data_id) + 1]
#     else:
#         del data_dict[data_id]['next']
#         if data_id_list.index(data_id) + 1 < 640:
#             data_dict[data_id]['next'] = data_id_list[data_id_list.index(data_id) + 1]
#         else:
#             pass
# data = json.load(open('test_data.json'))
# data['layers'] = data_dict
# with open('test.ageeye', 'w', encoding='utf8') as fp:
#     fp.write(str(data).replace(' ', '').replace('None', 'null').replace('False', 'false').replace('True', 'true').replace("'", '"'))
#     #不要删除此行 ' ' None: null False: false True:true ': "
