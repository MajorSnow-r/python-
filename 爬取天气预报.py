"""需求: 爬取 华北 东北 华东 华中 华南 西北 西南 港澳台 10月9号的天气
       1.用多线程爬取天气预报
       2.利用bs4去进行解析
       3.保存到 mongdb中 ,因为在多线程中没有连接上数据库,所以先把数据都保存到csv中 然后在进行保存"""

import requests
import csv
import threading                     #多线程
from bs4 import BeautifulSoup        #解析器
from pymongo import MongoClient      #数据库
from queue import Queue              #生产者消费者

with open("天气预报.csv", "a", encoding="utf-8", newline="") as f:
    write = csv.DictWriter(f, fieldnames=["chengshi_name", "max_qiwe", "min_qiwe"])
    write.writeheader()
# 生产者类
class tianqi(threading.Thread):

    def __init__(self,shengchan,xiaof):
        self.shengchan = shengchan
        self.xiaof = xiaof
        """因为创建多线程的类自带一个init,所有自己写的init没有这个方法,要重新初始化一个类自带的init方法"""
        threading.Thread.__init__(self) # self就是对象本身 重写多线程 init 方法的时候加进去

    # 重新run方法
    def run(self):
        while True:
            # 判断线程队列是否为空
            if self.shengchan.empty():
                pass
            url = self.shengchan.get()
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36X-Requested-With: XMLHttpRequest"}
            response = requests.get(url,headers=headers)
            response.encoding = "utf-8"
            responses = response.text
            """函数中调用函数,self指的就是对象本身,用对象去调用方法,调用完方法就可以执行了"""
            self.jiexi(responses)

    # 解析数据的函数
    def jiexi(self,responses):
        # 创建 soup对象
        soup = BeautifulSoup(responses,"lxml")

        # 获取所有的 div class="conMidtab"
        divs = soup.find("div",class_="conMidtab")

        # 获取所有的 table,因为这个table就是表格的全部数据
        tables = divs.find_all("table")
        li = []
        # 通过table在去获取tr标签

        for tr in tables:
            trs = tr.find_all("tr")[2:] # 取下标2之后的数据
            # 在去tr中获取td标签
            for index,td in enumerate(trs):
                dic ={}
                # 获取所有tr标签下面的 td 标签
                tds = td.find_all("td")
                """因为有直辖市所以要把直辖市扣除去,可以利用enumerate这个方法,通过下标将元素判断出去,因为直辖市都是比正常的城市多了一个标签,那么也就是如果下标等于0
                       那么就取下标为1的城市名字,否则就正常取其他城市0为下标的元素"""
                # 如果下标等等 0
                if index == 0:
                    tds = tds[1] # 如果是直辖市多一个元素的就取下标为1的
                else:
                    tds = tds[0] # 如果是正常城市就正常取下标为0的

                # 这个是获取到的所有城市的名字
                chengshi_name = list(tds.stripped_strings)[0]

                # 获取最高温度
                """上面的那个城市名称是通过tr.find_all取的td,所以下面的这个也要是根据tr.find_all去取值 不能直接用tds这个值的"""
                max_qiwe = list(td.find_all("td")[-5].stripped_strings)[0]

                # 获取最低温度
                min_qiwe = list(td.find_all("td")[-2].stripped_strings)[0]

                # 保存成字典的格式
                dic["chengshi_name"] = chengshi_name
                dic["max_qiwe"] = max_qiwe
                dic["min_qiwe"] = min_qiwe
                # 将数据都储存到列表中
                li.append(dic)

        # 将数据都放入到消费者队列中
        self.xiaof.put(li)

# 消费者类
class tianqi_xiao(threading.Thread):

    def __init__(self,shengchan,xiaof):
        self.shengchan = shengchan
        self.xiaof = xiaof
        # 重新 init 方法
        threading.Thread.__init__(self)

    def run(self) -> None:

        while True:
            if self.xiaof.empty():
                pass
            data = self.xiaof.get()
            self.save(data)

    def save(self,data):

        with open("天气预报.csv","a",encoding="utf-8",newline="")as f:
            write = csv.DictWriter(f,fieldnames=["chengshi_name","max_qiwe","min_qiwe"])
            write.writerows(data)
            print("写入成功")

if __name__ == '__main__':
    # 创建线程锁
    suo = threading.Lock()
    # 创建队列
    shengchan = Queue()
    # 创建url 并且将url放入到队列中去
    lists = ["hb","db","hd","hz","hn","xb","xn"]
    # 翻页处理 url
    for i in lists:
        url_1 = f"http://www.weather.com.cn/textFC/{i}.shtml"
        # 将url放入到队列中去
        shengchan.put(url_1)

    # 消费者队列
    xiaof = Queue()

    # 创建多线程
    for threads in range(5):
        th = tianqi(shengchan,xiaof)
        th.start()

    # 创建多线程(消费者)
    for thread in range(5):
        ths = tianqi_xiao(shengchan,xiaof)
        ths.start()