#!/usr/local/bin
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib
import MySQLdb
import urllib2
import cookielib
from bs4 import BeautifulSoup
import MySQLdb
import re
import sys
list=[]
class addmrtg:
    def chamrtg(self,key,linetype):
	    if linetype == "BACKUP":
		loginUrl = "http://183.3.210.251:10080/"
	    else :
		loginUrl = "http://192.168.55.139:10080/"
	    cookie = cookielib.CookieJar()
	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	    postdata = urllib.urlencode({
		    "login_username":"herbiel",
		    "login_password":"he",
		    "action":"login"
		    })
	    loginhtml = opener.open(loginUrl,postdata)
	    gradeUrl2 = loginUrl+"graphs.php?host_id=-1&template_id=-1&filter=%s&graph_rows=30&page=1"%key
	    html2 = opener.open(gradeUrl2,None)
	    content = html2.read()
	    soup = BeautifulSoup(content,"html5lib")
	    result=soup.find("tr",bgcolor='#F5F5F5')
	    list=result.find_all("td")
	    mrtgtitle=list[0].text.strip()
	    p = re.compile(r'id\d+')
	    result=str(result)
	    p = re.compile(r'id=\d+')
	    id=p.findall(result)[0]
	    num = re.compile(r'\d+')
	    mrtgid=num.findall(id)[0]
	    return mrtgid
    def chatellme(self,lineid):
	    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="newtellme", charset="utf8")
	    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	    cursor.execute("select cid,lineport,siteid,contractname,linejifangtype from tellmeview2 where lineid like '%s'"%lineid)
	    line_result=cursor.fetchone()
	    cid="%(cid)s " %line_result
	    siteid="%(siteid)s " %line_result
	    lineport="%(lineport)s " %line_result
	    contractname="%(contractname)s " %line_result
	    linejifangtype="%(linejifangtype)s " %line_result
  	    conn.close();	
	    return cid,siteid,lineport,contractname,linejifangtype
    def chamrtg4(self,cid,lineportnum,linejifangtype,des,link):
	    conn = MySQLdb.connect(host="192.168.253.137", user="bothwin", passwd="both-win", db="trafficflow", charset="utf8")
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute("select cid from tf_user where cid like '%s'"%cid)
	    cid_result=cursor.fetchone()
	    cursor.execute("select * from tf_link where description like '%%%s%%'"%lineportnum)
            result=cursor.fetchone()
	    if cid_result is None and result is None :
	        cursor.execute("insert into tf_user (username,password,cid)values('%s','%s','%s')"%(cid,cid+"zxc",cid))
		cursor.execute("insert into tf_link (description,link,username)values('%s','%s','%s')"%(des,link,cid))
	        conn.commit();
	    elif cid_result is not None and result is None:
	        cursor.execute("insert into tf_link (description,link,username)values('%s','%s','%s')"%(des,link,cid))
	        conn.commit();
	    conn.close();
    def updatetellme(self,mrtgserver,mrtgpass,cid):
            conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="newtellme", charset="utf8")
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	    cursor.execute("select mrtg_pass from tellme_cid where mrtg_pass like '%%%s%%'"%cid)
 	    mrtgpass_result=cursor.fetchone()
	    if mrtgpass_result is None:
	        cursor.execute("update tellme_cid set mrtg_server ='%s',mrtg_pass ='%s' where cid = '%s'"%(mrtgserver,mrtgpass,cid))
		conn.commit();
	    conn.close();
