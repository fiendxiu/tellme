#!/usr/bin/python
#coding:utf-8
import json
import urllib2
from urllib2 import URLError
import sys
#接收人
mailtolist = ['test@163.com',]
#格式：zabbix地址，zabbix帐号，zabbix密码，邮件标题
zabbix_addresses=['http://192.168.55.10/zabbix,admin,both-win,test1','http://test2.zabbix.com,admin,123456,test2','http://test3.zabbix.com,admin,123456,test3']
class ZabbixTools:
    def __init__(self,address,username,password):
                                                                       
        self.address = address
        self.username = username
        self.password = password
                                                                       
        self.url = '%s/api_jsonrpc.php' % self.address
        self.header = {"Content-Type":"application/json"}
                                                                       
                                                                       
                                                                       
    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": self.username,
                                      "password": self.password
                                      },
                           "id": 0
                           })
                                                                       
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
                                                                   
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, please Check your name and password:", e.code
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            self.authID = response['result']
            return self.authID
                                                                           
    def trigger_get(self):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"trigger.get",
                           "params": {
                                      "output": [
                                                "triggerid",
                                                "description",
                                                "priority"
                                                ],
                                      "filter": {
                                                 "value": 1
                                                 },
                                      "expandData":"hostname",
                                      "sortfield": "priority",
                                      "sortorder": "DESC"
                                    },
                           "auth": self.user_login(),
                           "id":1              
        })
                                                                       
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
                                                                       
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            issues = response['result']
            content = ''
            if issues:
                for line in issues:
                    content = content + "%s:%s\r\n" % (line['host'],line['description'])
            return content
                                                                           
if __name__ == "__main__":
    for zabbix_addres in zabbix_addresses:
        address,username,password,subject = zabbix_addres.split(',')
        z = ZabbixTools(address=address, username=username, password=password)
        content = z.trigger_get()
    print "Done!"
