import pyautogui  #GUI自动花工具,其目的是可以用程序自动控制鼠标和键盘操作
import pyperclip
from datetime import datetime # 关于时间的模块
# 这个库可以实现延迟调度要执行的python代码的功能,可以执行一次 也可以定期执行
from apscheduler.schedulers.blocking import BlockingScheduler
import time
def main():

    pyautogui.PAUSE =0
    # wzhi = pyautogui.Point()
    # 获取当前鼠标的位置
    # print(pyautogui.position())
    # shubiao =pyautogui.position(x=364,y=757)
    # 快捷键打开微信
    pyautogui.hotkey("Ctrl","Alt","w")
    # 获取微信输入框的光标位置
    # time.sleep(2)
    # print(pyautogui.position())

    # 微信输入框光标的位置
    # shubiao_input = pyautogui.position(x=578,y=508)
    # 点击
    # pyautogui.click(shubiao_input)

    # 将鼠标移动到指定的位置 ,duration=1的意思就是执行时长
    # pyautogui.moveTo(shubiao_input,duration=1)

    # pyperclip.copy的意思就是将字符串放置到 粘贴板中 下载使用的时候直接 ctrl+v 粘贴出来就可以了
    pyperclip.copy('叫大哥')
    # 组合键 粘贴的意思 将粘贴板中的内容粘贴到 微信输入框
    pyautogui.hotkey("ctrl","v")
    # 这个方法只能输入英文 或者数字
    # pyautogui.typewrite
    # 敲击回车
    pyautogui.press("enter")

    # 延迟几秒
    time.sleep(2)

    # 将内容放到粘贴板中
    pyperclip.copy("大哥")

    # 将内容复制出来
    pyautogui.hotkey("ctrl","v")
    # 敲击回车
    pyautogui.press("enter")

    #设置定时发送
    #先实例化 一个 BlockingScheduler

dingshi = BlockingScheduler()
# 第一个参数是到点要执行的程序，第二个是触发器  第三个是超出这个秒数程序就不用再执行了, 后面run_date是要执行的时间
dingshi.add_job(main,trigger='date',misfire_grace_time=600,run_date="2022-09-16 19:53:00")#添加任务
dingshi.start()

