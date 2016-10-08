#-*-encoding:utf-8-*-#
'''
version 0.1
查询域名是否被注册，并发送邮件通知
'''
import requests
import smtplib  
from email.mime.text import MIMEText
import re
#换成你的接受邮箱，发送邮箱可以不换
mailto_list=['xxxxxx@xx.xxx'] 
mail_host="smtp.xxxx.com"  #设置服务器
mail_user="xxxx"    #用户名
mail_pass="xxxx"   #口令 
mail_postfix="xxxx.com"  #发件箱的后缀

def whois(domain):
	url = 'http://whois.chinaz.com/%s' %domain
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
	#print url
	res = requests.get(url,headers=headers)
	res_cont = res.content;
	#open('2.txt','wb').write(res_cont)
	s = 'col-red'
	flag = res_cont.find(s)
	if flag>=0:
		return 1,-1,-1,-1
	else:
		time_all = re.findall(r'\d{4}\D+\d{2}\D+\d{2}',res_cont)
		year = time_all[3][0:4]
		month = time_all[3][7:9]
		day = time_all[3][12:14]
		return -1,year,month,day
	#print res_cont
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
if __name__ == '__main__':
	domain = 'choushaddsafbi.com'
	state,year,month,day = whois(domain)
	if state ==-1:
		msg = "域名%s已被注册,到期时间：%s年%s月%s日" %(domain,year,month,day)
	else:
		msg = "域名%s可被注册 注册地址：https://wanwang.aliyun.com/" %domain
	if send_mail(mailto_list,"domainCheck",msg):  
		print "success"
	else:  
		print "fail"
	