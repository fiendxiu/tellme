# Create your views here.
# coding: utf-8
import MySQLdb
from models import *
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,loader,RequestContext
import time,datetime
from forms import *
#from other import paging,Modelskey,Formskey,Forskey,Idkey,Check_quanxian
from other import *
from django.db import IntegrityError
from django.contrib.auth.decorators import permission_required
#from monit import createrrd,todayimage,weeksimage,monthimage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
#from django.forms.models import model_to_dict
import re
from ticketdata import tickets
from newticketdata import newtickets
from configbackup import confadd

@csrf_exempt
def index(request):
        if request.user.is_authenticated():
                if request.method == 'GET':
                        data = Cid.objects.all() 
                        room = paging(data,request.GET.get('page','1'))
                return render_to_response('index.html',{'room':room,'today':datetime.datetime.today()},context_instance=RequestContext(request)) 
        return HttpResponseRedirect('/login/')

def displayold(request,url):
        if request.user.is_authenticated():
                form = Formskey(url)(request.POST)
                if request.method == 'POST':
                        if form.is_valid():
                                form.save()
                                if ( url == 'server' and request.POST['ip'] != ''):
                                        createrrd(request.POST['ip'])
                                return HttpResponseRedirect('/'+url+'/')
                data = Modelskey(url).objects.all()
                room = paging(data,request.GET.get('page','1'))
                return render_to_response(url+'.html',{'form':form,'room':room,'today':datetime.datetime.today()},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')


def display(request,url):
        curl = request.get_full_path()
        if request.user.is_authenticated():
             jieguo = False
             form = Formskey(url)(request.POST)
             if url == 'site' or url == 'line' or url == 'service' : 
                 if request.method == 'POST' : 
                     if request.POST['q'] :
                          data = Modelskey(url).objects.filter(pk__icontains=request.POST['q']).exclude(status__icontains='OFF')
                         # room = paging(data,request.GET.get('page','1'))
                          room = paging(data,1)
                          request.session['url_request'] = request.POST['q']
                          jieguo = True
                     else:
                         #del request.session['url_request']
                         data = Modelskey(url).objects.exclude(status__icontains='OFF').all()[:15]
                         room = paging(data,request.GET.get('page','1'))
                 else:
                     if 'url_request' in request.session and request.GET.get('page'):
                         try:
                             data = Modelskey(url).objects.filter(pk__icontains=request.session['url_request']).exclude(status__icontains='OFF')
                             room = paging(data,request.GET.get('page','1'))
                             jieguo = True
                         except ObjectDoesNotExist:
                             del request.session['url_request']
                             data = Modelskey(url).objects.exclude(status__icontains='OFF').all()[:15]
                             room = paging(data,request.GET.get('page','1'))                           
                     else:
                         data = Modelskey(url).objects.exclude(status__icontains='OFF').all()[:15]
                         room = paging(data,request.GET.get('page','1'))
                
                 return render_to_response('search_type.html',{'curl':curl,'room':room,'jieguo':jieguo,'type':url,'today':datetime.datetime.today()},context_instance=RequestContext(request))
             elif url == 'jtid' :
                  jieguo = False
                  if request.method == 'POST' and  request.POST['q'] :
                     data = JituanID.objects.filter(jtid__icontains=request.POST['q']).exclude(status__icontains='OFF')
                     if len(data) > 0 :
                        jieguo = True
                  else:
                     data = Modelskey(url).objects.exclude(status__icontains='OFF').all()
                  room = paging(data,request.GET.get('page','1'))
                  return render_to_response(url+'.html',{'curl':curl,'form':form,'room':room,'type':url,'jieguo':jieguo,'today':datetime.datetime.today()},context_instance=RequestContext(request))

             else:
                jieguo = False 
                if request.method == 'POST' and  request.POST['q'] :
                     data = Cid.objects.filter(cid__icontains=request.POST['q']).exclude(status__icontains='OFF')
                     if len(data) > 0 :
                        jieguo = True                                         
                else:
                     #data = Modelskey(url).objects.all()[-15:0]
                     data = Modelskey(url).objects.exclude(status__icontains='OFF').all()[:15]
                room = paging(data,request.GET.get('page','1'))
                return render_to_response(url+'.html',{'curl':curl,'form':form,'room':room,'type':url,'jieguo':jieguo,'today':datetime.datetime.today()},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')

def addcid(request,url):
        if request.user.is_authenticated():
              if  Check_quanxian(request,url,'add'):
                if request.method == 'POST':
                        form = Formskey(url)(request.POST)
                        if form.is_valid():
                            m=form.save(commit=False)
                            if m.sales.endswith('@fnetlink.com'):
                                cid = request.POST['cid']
                                form.save()
                                #return HttpResponseRedirect('/'+url+'/')
                               
                                return render_to_response('cidaddok.html',{'cid':cid},context_instance=RequestContext(request))
                            else:
                                errors = "业务员邮箱格式错误"
                                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                        else:
                                return render_to_response(url+'add.html',locals(),context_instance=RequestContext(request))
                form = Formskey(url)
                
                try: 
                   max_id = Cid.objects.filter(jtid_id=1000).order_by("-cid")[0].cid
		   maxp_id = Cid.objects.filter(jtid_id=1009).order_by("-cid")[0].cid
                except:             
                   newcid=8000
		   newcid1=8000
                else:
                   newcid=max_id+1
		   newcid1=maxp_id+1
                return render_to_response(url+'add.html',{'form':form,'newcid':newcid,'newcid1':newcid1},context_instance=RequestContext(request))
              else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))  
        return HttpResponseRedirect('/login/')


def addsite(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'add'):  
                if request.method == 'POST':
                        request.POST=request.POST.copy()
                        request.POST['siteid']=id+request.POST['siteid']
                        form = Formskey(url)(request.POST)
                        form.fields['cid'].queryset = Cid.objects.filter(cid=id)
                        if form.is_valid():
                                form.save()
                                #return HttpResponseRedirect('/'+url+'/')
                                form = Formskey(url)()
                                form.fields['cid'].queryset = Cid.objects.filter(cid=id)
                                info=request.POST['siteid']
                                return render_to_response(url+'add.html',{'form':form,'url':url,'info':info},context_instance=RequestContext(request))
                        else:
                                return render_to_response(url+'add.html',locals(),context_instance=RequestContext(request))
                else:
                   form = Formskey(url)() 
                   form.fields['cid'].queryset = Cid.objects.filter(cid=id) 
                   return render_to_response(url+'add.html',{'form':form,'url':url},context_instance=RequestContext(request)) 
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request)) 
        return HttpResponseRedirect('/login/')


def addline(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'add'):
                if request.method == 'POST':
                        request.POST=request.POST.copy()
                        request.POST['lineid']=id+request.POST['lineid']
                        form = Formskey(url)(request.POST)
                        form.fields['siteid'].queryset = Site.objects.filter(pk=id)
                        if form.is_valid():
                                form.save()
                                #zabbix_add(request.POST['lineid'],Site.objects.get(siteid=id).sitename,request.POST['linejiankongip'],)
                                #zabbix_add(request.POST['lineid'],Site.objects.get(siteid=id).sitename,request.POST['linejiankongip'],request.POST['linejifangtype'],request.POST['lineserver'])
                                #return HttpResponseRedirect('/'+url+'/')
                                confadd(request.POST['lineid'],request.POST['linejiankongip'])
                                form = Formskey(url)()
                                form.fields['siteid'].queryset = Site.objects.filter(siteid=id)
                                #sitename=Site.objects.get(siteid=id).sitename
                                info=request.POST['lineid']
                              
                                return render_to_response(url+'add.html',{'form':form,'url':url,'info':info},context_instance=RequestContext(request))
                        else:
                                return render_to_response(url+'add.html',locals(),context_instance=RequestContext(request))
                else:
                   form = Formskey(url)() 
                   form.fields['siteid'].queryset = Site.objects.filter(pk=id) 
                   return render_to_response(url+'add.html',{'form':form,'url':url},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')

def addservice(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'add'):
                if request.method == 'POST':
                        request.POST=request.POST.copy()
                        request.POST['serviceid']=id+request.POST['serviceid']
                        form = Formskey(url)(request.POST)
                        form.fields['siteid'].queryset = Site.objects.filter(pk=id)
                        if form.is_valid():
                                form.save()
                                #return HttpResponseRedirect('/'+url+'/')
                                form = Formskey(url)()
                                form.fields['siteid'].queryset = Site.objects.filter(siteid=id)
                                info=request.POST['serviceid']
                                return render_to_response(url+'add.html',{'form':form,'url':url,'info':info},context_instance=RequestContext(request))
                        else:
                                return render_to_response(url+'add.html',locals(),context_instance=RequestContext(request))
                else:
                   form = Formskey(url)()
                   form.fields['siteid'].queryset = Site.objects.filter(pk=id)
                   return render_to_response(url+'add.html',{'form':form,'url':url},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')


def addjtid(request,url):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'add'):
                if request.method == 'POST':
                        form = Formskey(url)(request.POST)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/'+url+'/')
                        else:
                                return render_to_response(url+'add.html',locals(),context_instance=RequestContext(request))
                form = Formskey(url)
                return render_to_response(url+'add.html',{'form':form},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')




def editjtid(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'change'):
                Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                if request.method == 'POST':
                        form = Formskey(url)(request.POST,instance=Modelsurl)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/'+url+'/')
                form = Formskey(url)(instance=Modelsurl)
                return render_to_response('jtidedit.html',{'form':form,'url':url,'id':id},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request)) 
        return HttpResponseRedirect('/login/')



def editcid(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'change'): 
                Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                if request.method == 'POST':
                        form = Formskey(url)(request.POST,instance=Modelsurl)
                        if form.is_valid():
                            m=form.save(commit=False)
                            if m.sales.endswith('@fnetlink.com'):
                                form.save()
                                editurl=url+'/edit/'+id
                                return HttpResponseRedirect('/'+editurl+'/')
                            else:
                                errors = "业务员邮箱格式错误"
                                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                form = Formskey(url)(instance=Modelsurl)
                return render_to_response('cidedit.html',{'form':form,'url':url,'id':id},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request)) 
        return HttpResponseRedirect('/login/')


def editsite(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'change'):
                Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                #Modelsurl.siteid =re.findall(r"\d?([A-Z])", id)[0]
                if request.method == 'POST':
                        #request.POST=request.POST.copy()
                        #request.POST['siteid']=re.findall(r"(\d+)[A-Z]$", id)[0]+request.POST['siteid']
                        form = Formskey(url)(request.POST,instance=Modelsurl)
                        if form.is_valid():
                                form.save()
                                editurl=url+'/edit/'+id
                                return HttpResponseRedirect('/'+editurl+'/')
                form = Formskey(url)(instance=Modelsurl)
                return render_to_response(url+'edit.html',{'form':form,'url':url,'id':id},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')


def editline(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'change'):
                Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                #Modelsurl.lineid =re.findall(r"\d?[A-Z](\d+)$", id)[0]
                if request.method == 'POST':
                        #request.POST=request.POST.copy()
                        #request.POST['lineid']=id+request.POST['lineid']
                        #request.POST['lineid']=+request.POST['lineid']re.findall(r"\d?[A-Z](\d+)$", id)[0]+request.POST['lineid']
                        form = Formskey(url)(request.POST,instance=Modelsurl)
                        if form.is_valid():
                                form.save()
                                editurl=url+'/edit/'+id                                
                                return HttpResponseRedirect('/'+editurl+'/')
                form = Formskey(url)(instance=Modelsurl)
                return render_to_response(url+'edit.html',{'form':form,'url':url,'id':id},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')

def editservice(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'change'):
                Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                if request.method == 'POST':
                       
                        form = Formskey(url)(request.POST,instance=Modelsurl)
                        if form.is_valid():
                                form.save()
                                editurl=url+'/edit/'+id
                                return HttpResponseRedirect('/'+editurl+'/')
                form = Formskey(url)(instance=Modelsurl)
                return render_to_response(url+'edit.html',{'form':form,'url':url,'id':id},context_instance=RequestContext(request))
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')


def delete(request,url,id):
        if request.user.is_authenticated():
             if  Check_quanxian(request,url,'delete'):
                Del = get_object_or_404(Modelskey(url),pk=id)
                try:
                        Del.delete()
                        if url == 'line' :
                           zabbix_del(id)
                except  IntegrityError:
                        errors = "底下有分类数据未清空！无法删除"
                        return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                else:
                        return HttpResponseRedirect('/'+url+'/')
             else:
                errors = "您无此权限,请返回"
                return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')

 
def list(request,url,id,flag):
        curl = request.get_full_path()
        if request.user.is_authenticated():
                #pag = Modelskey(url).objects.get(siteid=id)
                if url == 'jtid' and flag == '1':
                        tempdata = JituanID.objects.filter(jtid=id)
                        jtdata = tempdata.exclude(status__exact="OFF") 
                        tempdata = Cid.objects.filter(jtid_id=id)
                        ciddata = tempdata.exclude(status__exact="OFF")
                        cidroom = paging(ciddata,request.GET.get('page','1'))
                        jtroom =  paging(jtdata,request.GET.get('page','1'))                        
                        return render_to_response(url+'list.html',{'curl':curl,'cidroom':cidroom ,'jtroom':jtroom ,'room':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                elif url == 'jtid' and flag == '0':
                        jtdata = JituanID.objects.filter(jtid=id)
                        ciddata = Cid.objects.filter(jtid_id=id)
                        cidroom = paging(ciddata,request.GET.get('page','1'))
                        jtroom =  paging(jtdata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'cidroom':cidroom ,'jtroom':jtroom ,'room':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                if url == 'cid' and flag == '1':
                        Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                        form = Formskey(url)(instance=Modelsurl)
                        tempdata = Modelskey(url).objects.filter(cid=id)
                        ciddata = tempdata.exclude(status__exact="OFF")
                        tempdata = Site.objects.filter(cid_id=id)
                        sitedata = tempdata.exclude(status__exact="OFF")
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        siteroom = paging(sitedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'form':form,'cidroom':cidroom ,'room':siteroom ,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                elif url == 'cid' and flag == '0':
                        Modelsurl = get_object_or_404(Modelskey(url),pk=id)
                        form = Formskey(url)(instance=Modelsurl)
                        ciddata = Modelskey(url).objects.filter(cid=id)
                        sitedata = Site.objects.filter(cid_id=id)
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        siteroom = paging(sitedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'form':form,'cidroom':cidroom ,'room':siteroom ,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                if url == 'site' and flag == '1':
                        cidnum =re.findall(r"^(\d+)[A-Z][a-z]?$", id)[0]
                        #//cidnum='2014'
                        tempdata =  Cid.objects.filter(cid=cidnum) 
                        ciddata = tempdata.exclude(status__exact="OFF")
                        tempdata = Modelskey(url).objects.filter(siteid=id) 
                        sitedata = tempdata.exclude(status__exact="OFF")
                        newticket=newtickets(id)
                        ticket=tickets(id)
                        tempdata = Line.objects.filter(siteid_id=id)
                        linedata = tempdata.exclude(status__exact="OFF")
                        tempdata = Service.objects.filter(siteid_id=id)
                        servicedata = tempdata.exclude(status__exact="OFF")
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        siteroom = paging(sitedata,request.GET.get('page','1'))
                        lineroom = paging(linedata,request.GET.get('page','1'))
                        serviceroom = paging(servicedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'cidroom':cidroom ,'siteroom':siteroom ,'room':lineroom ,'serviceroom':serviceroom,'today':datetime.datetime.today(),'flag':flag,'newticket':newticket,'ticket':ticket},context_instance=RequestContext(request))
                elif url == 'site' and flag == '0':
                        cidnum =re.findall(r"^(\d+)[A-Z][a-z]?$", id)[0]
                        #//cidnum='2014'
                        ciddata = Cid.objects.filter(cid=cidnum)
                        sitedata = Modelskey(url).objects.filter(siteid=id)
                        newticket=newtickets(id)
                        ticket=tickets(id)
                        linedata = Line.objects.filter(siteid_id=id)
                        servicedata = Service.objects.filter(siteid_id=id)
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        siteroom = paging(sitedata,request.GET.get('page','1'))
                        lineroom = paging(linedata,request.GET.get('page','1'))
                        serviceroom = paging(servicedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'cidroom':cidroom ,'siteroom':siteroom ,'room':lineroom ,'serviceroom':serviceroom,'today':datetime.datetime.today(),'flag':flag,'newticket':newticket,'ticket':ticket},context_instance=RequestContext(request))
                if url == 'line' and flag == '1':
                        tempdata = Modelskey(url).objects.filter(lineid=id)  
                        linedata = tempdata.exclude(status__exact="OFF")
                        siteroom=linedata[0].siteid
                        #//sitedata=a.objects.all()
                        #//siteroom =  paging(sitedata,request.GET.get('page','1'))
                        tempdata = Cid.objects.filter(cid=siteroom.cid_id)
                        ciddata = tempdata.exclude(status__exact="OFF")
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        lineroom =  paging(linedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'room': lineroom,'site':siteroom,'cidroom':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                elif url == 'line' and flag == '0':
                        linedata = Modelskey(url).objects.filter(lineid=id)
                        siteroom=linedata[0].siteid
                        #//sitedata=a.objects.all()
                        #//siteroom =  paging(sitedata,request.GET.get('page','1'))
                        ciddata = Cid.objects.filter(cid=siteroom.cid_id)
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        lineroom =  paging(linedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'room': lineroom,'site':siteroom,'cidroom':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                if url == 'service' and flag == '1':
                        tempdata = Modelskey(url).objects.filter(serviceid=id)
                        servicedata = tempdata.exclude(status__exact="OFF")
                        siteroom=servicedata[0].siteid
                        tempdata = Cid.objects.filter(cid=siteroom.cid_id)
                        ciddata = tempdata.exclude(status__exact="OFF")
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        serviceroom =  paging(servicedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'room': serviceroom,'site':siteroom,'cidroom':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                elif url == 'service' and flag == '0':
                        servicedata = Modelskey(url).objects.filter(serviceid=id)
                        siteroom=servicedata[0].siteid
                        ciddata = Cid.objects.filter(cid=siteroom.cid_id)
                        cidroom =  paging(ciddata,request.GET.get('page','1'))
                        serviceroom =  paging(servicedata,request.GET.get('page','1'))
                        return render_to_response(url+'list.html',{'curl':curl,'room': serviceroom,'site':siteroom,'cidroom':cidroom,'today':datetime.datetime.today(),'flag':flag},context_instance=RequestContext(request))
                return render_to_response(url+'list.html',{'curl':curl,'cidroom':cidroom ,'room':siteroom ,'today':datetime.datetime.today()},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')

@csrf_exempt
def search(request):
        curl = request.get_full_path()
        filterOff = "off"
        if request.user.is_authenticated():
                error = False
                if 'q' in request.GET:
                        q = request.GET['q']
			if '酒店' in q:
				q=''
                        info = request.GET['info']
                        if 'filterOff' in request.GET:
                                filterOff = request.GET['filterOff']
                        if not q:
                                error = True
                        else:
                            if info == "cid" : 
                               if filterOff == "on":
                                       tempdata = Cid.objects.filter(cid__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Cid.objects.filter(cid__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'cid'
                            elif info == "hetong" :
                               if filterOff == "on":
                                       tempdata = Cid.objects.filter(contractname__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF") 
                               else:
                                       data = Cid.objects.filter(contractname__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'cid'
                            elif info == "sitename" :
                               if filterOff == "on":
                                       tempdata = Site.objects.filter(sitename__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Site.objects.filter(sitename__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'site'
                            elif info == "siteaddr" :
                               if filterOff == "on":
                                       tempdata = Site.objects.filter(siteaddr__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Site.objects.filter(siteaddr__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'site'
                            elif info == "cidcont" :
                               if filterOff == "on":
                                       tempdata = Site.objects.filter(sitecontact__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Site.objects.filter(sitecontact__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'site'
                            elif info == "ip" :
                               if filterOff == "on":
                                       tempdata = Line.objects.filter(Q(linewanip__icontains=q) | Q(linelanip__icontains=q))
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Line.objects.filter(Q(linewanip__icontains=q) | Q(linelanip__icontains=q))
                               room = paging(data,request.GET.get('page','1'))
                               type = 'line'
                            elif info == "old_CID" :
                               if filterOff == "on":
                                       tempdata = Site.objects.filter(oldcid__icontains=q)
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Site.objects.filter(oldcid__icontains=q)
                               room = paging(data,request.GET.get('page','1'))
                               type = 'site'
			    elif info == "PE" :
                               if filterOff == "on":
                                       tempdata = Line.objects.filter(Q(lineserver__icontains=q) | Q(linelanip__icontains=q))
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Line.objects.filter(Q(lineserver__icontains=q) | Q(linelanip__icontains=q))
                               room = paging(data,request.GET.get('page','1'))
                               type = 'line'
                            elif info == "svrnum" :
                               if filterOff == "on":
                                       tempdata = Line.objects.filter(Q(lineservicenumber__icontains=q))
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Line.objects.filter(Q(lineservicenumber__icontains=q))
                               room = paging(data,request.GET.get('page','1'))
                               type = 'line'
                            elif info == "linenum" :
                               if filterOff == "on":
                                       tempdata = Line.objects.filter(Q(linenum__icontains=q))
                                       data = tempdata.exclude(status__exact="OFF")
                               else:
                                       data = Line.objects.filter(Q(linenum__icontains=q))
                               room = paging(data,request.GET.get('page','1'))
                               type = 'line'
                            else:
                               error = True
                            if len(data) < 1:
                                        error = True
                            return render_to_response('searchlist.html',{'curl':curl,'room':room,'error':error,'type':type,'today':datetime.datetime.today()},context_instance=RequestContext(request))
                return render_to_response('index.html',{'error':error})
        return HttpResponseRedirect('/login/')
def addmonitor(request,url,id):
        #dgb_proxyid=14800;sha_proxyid=14753;szb_proxyid=14801;zabbix_serverid=10166;other=0;
        res=id
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="newtellme", charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select linejiankongip,linejifangtype,lineserver,sitename from tellmeview4 where lineid like '%s'"%id)
        line_result=cursor.fetchone()
        lineserver="%(lineserver)s " %line_result
        sitename="%(sitename)s " %line_result
        linejifangtype="%(linejifangtype)s " %line_result
        linejiankongip="%(linejiankongip)s " %line_result
        linejiankongip=linejiankongip.strip()
        PE=lineserver[0:3]
        PE=PE.upper()
	ser=lineserver.upper()
	ser=ser.strip()
	ser="FNET-"+ser+"-CPE"
	grouplist=[]
	grouplist.append(ser)
        conn.close()
        hostname=id+"-"+linejifangtype+"-"+sitename
        import sys
        sys.path.append('/var/www/django/tellme2014/tellme2014/tellme/')
        from zabbix_api import zabbix_api
        zabbix=zabbix_api()
        if PE in "DGB" and "bk" not in lineserver:
                proxyid=14800
		peproxy=PE+"-PROXY"
        elif PE in "SHA":
                proxyid=14753
		peproxy=PE+"-PROXY"
        elif PE in "SZB" and "bk" not in lineserver:
                proxyid=14801
		peproxy=PE+"-PROXY"
        else :
                proxyid=0
		peproxy=""
	if peproxy != "":
		grouplist.append(peproxy)
	grouplist.append("Fnet-ISO-3")
        grouplist.append("FNET-CPE")
	pestr=u",".join(grouplist)
        zabbix.host_create(id,hostname,linejiankongip,pestr,'Fnet-CPE ICMP Ping',proxyid)
        return render_to_response("messages.html",locals(),context_instance=RequestContext(request))
def mrtgadd(request,url,id):
	import mrtg
	addmrtg=mrtg.addmrtg()
	(cid,siteid,lineport,contractname,linejifangtype)=addmrtg.chatellme(id)
	type=str(linejifangtype.strip())
        cid =cid.strip()
        lineport = lineport.strip()
        mrtgid=addmrtg.chamrtg(lineport,type)
        contractname=contractname.strip()
        contractname=contractname.replace('测试',"")
	ontractname=contractname.replace('-DS',"")
        des = str(contractname)+"-"+str(id)+"-Traffic-|HK-Outbound-"+str(lineport)+"-"+str(linejifangtype)
	if type == "BACKUP":
                link = "http://183.3.210.251:10080/graph_image1.php?local_graph_id="+mrtgid
        else:
                link = "http://mrtg.fnetlink.com.hk:10080/graph_image1.php?local_graph_id="+mrtgid
        addmrtg.chamrtg4(cid,lineport,linejifangtype,des,link)
        mrtgserver="http://mrtg4.fnetlink.com:10080/"
        mrtgpass="账号:"+cid+","+"密码:"+cid+"zxc"
        addmrtg.updatetellme(mrtgserver,mrtgpass,cid)	
	return render_to_response("mrtgmess.html",locals(),context_instance=RequestContext(request))
