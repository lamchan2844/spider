#-*-encoding:utf-8-*-#
'''
version 0.2
��ѯ�����Ƿ�ע�ᣬ�������ʼ�֪ͨ
'''
import requests
import smtplib  
import time
from email.mime.text import MIMEText
import re
#������Ľ������䣬����������Բ���
mailto_list=['907169968@qq.com'] 
mail_host="smtp.sina.com"  #���÷�����
mail_user="chenlinmytest"    #�û���
mail_pass="12345678"   #���� 
mail_postfix="sina.com"  #������ĺ�׺

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
    me="test"+"<"+mail_user+"@"+mail_postfix+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #����һ��ʵ������������Ϊhtml��ʽ�ʼ�
    msg['Subject'] = sub    #��������
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #����smtp������
        s.login(mail_user,mail_pass)  #��½������
        s.sendmail(me, to_list, msg.as_string())  #�����ʼ�
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
				#msg = " ����%s.%s�ѱ�ע��" %(domain,suffix)
			else:
				msg = "����%s.%s�ɱ�ע�� ע���ַ��https://wanwang.aliyun.com/" %(domain,suffix)
				if send_mail(mailto_list,"domainCheck",msg):  
					print "success send mail"
				else:  
					print "fail send mail"
				break
			time.sleep(61)
			print 'program is continue...'
	
