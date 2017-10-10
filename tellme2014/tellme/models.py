#coding: utf8
from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from time import gmtime, strftime
from django.utils.timezone import now, timedelta
# Create your models here.
STATIC_CHOICES = (
    (u'ON', u'ON'),
    (u'OFF',u'OFF'),
     (u'ON_TEST',u'正在TEST'),
    (u'OFF_TEST',u'关闭TEST'),
)
servertype_CHOICES = (
    (u'Fastip', u'Fastip'),
    (u'组网',u'组网'),
    (u'Fastip+组网',u'Fastip+组网'),
    (u'设备销售',u'设备销售'),
    (u'Other',u'Other'),
)
class JituanID(models.Model):
      jtid = models.IntegerField(u'集团ID' ,max_length=255,primary_key=True)
      jtname = models.CharField(u'客户集团名称', max_length=255)
      status = models.CharField(u'状态', max_length=10,choices=STATIC_CHOICES,default=u'ON')
      jtcreate_date = models.DateField(u'创建日期')
      def __unicode__(self):
        return  u'%s -- %s ' % (self.jtid,self.jtname)
      
class Cid(models.Model):
    cid = models.IntegerField(u'CID' ,max_length=255,primary_key=True)
    contractname = models.CharField(u'客户合同名', max_length=50)
    typeid = models.CharField(u'安装名义', max_length=50 , default=u'东莞光联')
    jtid = models.ForeignKey(JituanID,on_delete=models.PROTECT)
    sales  = models.CharField(u'业务员', max_length=50)
    servertype = models.CharField(u'客户服务类型', max_length=10,choices=servertype_CHOICES,blank=True)
    bp  = models.CharField(u'BP', max_length=50, blank=True)
    mrtg_server = models.CharField(u'用户登录查看Mrtg流量服务器', max_length=255, blank=True)
    mrtg_pass = models.CharField(u'mrtg客户账号资料', max_length=255, blank=True)
    netflow_server = models.CharField(u'用户登录Netflow的服务器', max_length=255, blank=True)
    netflow_pass = models.CharField(u'netflow客户账号资料', max_length=255, blank=True)
    App_pass = models.CharField(u'App客户账号资料', max_length=255, blank=True)
    cid_rd = models.CharField(u'VRF_RD', max_length=50 , blank=True)
    status = models.CharField(u'客户状态', max_length=10,choices=STATIC_CHOICES,default=u'ON')
    cidcreate_date = models.DateField(u'创建日期')
    def __unicode__(self):
        return  u'%s --- %s ' % (self.cid,self.contractname)
    class Meta:
        ordering = ['-cid']
     #   get_latest_by = 'cid'

class Site(models.Model):
    cid = models.ForeignKey(Cid,on_delete=models.PROTECT)
    siteid = models.CharField(u'SiteID' ,max_length=255,primary_key=True)
    oldcid = models.CharField(u'旧的CID(old_cid)', max_length=255, blank=True)
    sitename = models.CharField(u'站点名', max_length=50)
    siteaddr  = models.CharField(u'地址', max_length=255)
    contacts  = models.CharField(u'联络人', max_length=50, blank=True)
    sitecontact  = models.CharField(u'联络资料', max_length=50, blank=True)
    siteemail  = models.CharField(u'联络Email', max_length=50, blank=True)
    status = models.CharField(u'站点状态', max_length=10,choices=STATIC_CHOICES,default=u'ON')
    sitecreate_date = models.DateField(u'创建日期')
    def __unicode__(self):
        return  u'%s -- %s ' % (self.cid,self.sitename)
    class Meta:
        ordering = ['-siteid']

class Line(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    lineid = models.CharField(u'LineID' ,max_length=255,primary_key=True)
    lineserviceid = models.CharField(u'LINE服务ID', max_length=50,blank=True)
    lineserver = models.CharField(u'接入服务器', max_length=50)
    pengpop=models.CharField(u'鹏博士POP', max_length=50,help_text="如果接入鹏博士POP，请选择POP区域")
    lineport = models.CharField(u'接入端口', max_length=50,blank=True)
    lineswitch = models.CharField(u'在那台Switch上', max_length=50,blank=True)
    lineswitchport = models.CharField(u'Switch端口', max_length=50,blank=True)
    lineaccesstype = models.CharField(u'接入类型', max_length=50) 
    linejifangtype = models.CharField(u'主/备类型', max_length=50,blank=True,help_text="例如:主光纤,备份线路")
    linewanip = models.CharField(u'WAN_IP', max_length=50, blank=True)
    linelanip = models.CharField(u'LAN_IP', max_length=50, blank=True)
    linejiankongip = models.CharField(u'监控IP地址:', max_length=50)
    linepass  = models.CharField(u'路由器用户和密码', max_length=50, blank=True)
    linebandwidth = models.CharField(u'线路频宽', max_length=50)
    linetype = models.CharField(u'线路厂商和类型', max_length=50, blank=True)
    linequan = models.CharField(u'线路所有权', max_length=50, blank=True)
    linelocalinfo = models.CharField(u'本地线路信息', max_length=50, blank=True)
    linenum =  models.CharField(u'线路编号', max_length=50, blank=True)
    linebaozhanginfo = models.CharField(u'线路报障资料', max_length=255, blank=True)
    lineservicenumber = models.CharField(u'公司服务编号', max_length=255, blank=True)
    linemrtgserver = models.CharField(u'流量服务器server', max_length=255, blank=True)
    linerrdid = models.CharField(u'流量图ID', max_length=50, blank=True)
    lineother = models.CharField(u'其他资料', max_length=65500, blank=True)
    status = models.CharField(u'Line状态', max_length=10,choices=STATIC_CHOICES,default=u'ON')
    linecreate_date = models.DateField(u'创建日期') 
    def __unicode__(self):
        return  u'%s --- %s ' % (self.siteid,self.lineid)
    class Meta:
        ordering = ['-lineid']

class Service(models.Model):
    serviceid = models.CharField(u'ServiceID' ,max_length=255,primary_key=True)
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    servicetype = models.CharField(u'服务类型', max_length=50)
    serviceserviceid = models.CharField(u'服务ID', max_length=255,blank=True)
    serviceshebei= models.CharField(u'包含的设备清单', max_length=255, blank=True)
    servicefeiyong= models.CharField(u'服务费用计算方式', max_length=255, blank=True)
    serviceother = models.CharField(u'其他资料', max_length=255, blank=True)
    status = models.CharField(u'Service状态', max_length=10,choices=STATIC_CHOICES,default=u'ON')
    servicecreate_date = models.DateField(u'创建日期') 
    def __unicode__(self):
        return  u'%s' % (self.servictype)
    class Meta:
        ordering = ['-serviceid']
