from geojson import FeatureCollection, Feature, Point
import csv
import json


# {"type":"Feature",
#     "geometry": {
#     "type":"Point","coordinates":[127.7156,47.5683] },
#     "properties":{"AREA":54.4471,"PERIMETER":68.4888,"?????":2,"????_1":23,"ADCODE93":230000,"ADCODE99":230000,"NAME":"????","POLYGONID":2,"SCALE":1.0,"ANGLE":0.0},
#     "id":"?????_label.1"
# }


# features = []
# csvpath = '/home/ivan/Documents/WeChat Files/wyf15713804915/Files/address.csv'
# with open(csvpath, newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for line in reader:
#         coordinates = float(line[1]), float(line[2])
#         features.append(
#             Feature(
#                 type="Feature",
#                 geometry=Point(coordinates),
#                 properties={
#                     "名称": line[0],
#                     "位置": line[3],
#                     "遗址": line[4],
#                     "遗物": line[5],
#                     "火葬": line[6],
#                     "遗迹的内容与性质": line[7],
#                     "时代": line[8],
#                     "年代": line[9],
#                     "物种": line[10],
#                     "调查年": line[11],
#                     "调查机关": line[12],
#                     "负责调查的人": line[13],
#                     "有关文献": line[14]
#                 }
#             )
#         )
#     print(features)
# collection = FeatureCollection(features)
# with open("geo.json", "w") as f:
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


data = []
file_data = csv.reader(open('/Tools/高句丽上传数据1.csv', encoding='utf8'))
for row in file_data:
    if row[-1].replace('\n', '') == '':
        pass
    elif row[-1].replace('\n', '') == '无':
        pass
    else:
        if row[-1].replace('\n', '').replace('·', '') not in data:
            data.append(row[-1].replace('\n', '').replace('·', ''))
for i in data:
    with open('data.csv', 'a', encoding='utf8') as fp:
        fp.write(i + '\n')