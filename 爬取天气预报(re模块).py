"""利用正则爬取42天天气预报
   1.爬取日期
   2.爬取天气
   3.爬取温度
   4.爬取风向
   5.爬取风力
"""
import requests
import re
from queue import Queue
import threading
from pymongo import MongoClient

# 生产者类
class sheng_thread(threading.Thread):

    def __init__(self,sheng_queue,xiao_queue):
        self.sheng_queue = sheng_queue
        self.xiao_queue = xiao_queue
        # 重写多线程的init方法
        threading.Thread.__init__(self)

    # 重写run方法
    def run(self) -> None:
        while True:
            if self.sheng_queue.empty():
                pass

            zhen_url = self.sheng_queue.get()
            # 发送请求
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
            response = requests.get(url=zhen_url,headers=headers)
            response.encoding ="utf-8"
            self.jiexi(response.text)

    def jiexi(self,response):
        li =[]
        # 获取包含了所有需要元素的 ul 标签
        ul = re.search('.*(<ul class="t .*?">.*?</ul>).*',response,re.S)
        urs = ul.group(1)

        a = re.finditer('<span class="time">(?P<rq>.*?)</span>.*?<span class="wea">(?P<tq>.*?)</span>.*?<em>(?P<wd>.*?)</em>.*?<span class="wind">(?P<fx>.*?)</span>.*?<span class="wind1">(?P<fl>.*?)</span>',urs,re.S)
        for i in a:
            dic = i.groupdict()
            li.append(dic)
        xiao_queue.put(li)

# 消费者类
class xiao_thread(threading.Thread):

    def __init__(self,xiao_queue):
        self.xiao_queue = xiao_queue
        threading.Thread.__init__(self)

    def run(self) -> None:
        while True:
            if self.xiao_queue.empty:
                pass

            data = self.xiao_queue.get()

            mongo = MongoClient()

            database = mongo.get_database("retianqi")

            # 写入数据
            for da in data:
                database.retianqiybao.insert_one(da)

if __name__ == '__main__':
    lock = threading.Lock()

    sheng_queue = Queue()

    url = "http://www.weather.com.cn/weather15d/101250101.shtml"

    sheng_queue.put(url)
    xiao_queue = Queue()

    for i in range(5):
        sheng = sheng_thread(sheng_queue,xiao_queue)
        sheng.start()

    for j in range(5):
        xiao = xiao_thread(xiao_queue)
        xiao.start()