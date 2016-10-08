#-*-encoding:utf-8-*-#
'''
version 0.1
��ѯ�����Ƿ�ע�ᣬ�������ʼ�֪ͨ
'''
import requests
import smtplib  
from email.mime.text import MIMEText
import re
#������Ľ������䣬����������Բ���
mailto_list=['xxxxxx@xx.xxx'] 
mail_host="smtp.xxxx.com"  #���÷�����
mail_user="xxxx"    #�û���
mail_pass="xxxx"   #���� 
mail_postfix="xxxx.com"  #������ĺ�׺

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
if __name__ == '__main__':
	domain = 'choushaddsafbi.com'
	state,year,month,day = whois(domain)
	if state ==-1:
		msg = "����%s�ѱ�ע��,����ʱ�䣺%s��%s��%s��" %(domain,year,month,day)
	else:
		msg = "����%s�ɱ�ע�� ע���ַ��https://wanwang.aliyun.com/" %domain
	if send_mail(mailto_list,"domainCheck",msg):  
		print "success"
	else:  
		print "fail"
	