import requests
import re
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText

############################################################################################
#link 和 Referer 需要改 发件收件邮箱要改
######################################教务网基本信息############################################
link = 'http://10.1.1.7/(xxxxxxxxxxxxxxxxxxxxxx)/xscjcx.aspx?xh=190701030037&xm=%BD%AD%CE%C4%CC%CE&gnmkdm=N121613'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Referer': 'http://10.1.1.7/(xxxxxxxxxxxxxxxxxxxxxx)/xscjcx.aspx?xh=190701030037&xm=%BD%AD%CE%C4%CC%CE&gnmkdm=N121613'
}
proxies = {
    "http": "http://127.0.0.1:8080"
}

#####################################邮件基本信息##########################################
# 第三方 SMTP 服务
mail_host = "smtp.163.com"             # SMTP服务器
mail_user = "xxxxxxxxx@163.com"     # 用户名
mail_pass = "xxxxxxxxxxxxxxx"         # 授权密码
sender = 'xxxxxxxxxxxx@163.com'        # 发件人邮箱
receivers = ['xxxxxxxxxxxx@qq.com']       # 接收邮件
content = ''
title = '教务网成绩变动'  # 邮件主题

def sendEmail():
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())

    email_client.quit()

#####################################教务网解析模块#########################################

def printScore(semester,scheoolYear):
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '',
        'hidLanguage': '',
        'ddlXN': scheoolYear,  # 学年scheoolYear
        'ddlXQ': semester,  # 学期semester
        'ddl_kcxz': '',
        'btn_xq': '学期成绩 '
    }
    a = requests.post(link, headers=headers, data=data).content.decode('GBK')
    #a = requests.post(link,headers=headers,data=data,proxies=proxies).content.decode('GBK')
    b = re.findall('<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>&nbsp;</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>',a)
    scorelist=[]

    print("课程名称------------------------------------------------分数-------")
    for i in b:
        print('{0:20}----------------------------'.format(i[3]), i[-1])
    print("---------------------------------------------------------------")
    len_list=len(b)
    for x in range(len_list):
        scorelist.append(b[x][3])
        scorelist.append(b[x][-1])
    # print(a)
    return scorelist

def choice_scheoolYear():
    print("请选择学年 输入数字")
    print("1------2019-2020")
    print("2------2020-2021")
    print("3------2021-2022")
    print("4------2022-2023")
    scheoolyear=eval(input())
    if scheoolyear==1:
        return '2019-2020'
    if scheoolyear==2:
        return '2020-2021'
    if scheoolyear==3:
        return '2021-2022'
    if scheoolyear==4:
        return '2022-2023'

def choice_semester():
    print("请选择学期 输入数字 一般1是上 2下 3不知道啥玩意")
    scheoolyear=eval(input())
    if scheoolyear==1:
        return '1'
    if scheoolyear==2:
        return '2'
    if scheoolyear==3:
        return '3'

def choice_time():
    print("多少时间爬一次")
    print("输入多少秒")
    T=eval(input())
    return T

#########################################################################################

if __name__ == '__main__':
    ch_sc = choice_scheoolYear()
    ch_se = choice_semester()
    Time = choice_time()

    while (1):
        SCORE1 = printScore(ch_se, ch_sc)
        time.sleep(Time)
        SCORE2 = printScore(ch_se, ch_sc)
        time.sleep(Time)
        if not (SCORE1==SCORE2):
            content = str(SCORE2)
            sendEmail()




