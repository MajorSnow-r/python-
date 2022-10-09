import requests
import os
from bs4 import BeautifulSoup
import threading
from queue import Queue
from pymongo import MongoClient

"""爬取站长之家
   1.利用bs4的解析方式
   2.爬取图片名称和对应的url
   3.利用多线程爬取
   4.保存导 mongdb
"""
"""页面分析
1.获取包含所有图片的 div class="tupian-list com-img-txt-list masonry"
2.在获取所有的 class="item masonry-brick"
3.在获取下面的所有 文本和 链接
"""
wjian = os.getcwd() + "\\站长之家\\"
if not os.path.exists(wjian):
    os.makedirs(wjian)

# 定义一个生产者类
class shengchan(threading.Thread):

    def __init__(self, sheng_queue, xiao_queue):
        self.sheng_queue = sheng_queue
        self.xiao_queue = xiao_queue

        threading.Thread.__init__(self)

    # 重写 run方法
    def run(self):
        while True:
            # 上锁
            lock.acquire()
            if self.sheng_queue.empty():  # empty判断队列实付为空
                pass
            url_1 = self.sheng_queue.get()
            # print(url_1)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
            response = requests.get(url_1, headers=headers)
            # 解锁
            lock.release()
            response.encoding = "uft-8"
            response_text = response.text
            self.requests_data(response_text)

    # 发送请求
    def requests_data(self, response_text):
        lis = []
        soup = BeautifulSoup(response_text, "lxml")
        div = soup.find("div", class_="tupian-list com-img-txt-list")
        div_2 = div.find_all('div', class_="item")
        # print(div_2)
        for div_data in div_2:
            dic = {}
            a = list(div_data.find_all("a", class_="name")[0].stripped_strings)[0]
            img = div_data.find_all("img", class_="lazy")[0].get("data-original")
            dic["name"] = a
            dic["img"] = img
            lis.append(dic)
        self.xiao_queue.put(lis)


# 定义一个消费者类
class xiaofei(threading.Thread):
    def __init__(self, sheng_queue, xiao_queue):
        self.sheng_queue = sheng_queue
        self.xiao_queue = xiao_queue
        threading.Thread.__init__(self)
    def run(self) -> None:
        while True:
            if self.xiao_queue.empty():
                pass
            data = self.xiao_queue.get()
            for url_list in data:
                """将队列中的url跟name都分别取出来 url用来请求,name用来保存"""
                zhen_url = url_list["img"]
                names = url_list["name"]
                self.baocun(names, zhen_url)

    def baocun(self, names, zhen_url):
        url_url = "https:" + zhen_url
        headerss = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        responses = requests.get(url_url, headers=headerss)
        with open(file=wjian + names + ".jpg", mode="wb") as f:
            # content转成二进制数据
            f.write(responses.content)
            print(f"{names}写入成功")

if __name__ == '__main__':
    lock = threading.Lock()
    sheng_queue = Queue()
    for i in range(1, 20):  # 从2开始爬取到20
        if i == 1:
            url = "https://sc.chinaz.com/tupian/index.html"
        else:
            url = f"https://sc.chinaz.com/tupian/index_{i}.html"
        sheng_queue.put(url)
    xiao_queue = Queue()
    # 创建生产者多线程
    for j in range(7):
        sheng_thread = shengchan(sheng_queue, xiao_queue)
        sheng_thread.start()
    for z in range(7):
        xiao_thread = xiaofei(sheng_queue, xiao_queue)
        xiao_thread.start()

