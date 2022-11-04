"""爬取有道翻译,破解js逆向"""
import requests
from faker import Faker
import execjs


def send(yh):
    li = ["不"]
    """无限循环,只要条件不满足就一直循环"""
    while yh != li:
        yh = input("请输入要翻译的内容:")
        if yh in li:
            break
        random_ua = Faker()
        ua = random_ua.user_agent()
        url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

        headers = {
            "User-Agent": ua,
            "Cookie": "OUTFOX_SEARCH_USER_ID_NCOO=597122912.6571933; OUTFOX_SEARCH_USER_ID=731992237@2408:8435:3900:82b:2c3b:f623:3abb:bfb2; ___rl__test__cookies=1667566891449",
            "Host": "fanyi.youdao.com",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://fanyi.youdao.com/",
            "Origin": "https://fanyi.youdao.com"
        }

        with open(file="有道翻译.js", mode="r", encoding="utf-8") as f:
            js_data = f.read()

        # 用compile()编译js代码
        js = execjs.compile(js_data)
        # 用call调用js代码,第一个参数是js的函数,第二个参数是用户输入的内容
        js_dict = js.call("youdao", yh)
        # print(js.call("youdao",yh))
        """打印:{'ts': '1667571854483', 'bv': '47edca4d7e6ec9bf4fca7156ea36b8ef', 'salt': '16675718544836', 'sign': '2baa771d06ed8a5d6aff0b24351e1a31'}"""

        data = {
            "i": yh,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            # 下面的参数是涉及到加密的,所以这里进行要进行js解密
            # "salt":"16675678836978",
            # "sign":"1e73c687bd29851fd6ee16567087e700",
            # "lts":"1667567883697",
            "bv": "47edca4d7e6ec9bf4fca7156ea36b8ef",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # 将两个字典更新到一起
        data.update(js_dict)
        # print(data)

        response = requests.post(url=url, headers=headers, data=data)
        json_data = response.json()
        text = json_data['translateResult'][0][0]['tgt']
        print(text)


def call():
    shuru = input("请输入要翻译的内容:")
    send(shuru)


if __name__ == '__main__':
    call()
