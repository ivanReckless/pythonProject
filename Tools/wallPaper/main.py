import requests
import os
import datetime


def get_wallpaper_from_bing(url):
    wall_paper_path = '/home/ivan/Pictures/Wallpapers'
    headers = {
        'Host': 'cn.bing.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': '_EDGE_V=1; MUID=25D893D690A661A3325B9CBE91886042; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=3B89D9B9280A4E799B768354B5947ACA&dmnchg=1; SRCHUSR=DOB=20201019&T=1603091095000; MUIDB=25D893D690A661A3325B9CBE91886042; SRCHHPGUSR=CW=1920&CH=232&DPR=1&UTC=480&DM=0&HV=1603092136&WTS=63738687738&BRW=W&BRH=S; SNRHOP=I=&TS=; _EDGE_S=mkt=zh-cn&SID=1AD3CEDDEEE36E5A270AC1B5EFA06F59; _SS=PC=U510&SID=1AD3CEDDEEE36E5A270AC1B5EFA06F59; SRCHS=PC=U510; ipv6=hit=1603095550964&t=4',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    r = requests.get(url, headers=headers).content
    wall_paper_name = url.split('th?id=')[1].split('.')[1].split('_')[0] + '_' + str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day)
    with open(os.path.join(wall_paper_path, wall_paper_name + '.jpg'), 'wb') as fp:
        fp.write(r)


if __name__ == '__main__':
    get_wallpaper_from_bing(url=input("今天的图片网址——————"))