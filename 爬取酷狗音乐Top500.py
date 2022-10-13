"""
需求,爬取top500,,前三页音乐,保存到本地
"""
import requests
import os
import re
import json

# 创建文件夹
wjian = os.getcwd()+"\\酷狗音乐\\"
if not os.path.exists(wjian):
    # 递归创建文件
    os.makedirs(wjian)


def save_music(hash_1,album_id):
    url = "https://wwwapi.kugou.com/yy/index.php"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    # 因为url太长了参数不好分析,就用params携带参数
    params = {
        "r": "play/getdata",
        # "callback": "jQuery19105751414880015133_1665669104768",
        "hash": hash_1,
        "dfid": "3exR6E3fInEg3SGauN0NM78t",
        "appid": "1014",
        "mid": "b216daa882c0dee6db23f8a976011de9",
        "platid": "4",
        "album_id": album_id,
        "_": "1665669104770",
    }
    response = requests.get(url,headers=headers,params=params)
    # 因为请求的时候携带了 "callback": "jQuery19105751414880015133_1665669104768"这个参数,有这个参数返回的数据就不是字典,其实可以用正则
    # 进行处理,但是比较麻烦,这里把这个参数去掉,然后数据就变成字典的格式,用字典的键去取值
    json_dic = response.json()

    # 取歌曲的名称---> 通过字典的键值对进行取
    music_name = json_dic["data"]["audio_name"]

    mode = re.compile(r'[\*\/\\\+\-\"\$\%\']')
    re.sub(mode,"",music_name)

    # 取歌曲的url---> 通过字典的键值对进行取
    music_url = json_dic["data"]["play_url"]

    requests_music = requests.get(music_url).content

    # 保存歌曲到本地
    with open(file = wjian +"{}".format(music_name)+".mp3",mode="wb")as f:
        f.write(requests_music)
        print("正在保存{}".format(music_name))


def hash_id(url_id):

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    response_id = requests.get(url_id,headers=headers)

    res = re.search(r".*?global.features =(.*?);",response_id.text,re.S)
    id_data = res.group(1)

    dic = json.loads(id_data)

    for j in dic:

        hash_1 = j["Hash"]
        album_id = j["album_id"]
        save_music(hash_1,album_id)


if __name__ == '__main__':

    for i in range(1,4):
        url_id = "https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank".format(i)
        hash_id(url_id)

"""    以上代码有问题联系我    """


