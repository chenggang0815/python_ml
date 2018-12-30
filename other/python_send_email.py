#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '＊＊＊@163.com'
receiver = '＊＊＊@163.com'
subject = '勤劳的python!'
smtpserver = 'smtp.163.com'
username = '＊＊＊@163.com'
password = '＊＊＊＊＊＊'

msg = MIMEText('这是一条来自python的邮件,我的目的是监控京东上的图书优惠券～妈妈再也不用担心我买不起书啦！！！','plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = '＊＊＊@163.com>'
msg['To'] = "＊＊＊@163.com"


smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

print('发送成功')
