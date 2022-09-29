""" 单线程爬取表情包 利用 urllib的urlretrieve 保存图片  翻页爬取分析网页url 利用循环翻页
    利用xpath解析网页数据  利用正则替换没有用的字符 """
import requests
from urllib import request
import re
import os
from lxml import etree #先要将html 转成 xml
def dome_1():
    # 计数变量
    count = 0
    # 利用os模块创建文件夹,根据当前文件路径后面在拼接一个路径
    b = os.getcwd() +"\\表情包"
    print(b)
    # 判断路径下的文件是否存在
    if not os.path.exists(b):
        # 不存在就创建这个文件夹
        os.makedirs(b)
    else:
        print("文件已经存在")
    # 翻页处理
    for tim in range(1,150):
        url = f"https://www.fabiaoqing.com/biaoqing/lists/page/{tim}.html"

        # headers 携带
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

        # 发送请求 获取响应
        response = requests.get(url,headers=headers)

        # 获取数据
        html =response.text
        # print(html) #检查

        # 将xml 转成 html
        xml = etree.HTML(html)

        # 解析数据,获取所有的 img 的列表
        jiexi =xml.xpath('//div[@class="ui segment imghover"]/div[@class="tagbqppdiv"]//img[@class="ui image lazy"]')
        # print(jiexi) #检查
        for i in jiexi:
            # @的意思是选取元素,选取当前节点的元素
            imgs = i.xpath("@data-original")[0] #[0]的意思是将元素从列表中取出来
            # print(imgs) #检查
            # 获取表情包名称数据解析
            name =i.xpath("@title")[0]

            #利用正则中的sub 方法吧一些特殊字符都替换掉,写入二进制是没有办法写入特殊字符的
            name =re.sub(r"[，。？? /\\#*<>：:]","",name)

            # 因为图片是二进制的 所以用urlib里面的urlretrieve 来保存图片
            # 拼接得到图片保存的完整路径，b的路径拼接name的文件,就等于把name放到b文件路径里面去
            file_name = os.path.join(b, name + '.jpg')
            # print(file_name) #检查
            request.urlretrieve(imgs, file_name) #意思就是在表情包文件夹下面写入内容
            count += 1
            print(f"下载{count}张图片")

if __name__ == '__main__':
    dome_1()


