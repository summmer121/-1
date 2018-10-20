
import datetime
import logging
import os

import requests,re
from bs4 import BeautifulSoup
from logging.handlers import TimedRotatingFileHandler


import smtplib,time
from email.mime.text import MIMEText
from email.utils import formataddr



#########   所有长******** 皆为个人使用  不公开 需要的自己去百度server酱 申请key （免费)
my_sender = '441340677@qq.com'  # 发件人邮箱账号     作者本人 qq  有什么问题可以加我
my_pass = '**********'  # 发件人邮箱密码            自己去申请密码
my_user = '441340677@qq.com'  # 收件人邮箱账号，我这边发送给自己



def mail(xinxi):
    '''一开始是设置的邮箱通知的  现在已经不用了，留给有需要的朋友吧'''
    ret=True
    try:
        msg=MIMEText('填写邮件内容','plain','utf-8')
        msg['From']=formataddr(["发件人昵称",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["收件人昵称",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="%s更新了"%xinxi               # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()# 关闭连接
    except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

def get_nzuixin():
    '''获取逆天邪神最新章节'''
    try:
        url = r"http://www.nitianxieshen.com/"
        a = requests.get(url, timeout=60)
        a.encoding = "utf-8"
        soup = BeautifulSoup(a.text, 'html.parser')
        b = soup.find_all('li')
        gengxin = {}
        new = []
        link={}
        for i in b:
            if 'juan.html' not in i.find('a').get('href'):
                name = i.find('a').get_text()
                href = i.find('a').get('href')
                zhangjie = re.search('\d+', name)
                if name == "序章":
                    break
                if zhangjie:
                    new.append(int(zhangjie.group()))
                    gengxin[int(zhangjie.group())] = name
                    link[int(zhangjie.group())] = href
        zuixin = max(new)
        return zuixin,gengxin,link
    except:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        logger.error("%s  获取逆天邪神最新章节报错"%now)
        time.sleep(60)
        get_nzuixin()
def get_qzuixin():
    '''获取全职法师最新章节'''
    try:
        quanzhi_url = r"https://www.biquge5200.cc/2_2599/"
        quanzhi = requests.get(quanzhi_url, timeout=60)
        quanzhi.encoding = "gbk"
        soup = BeautifulSoup(quanzhi.text, "html.parser")
        t = soup.find_all('dd')
        new = []
        gengxin = {}
        link={}
        for i, v in enumerate(t):
            if i < 9:
                name = v.find('a').get_text()
                href = v.find('a').get('href')
                zhangjie = re.search('\d+', name)
                if zhangjie:
                    new.append(int(zhangjie.group()))
                    gengxin[int(zhangjie.group())] = name
                    link[int(zhangjie.group())] = href
        qzuixin=max(new)
        return qzuixin,gengxin,link
    except:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        logger.error("%s  获取全职法师最新章节报错"%now)
        time.sleep(60)
        get_qzuixin()



def send(a,b):
    '''这个是一开始单纯发送微信给个人的  现在改成了发送给所有订阅的人，也已经用不到了！！！'''
    now = time.strftime("%Y-%m-%d %X", time.localtime())
    url="https://sc.ftqq.com/****************************"
    data={
        "text":a,
        "desp":b
    }
    res = requests.post(url, data=data)
    try:
        if res.json()["code"] == 0:
            print("%s 发送成功，重新发送" % a)
        else:
            print("%s 发送失败，重新发送" % a)

    except:
        print('发送出错')


def nsendAll(a, b):
    '''发送爬取到的 逆天邪神 最新章节 给所有订阅者'''
    url = "https://pushbear.ftqq.com/sub"
    data = {
        "sendkey": "***************************",
        "text": a,
        "desp": b,
    }
    res = requests.post(url, data=data)
    try:
        if res.json()["code"] == 0:
            print("%s 发送成功" % a)
        else:
            print(res.json())
            print("%s 发送失败，重新发送" % a)
    except:
        print('发送出错')


def qsendAll(a, b):
    '''发送爬取到的 全职法师 最新章节 给所有订阅者'''
    url = "https://pushbear.ftqq.com/sub"
    data = {
        "sendkey": "*************************",
        "text": a,
        "desp": b,
    }
    res = requests.post(url, data=data)
    try:
        if res.json()["code"] == 0:
            print("%s 发送成功" % a)
        else:
            print(res.json())
            print("%s 发送失败，重新发送" % a)
    except:
        print('发送出错')


class log():
    '''日志文件'''
    def __init__(self):
        self.logger = logging.getLogger(__name__)
# 以下三行为清空上次文件
# 这为清空当前文件的logging 因为logging会包含所有的文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
# 将当前文件的handlers 清空
        self.logger.handlers = []
# 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)
# 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
# loggger 文件配置路径
            basepath = os.path.dirname(__file__)
            print()
            if int(datetime.datetime.now().month)<10:
                month='0'+str(datetime.datetime.now().month)
            else:
                month=str(datetime.datetime.now().month)
            if int(datetime.datetime.now().day)<10:
                day='0'+str(datetime.datetime.now().day)
            else:
                day=str(datetime.datetime.now().day)
            filename='%s.log' % (str(datetime.datetime.now().year)+month+day)


            #self.handler = logging.FileHandler(filename,encoding='utf-8')
           # self.hander=TimedRotatingFileHandler(filename,encoding='utf-8',when="D", interval=1, backupCount=2)
            self.handler = logging.handlers.TimedRotatingFileHandler("运行日志.log", encoding='utf-8',when='D', interval=1, backupCount=1)
            # # 设置后缀名称，跟strftime的格式一样
            self.handler.suffix = "%Y-%m-%d.log"

# logger 配置等级
            self.logger.setLevel(logging.DEBUG)
# logger 输出格式
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
# 添加输出格式进入handler
            self.handler.setFormatter(formatter)
# 添加文件设置金如handler
            self.logger.addHandler(self.handler)
    def info(self,message=None):
        self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)

    def debug(self,message=None):
        self.__init__()
        self.logger.debug(message)
        self.logger.removeHandler(self.logger.handlers)

    def warning(self,message=None):
        self.__init__()
        self.logger.warning(message)
        self.logger.removeHandler(self.logger.handlers)

    def error(self,message=None):
        self.__init__()
        self.logger.error(message)
        self.logger.removeHandler(self.logger.handlers)

    def critical(self, message=None):
        self.__init__()
        self.logger.critical(message)
        self.logger.removeHandler(self.logger.handlers)
logger=log()


abc=[]
nzuixin=1
qzuixin=1
try:
    nzuixin,title1,link1 = get_nzuixin()
    qzuixin,title2,link2= get_qzuixin()
    with open("最新章节.txt", "r") as f:
        chushi = f.readlines()
        for i in chushi:
            if i!='':
                abc.append(int(i))
        if len(abc) < 2:
            with open("最新章节.txt", "w") as f:
                f.write('%d\n'%nzuixin)
                f.write('%d'%qzuixin)
except:

    with open("最新章节.txt", "w") as f:
        f.write('%d\n' % nzuixin)
        f.write('%d' % qzuixin)



chushi=int(abc[0])
qchushi=int(abc[1])  ######获取文本里的最新值
while 1:
    try:
        nzuixin,title1,link1=get_nzuixin()
        qzuixin,title2,link2=get_qzuixin()
        if nzuixin>chushi and nzuixin!=None:
            if nzuixin-chushi>5:
                chushi=nzuixin-5

            for d in range(chushi + 1, nzuixin + 1):
                a = "逆天邪神--   {}".format(title1[d])
                try:
                    res = requests.get(link1[d], timeout=60)
                    res.encoding = "utf-8"
                    soup = BeautifulSoup(res.text, 'html.parser')
                    content = soup.find_all('p')
                    s = ''
                    for i in content[1:-1]:
                        s = s + str(i)
                    s = s.replace('<p>', '&emsp;')
                    s = s.replace('</p>', '\n\n')

                    nsendAll(a,s)

                    chushi =d
                    with open("最新章节.txt","w") as f:
                        f.write('%s\n'%str(d))
                        f.write('%s\n'%str(qchushi))
                except:
                    print("爬取发送正文%s失败" % title1[d])

        else:
            now = time.strftime("%Y-%m-%d %X", time.localtime())
            print("%s    逆天邪神还没有更新,最新  %s"%(now,title1[nzuixin]))

        if qzuixin > qchushi and qzuixin !=None:
            if qzuixin-qchushi>5:
                qchushi=qzuixin-5
            for d in range(qchushi+1,qzuixin+1):
                a="全职法师--  {}".format(title2[d])
                try:
                    quanzhi = requests.get(link2[d], timeout=60)
                    quanzhi.encoding = "gbk"
                    soup = BeautifulSoup(quanzhi.text, "html.parser")
                    content = soup.find('div', id="content")
                    content = str(content)
                    s = content.replace("<p>", '&emsp;')
                    s = s.replace("</p>", '\n\n')
                    qsendAll(a,s)
                    qchushi = qzuixin
                    with open("最新章节.txt", "w") as f:
                        f.write('%s\n' % str(chushi))
                        f.write('%s\n' % str(d))
                except:
                    print("爬取发送正文%s失败"%title2[d])


        else:
            now = time.strftime("%Y-%m-%d %X", time.localtime())
            print("%s    全职法师还没有更新,最新  %s" % (now,title2[qzuixin]))
        time.sleep(300)
    except:
        print("报错，停止爬取2分钟")
        time.sleep(120)


