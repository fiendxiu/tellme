#!/usr/bin/python 
#coding:utf-8 
 
import json 
import urllib2 
from urllib2 import URLError 
import sys,argparse
import re 
class zabbix_api: 
        def __init__(self): 
            self.url = 'http://192.168.55.10/zabbix/api_jsonrpc.php' #修改URL
            self.header = {"Content-Type":"application/json"}         
             
             
        def user_login(self): 
            data = json.dumps({ 
                               "jsonrpc": "2.0", 
                               "method": "user.login", 
                               "params": { 
                                          "user": "Admin", #修改用户名
                                          "password": "both-win" #修改密码
                                          }, 
                               "id": 0 
                               }) 
             
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
         
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "\033[041m 用户认证失败，请检查 !\033[0m", e.code 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                #print response['result'] 
                self.authID = response['result'] 
                return self.authID 
             
        def host_get(self,hostName=''): 
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                              "output": "extend",
                              "filter":{"host":hostName} 
                              },
                    "auth": self.user_login(),
                    "id": 1
                    })
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                 
         
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                if hasattr(e, 'reason'): 
                    print 'We failed to reach a server.' 
                    print 'Reason: ', e.reason 
                elif hasattr(e, 'code'): 
                    print 'The server could not fulfill the request.' 
                    print 'Error code: ', e.code 
            else: 
                response = json.loads(result.read()) 
                #print response
                result.close() 
                print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
                for host in response['result']:      
                        status={"0":"OK","1":"Disabled"}
                        available={"0":"Unknown","1":"available","2":"Unavailable"}
                        #print host
                        if len(hostName)==0:
                                print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
                        else:
                                print host['hostid']
                                print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
                                return host['hostid']

        def hostgroup_get(self, hostgroupName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"hostgroup.get", 
                               "params":{ 
                                         "output": "extend", 
                                         "filter": { 
                                                    "name": hostgroupName 
                                                    } 
                                         }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               }) 
             
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                #print result.read()
                response = json.loads(result.read()) 
                result.close() 
                #print response()
                for group in response['result']:
                        if  len(hostgroupName)==0:
                                print "hostgroup:  \033[31m%s\033[0m \tgroupid : %s" %(group['name'],group['groupid'])
                        else:
                                print "hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid'])
                                self.hostgroupID = group['groupid'] 
                                return group['groupid'] 


        def template_get(self,templateName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method": "template.get", 
                               "params": { 
                                          "output": "extend", 
                                          "filter": { 
                                                     "name":templateName                                                        
                                                     } 
                                          }, 
                               "auth":self.user_login(), 
                               "id":1, 
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
                #print response
                for template in response['result']:                
                    if len(templateName)==0:
                        print "template : \033[31m%s\033[0m\t  id : %s" % (template['name'], template['templateid'])
                    else:
                        self.templateID = response['result'][0]['templateid'] 
                        print "Template Name :  \033[31m%s\033[0m "%templateName
                        return response['result'][0]['templateid']
        def hostgroup_create(self,hostgroupName):

            if self.hostgroup_get(hostgroupName):
                print "hostgroup  \033[42m%s\033[0m is exist !"%hostgroupName
                sys.exit(1)
            data = json.dumps({
                              "jsonrpc": "2.0",
                              "method": "hostgroup.create",
                              "params": {
                              "name": hostgroupName
                              },
                              "auth": self.user_login(),
                              "id": 1
                              })
            request=urllib2.Request(self.url,data)

            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request)
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close()
                print "\033[042m 添加主机组:%s\033[0m  hostgroupID : %s"%(hostgroupName,response['result']['groupids'])


                     
        def host_create(self,host,name, hostip, hostgroupName, templateName): 
            if self.host_get(hostip):
                print "\033[041m该主机已经添加!\033[0m" 
                sys.exit(1)

            group_list=[]
            template_list=[]
            for i in hostgroupName.split(','):
                var = {}
                var['groupid'] = self.hostgroup_get(i)
                group_list.append(var)
            for i in templateName.split(','):
                var={}
                var['templateid']=self.template_get(i)
                template_list.append(var)

            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"host.create", 
                               "params":{ 
                                         "host": host,
                                         "name": name, 
                                         "interfaces": [ 
                                         { 
                                         "type": 1, 
                                         "main": 1, 
                                         "useip": 1, 
                                         "ip": hostip, 
                                         "dns": "", 
                                         "port": "10050" 
                                          } 
                                         ], 
                                       "groups": group_list,
                                       "templates": template_list,
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
                print "添加主机 : \033[42m%s\031[0m \tid :\033[31m%s\033[0m" % (hostip, response['result']['hostids']) 



        def host_disable(self,hostip):
                data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                "hostid": self.host_get(hostip),
                "status": 1
                },
                "auth": self.user_login(),
                "id": 1
                })
                request = urllib2.Request(self.url,data)
                for key in self.header:
                        request.add_header(key, self.header[key]) 
                try: 
                        result = urllib2.urlopen(request)
                except URLError as e: 
                        print "Error as ", e 
                else: 
                        response = json.loads(result.read()) 
                        result.close()
                        print '----主机现在状态------------'
                        print self.host_get(hostip)
                     

        def host_delete(self,hostid):
            hostid_list=[]
            #print type(hostid)
            for i in hostid.split(','):
                #var = {}
                #var['hostid'] = self.host_get(i)
                #hostid_list.append(var)
                hostid_list.append(self.host_get(i))
            print hostid_list          
            data=json.dumps({
                                "jsonrpc": "2.0",
                                "method": "host.delete",
                                "params": hostid_list,   
                    "auth": self.user_login(),
                    "id": 1
                    })

            request = urllib2.Request(self.url,data)
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                 
            try: 
                result = urllib2.urlopen(request)
            except Exception,e: 
                print  e
            else: 

                result.close() 
                print "主机 \033[041m %s\033[0m  已经删除 !"%hostid 
        def host_update(self,hostip,oldip,newip):
              hostid=self.host_get(hostip)
              for interfaceid in self.hostinterface_get(hostid,oldip) :              
                data=json.dumps({
                "jsonrpc": "2.0",
                "method": "hostinterface.update",
                "params": {
                       "interfaceid": interfaceid,
                       "ip": newip 
                 },
                "auth": self.user_login(),
                "id": 1
                })
                request = urllib2.Request(self.url,data)
                for key in self.header:
                        request.add_header(key, self.header[key]) 
                try: 
                        result = urllib2.urlopen(request)
                except URLError as e: 
                        print "Error as ", e 
                else: 
                        response = json.loads(result.read()) 
                        result.close()
                        print '----UP主机为新的ＩＰ------------' 
############rodge
        def hostinterface_get(self,hostid,oldip):
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "hostinterface.get",
                    "params": {
                              "output": "extend",
                              "hostids": hostid,
                              "filter": {"ip":oldip}
                              },
                    "auth": self.user_login(),
                    "id": 1
                   })
            request = urllib2.Request(self.url,data)
            for key in self.header:
                request.add_header(key, self.header[key])


            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server could not fulfill the request.'
                    print 'Error code: ', e.code
            else:
                response = json.loads(result.read())
                #print response
                result.close()
                interfaceid_list=[]
                print "主机要修改的数量: \033[31m%s\033[0m"%(len(response['result']))
                for host in response['result']:
                                interfaceid_list.append(host['interfaceid'])
                                #print host['hostid']
                                #print host['interfaceid'] 
                                #print host['ip']
                                
                return interfaceid_list
        def host_jiankong(self,host_name):
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
                                                "value": 1 ,
                                                "host" : host_name
                                                  },
                                      "expandData":"hostname",
                                      "sortfield": "priority",
                                      "sortorder": "DESC"
                                    },
                           "auth": self.user_login(),
                           "id":1              
                   })
            request = urllib2.Request(self.url,data)
            for key in self.header:
                request.add_header(key, self.header[key])


            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server could not fulfill the request.'
                    print 'Error code: ', e.code
            else:
                response = json.loads(result.read())
                #print response
                result.close()
                if len(response['result']) > 0 :
                  for host in response['result']: 
                     #print host['description']
                     pattern1 = re.compile(r'is\s+unavailable\s+by\s+ICMP')
                     pattern2 = re.compile(r'Ping\s+loss\s+is\s+too\s+high') 
                     match1 = pattern1.search(host['description'])
                     match2 = pattern2.search(host['description'])
                     #match = pattern.search('{HOST.NAME} is unavailable by ICMP')
                     if match1:
                        host_status = "Down"
                        print "HostID : %s\t HostName : %s\t Status : %s "%(host['hostid'],host['hostname'],host_status)
                     elif match2 :
                        host_status = "Ping Loss high"
                        print "HostID : %s\t HostName : %s\t Status : %s "%(host['hostid'],host['hostname'],host_status)
                     else :
                        print "HostID : %s\t HostName : %s\t Status : %s "%(host['hostid'],host['hostname'],host['description'])
                     return host['hostid'] 
                else :
                      
                     print "HostID : %s\t Status： UP 或 不存在此主机 "%(host_name)


############################rodge

if __name__ == "__main__":
        zabbix=zabbix_api()
        parser=argparse.ArgumentParser(description='zabbix  api ',usage='%(prog)s [options]')
        parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='查询主机')
        parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='查询主机组')
        parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='查询模板信息')
        parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='添加主机组')
        parser.add_argument('-C','--add-host',dest='addhost',nargs=5,metavar=('hostname',"name",'192.168.2.1', 'test01,test02', 'Template01,Template02'),help='添加主机,多个主机组或模板使用分号')
        parser.add_argument('-d','--disable',dest='disablehost',nargs=1,metavar=('192.168.2.1'),help='禁用主机')
        parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('192.168.2.1'),help='删除主机,多个主机之间用分号')
        parser.add_argument('-U','--update',dest='updatehost',nargs=3,metavar=('hostname' 'oldip' 'newip'),help='up机器ip')
        parser.add_argument('-J','--jiankong',nargs=1,dest='jiankong',help='Check 主机是否有问题') 
        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv)==1:
                print parser.print_help()
        else:
                args=parser.parse_args()

                if args.listhost != 'host' :
                        if args.listhost:
                                zabbix.host_get(args.listhost)
                        else:
                                zabbix.host_get()
                if args.listgroup !='group':
                        if args.listgroup:
                                zabbix.hostgroup_get(args.listgroup)
                        else:
                                zabbix.hostgroup_get()
                if args.listtemp != 'template':
                        if args.listtemp:
                                zabbix.template_get(args.listtemp)
                        else:
                                zabbix.template_get()
                if args.addgroup:
                        zabbix.hostgroup_create(args.addgroup[0])
                if args.addhost:
                        zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2],args.addhost[3],args.addhost[4])
                if args.disablehost:
                        zabbix.host_disable(args.disablehost)
                if args.deletehost:
                        zabbix.host_delete(args.deletehost[0])
                if args.updatehost:
                        zabbix.host_update(args.updatehost[0],args.updatehost[1],args.updatehost[2])
                if args.jiankong:
                        zabbix.host_jiankong(args.jiankong)
