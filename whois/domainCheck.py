#-*-encoding:utf-8-*-#
'''
version 0.2
查询域名是否被注册，并发送邮件通知
'''
import requests
import smtplib  
import time
from email.mime.text import MIMEText
import re
#换成你的接受邮箱，发送邮箱可以不换
mailto_list=['907169968@qq.com'] 
mail_host="smtp.sina.com"  #设置服务器
mail_user="chenlinmytest"    #用户名
mail_pass="12345678"   #口令 
mail_postfix="sina.com"  #发件箱的后缀

def whois(domain,suffix):
	url = 'http://www.cndns.com/Ajax/domainQuery.ashx?panel=domain&domainName=%s&domainSuffix=.%s&cookieid=arejdu2jmdjbfdrioptzg4p4&usrname=&domainquerysign=6a1209cee8ece1142bd9d6de0cac93c5'%(domain,suffix)
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
	#print url
	res = requests.get(url,headers=headers)
	res_cont = res.content;
	print res_cont
	val = res_cont[4]
	return val
def send_mail(to_list,sub,content):  
    me="test"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
def gettime(domain,suffix):
	url = 'http://www.cndns.com/whois/index.aspx?num=0&d=%s.%s&token=76e9751c3a7f89498ca92fa5d6fd26dc'%(domain,suffix)
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
	res = requests.get(url,headers=headers)
	cont = res.content
	open('1.html','wb').write(cont)
	time_all = re.findall(r'2016',cont)
	print time_all
if __name__ == '__main__':
	print 'program is running...'
	domain = 'memcom'
	suffix = 'cn'
	open('code/python/spider/whois/logdomainCheck.txt','wb').write(time.ctime())
	while(True):
		now = time.ctime()
		if (now[11:16]=='08:10'):
			val = whois(domain,suffix)
			print val
			if val == '1':
				print 'the domain is using'
				#gettime(domain,suffix)
				#msg = " 域名%s.%s已被注册" %(domain,suffix)
			else:
				msg = "域名%s.%s可被注册 注册地址：https://wanwang.aliyun.com/" %(domain,suffix)
				if send_mail(mailto_list,"domainCheck",msg):  
					print "success send mail"
				else:  
					print "fail send mail"
				break
			time.sleep(61)
			print 'program is continue...'
	
