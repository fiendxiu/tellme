# coding: utf-8
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from models import *
from forms import *
from django.shortcuts import render_to_response,get_object_or_404
from django.template import Template,loader,RequestContext

def paging(data,page):
        #paginator = Paginator(data,30)
        paginator = Paginator(data,30)
        try:
                newpage=int(page)
        except ValueError:
                newpage=1
        try:
                contacts = paginator.page(newpage)
        except PageNotAnInteger:
                contacts = paginator.page(1)
        except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
        return contacts

def Modelskey(key):
        Models =  { 'cid':Cid,
                  'site':Site,
                  'line':Line,
                  'jtid':JituanID,
                  'service':Service,
                }
        return Models[key]

def Formskey(key):
        forms = { 'cid':FromCid,
                  'site':FromSite,
                  'line':FromLine,
                  'jtid':FromJituanID,
                  'service':FromService,
                }
        return forms[key]


def Idkey(key):
        Idkeys = { 'cid':'cid',
                  'site':'siteid',
                  'line':'lineid',
                  'jtid':'jtid',
                  'service':'service',
                }
        return Idkeys[key]

def Forskey(url,pag):
        forskey = { 
                        'jifang':pag.cabinet_set.all(),
                        'jigui':pag.server_set.all(),
                }

        return forskey[url]


def Check_quanxian(request,url,type):
        if url == 'cid' or  url == 'site' or url == 'line'  or url == 'service' :
           if   request.user.has_perm('tellme.'+type+'_'+url):
              return True 
             #errors = "您无此权限,请返回"
             #return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        elif url == 'jtid' :
           #if   request.user.has_perm('tellme.'+type+'_jituanID'):
             if   request.user.has_perm('tellme.'+type+'_jituanid'):
                return True
              # errors = "您无此权限,请返回"
               #return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        else:  
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return  False

def   checkpe(key):
        pe = {  'dga-fastip1':'dga-fastip1-CPE-Template ICMP Ping',
               'dga-fastip2':'dga-fastip2-CPE-Template ICMP Ping',
               'dga-fastip3':'dga-fastip3-CPE-Template ICMP Ping',
               'dga-fastip4':'dga-fastip4-CPE-Template ICMP Ping',
               'dga-mvpnpe1':'dga-mvpnpe1-CPE-Template ICMP Ping',
               'dga-sfastip1': 'dga-sfastip1-CPE-Template ICMP Ping' ,
               'dga-vpnpe1': 'dga-vpnpe1-CPE-Template ICMP Ping' ,
               'gza-vpnpe1': 'gza-vpnpe1-CPE-Template ICMP Ping' ,
               'sza-vpnpe1': 'sza-vpnpe1-CPE-Template ICMP Ping' ,
               'hka-vpnpe1': 'hka-vpnpe1-CPE-Template ICMP Ping' ,
               'hkb-vpnpe1': 'hkb-vpnpe1-CPE-Template ICMP Ping' ,
               'sza-lr2': 'sza-lr2-CPE-Template ICMP Ping' ,
               'other': 'Fnet-Template ICMP Ping',
                }
        return pe[key]

def   checkhostgroup(key):
        hostgroup = {  'dga-fastip1':'FNET-DGA-FASTIP1-CPE',
               'dga-fastip2':'FNET-DGA-FASTIP2-CPE',
               'dga-fastip3':'FNET-DGA-FASTIP3-CPE',
               'dga-fastip4':'FNET-DGA-FASTIP4-CPE',
               'dga-mvpnpe1':'FNET-DGA-MVPNPE1-CPE',
               'dga-sfastip1': 'FNET-DGA-SFASTIP1-CPE' ,
               'dga-vpnpe1': 'FNET-DGA-VPNPE1-CPE' ,
               'gza-vpnpe1': 'FNET-GZA-VPNPE1-CPE' ,
               'sza-vpnpe1': 'FNET-SZA-VPNPE1-CPE' ,
               'hka-vpnpe1': 'FNET-HKA-VPNPE1-CPE' ,
               'hkb-vpnpe1': 'FNET-HKB-VPNPE1-CPE' ,
               'sza-lr2': 'FNET-SZA-LR2-CPE',
               'other': 'FNET-CPE',
                }
        return hostgroup[key]
   

def   zabbix_add(lineid,name,ip,linetype,pe):
        hostgroup=checkhostgroup(pe)
        template=checkpe(pe)
        from zabbix_api import zabbix_api
        zabbix=zabbix_api() 
        return zabbix.host_create(lineid,lineid+'-'+linetype+'-'+name,ip,hostgroup,template)
def   zabbix_del(lineid):
        from zabbix_api import zabbix_api
        zabbix=zabbix_api()
        return  zabbix.host_delete(lineid)
def   zabbix_update(lineid,oldip,newip):
        from zabbix_api import zabbix_api
        zabbix=zabbix_api()
        return zabbix.host_update(lineid,oldip,newip)
  
