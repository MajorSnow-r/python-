"""多线程爬取音效"""
import requests
import os
from bs4 import BeautifulSoup
from queue import Queue
import threading

# 创建文件
wjian = os.getcwd()+"\\音效\\"
if not os.path.exists(wjian):
    os.makedirs(wjian)

# 生产者类
class sheng_thread(threading.Thread):

    def __init__(self,sheng_queue,xiao_queue):
        self.sheng_queue = sheng_queue
        self.xiao_queue = xiao_queue
        threading.Thread.__init__(self)

    def run(self):
        while True:
            lock.acquire()
            if self.sheng_queue.empty():
                pass

            urls = sheng_queue.get()
            # print(urls)
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
            response = requests.get(urls,headers=headers)
            lock.release()
            response.encoding = "utf-8"
            self.jiexi(response.text)

    def jiexi(self,response):
        li =[]
        soup = BeautifulSoup(response,"lxml")
        divs = soup.find_all("div",class_="right-head")
        for div in divs:
            dic = {}
            # 因为有的标签下面是没有a标签的所以进行一个判断
            if div.a: #如果没有a标签就是false不执行
                # 获取所有的名称
                name = list(div.a.p.stripped_strings)[0]
                # 获取所有的属性
                title = div.a.get("href")
                dic["name"] = name
                dic["title"] = title
                li.append(dic)
        xiao_queue.put(li)
#消费者类
class xiao_thread(threading.Thread):
    def __init__(self,xiao_queue):
        self.xiao_queue = xiao_queue
        threading.Thread.__init__(self)

    def run(self) -> None:
        while True:
            if self.xiao_queue.empty():
                pass
            list_url = self.xiao_queue.get()
            for u in list_url:
                url_url = "https://sc.chinaz.com" + u["title"] #拼接url
                name_data = u["name"]
                """https://sc.chinaz.com/yinxiao/221010085020.htm""" #真实的url
                headerss = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
                responses = requests.get(url_url,headers=headerss)
                with open(wjian+name_data+".mp3",mode='wb')as f:
                    f.write(responses.content)
                    print(f"正在写入{name_data}")


if __name__ == '__main__':
    lock = threading.Lock()

    sheng_queue = Queue()

    for i in range(1,6):
        if i == 1:
            url = "https://sc.chinaz.com/yinxiao/index.html"
        else:
            url = f"https://sc.chinaz.com/yinxiao/index_{i}.html"

        sheng_queue.put(url)
    xiao_queue = Queue()
    for i in range(3):
        sheng = sheng_thread(sheng_queue,xiao_queue)
        sheng.start()
    for j in range(3):
        xiao = xiao_thread(xiao_queue)
        xiao.start()


