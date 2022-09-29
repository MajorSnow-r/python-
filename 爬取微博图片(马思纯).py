import threading
import requests
import os
from lxml import etree
from queue import Queue

a = os.getcwd()+"\\微博图片\\"
if not os.path.exists(a):
    os.makedirs(a)

# 生产者类
class weibei(threading.Thread):

    def __init__(self, shengchan, data_list):
        self.shengchan = shengchan
        self.data_list = data_list
        threading.Thread.__init__(self)

    def run(self):

        while True:
            if shengchan.empty():
                pass
            url = shengchan.get()
            self.jiexi(url)

    def jiexi(self,url):

        headers = {
                 "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                 "cookie":"_s_tentry=weibo.com; Apache=9224227501232.648.1664365046045; SINAGLOBAL=9224227501232.648.1664365046045; ULV=1664365046081:1:1:1:9224227501232.648.1664365046045:; WBtopGlobal_register_version=2022092819; SUB=_2A25OMEJoDeRhGeBN6VQS9y7IwjSIHXVtRDSgrDV8PUNbmtANLWzZkW9NRJ8NVQtakSDdEL8RQpSdJOitGLuPfnSh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWn0IH9o_x-FLq7B7DfDIFn5JpX5KzhUgL.Foq0eoq0S05X1Kn2dJLoIpHjqgXLxK-L1K2LBKnLxKBLBonL1h5t; ALF=1695901112; SSOLoginState=1664365112; PC_TOKEN=dae9970586; WBStorage=4d96c54e|undefined"}
        response = requests.get(url,headers=headers)
        # print(response)
        # print(response.text)
        html = etree.HTML(response.text)
        jpg = html.xpath('//div[@node-type="feed_list_media_prev"]/div[@class="media media-piclist"]')

        for data in jpg:
            suo.acquire()
            jpg_url = data.xpath('./ul[@class="m3"]/li/img/@src')
            suo.release()
            if not jpg_url:
                jpg_url = data.xpath('./ul[@class="m4"]/li/img/@src')

            data_list.put(jpg_url)
# 消费者类
class xiaof(threading.Thread):
    def __init__(self,data_list):
        self.data_list = data_list
        threading.Thread.__init__(self)
        c = 300
    # 重写 run方法
        while True:
            if data_list.empty():
                pass

            # 取出队列中的元素
            git_url = data_list.get()

            for u in git_url:
                c -= 1
                url_zhen = u
                headers_1 = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                    "cookie": "_s_tentry=weibo.com; Apache=9224227501232.648.1664365046045; SINAGLOBAL=9224227501232.648.1664365046045; ULV=1664365046081:1:1:1:9224227501232.648.1664365046045:; WBtopGlobal_register_version=2022092819; SUB=_2A25OMEJoDeRhGeBN6VQS9y7IwjSIHXVtRDSgrDV8PUNbmtANLWzZkW9NRJ8NVQtakSDdEL8RQpSdJOitGLuPfnSh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWn0IH9o_x-FLq7B7DfDIFn5JpX5KzhUgL.Foq0eoq0S05X1Kn2dJLoIpHjqgXLxK-L1K2LBKnLxKBLBonL1h5t; ALF=1695901112; SSOLoginState=1664365112; PC_TOKEN=dae9970586; WBStorage=4d96c54e|undefined"}
                response_1 = requests.get(url_zhen,headers=headers_1).content
                with open(file= a+f"{c}.jpg",mode="wb")as f:
                    f.write(response_1)
                    print(f"正在写入{c}")

if __name__ == '__main__':

    suo = threading.Lock()
    shengchan = Queue()
    data_list = Queue()

    for i in range(1, 37):
        url_list = f"https://s.weibo.com/weibo?q=%E9%A9%AC%E6%80%9D%E7%BA%AF&page={i}"
        shengchan.put(url_list)
    for sheng in range(5):

        thre_5 = weibei(shengchan, data_list)
        thre_5.start()

    for xiao in range(5):
        thre_6 = xiaof(data_list)
        thre_6.start() # start 开启多线程