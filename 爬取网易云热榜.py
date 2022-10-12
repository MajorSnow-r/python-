import json
import requests
import re
from pymongo import MongoClient


def send(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    responses = response.text
    return responses


def jiexi(datas):
    texts = re.match('.*<textarea id="song-list-pre-data" style="display:none;">(.*?)</textarea>.*', datas, re.S)
    josns = texts.group(1)
    dicts = json.loads(josns)
    li = []
    for dic in dicts:
        # 定义一个保存名字的变量
        geshous = ""
        #  定义一个计数器
        jishu = 0
        # 歌曲的名字
        name = dic['name']
        # 获取歌曲的歌手
        for geshou in dic['artists']:
            dics = {}
            geshous += geshou['name']
            jishu += 1
        if jishu == 1:
            sengname = dic['artists'][0]['name']
        else:
            sengname = geshous

        dics["name"] = name
        dics["sengnname"] = sengname
        li.append(dics)
    return li


def preserve(preserve_data):
    mongo = MongoClient()

    database = mongo.get_database("wangyiyun")

    for mongo_data in preserve_data:
        database.wangyiyun.insert_one(mongo_data)

if __name__ == '__main__':
    url = "https://music.163.com/discover/toplist?id=19723756"
    datas = send(url)
    preserve_data = jiexi(datas)
    preserve(preserve_data)