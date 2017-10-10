# coding: utf-8
from django import forms
from django.forms import Textarea, Select,TextInput
from models import *
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
import string

SITEOPT=[]
#ZM1=string.ascii_uppercase
ZM2=string.ascii_uppercase

#for zm in ZM :
#   SITEOPT.append((zm,zm))
ZM=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Aa','Ab','Ac','Ad','Ae','Af','Ag','Ah','Ai','Aj','Ak','Al','Am','An','Ao','Ap','Aq','As','At','Au','Av','Aw','Ax','Ay','Az','Ba','Bb','Bc','Bd','Be','Bf','Bg','Bh','Bi','Bj','Bk','Bl','Bm','Bn','Bo','Bp','Bq','Br','Bs','Bt','Bu','Bv','Bw','Bx','By','Bz']
for zm in ZM :
   SITEOPT.append((zm,zm))
LINEOPT=[]
SHUZI=range(1,120)
for sz in SHUZI :
   LINEOPT.append((sz,sz))
SERVICEOPT=[]
SERVICEID=['_S1','_S2','_S3','_S4','_S5','_S6','_S7','_S8','_S9',]
#SERVICEID=['S1','S2']
for sid in SERVICEID :
	SERVICEOPT.append((sid,sid))
PE=[('dga-fastip1','dga-fastip1'),('dga-fastip2','dga-fastip2'),('dga-fastip3','dga-fastip3'),('dga-fastip4','dga-fastip4'),('dga-mvpnpe1','dga-mvpnpe1'),('dga-vpnpe1','dga-vpnpe1'),('dga-ipsec1','dga-ipsec1'),('dga-flr1','dga-flr1'),('dga-bk1','dga-bk1'),('dga-vpnbk1','dga-vpnbk1'),('dga-sfastip1','dga-sfastip1'),('dga-acvpnpe1','dga-acvpnpe1'),('sza-fastip1','sza-fastip1'),('sza-vpnpe1','sza-vpnpe1'),('sza-flr2','sza-flr2'),('sza-flr3','sza-flr3'),('sza-sfastip1','sza-sfastip1'),('sza-bk1','sza-bk1'),('gza-vpnpe1','gza-vpnpe1'),('hka-vpnpe1','hka-vpnpe1'),('hkb-lr1','hkb-lr1'),('hkb-lr2','hkb-lr2'),('sza-lr1','sza-lr1'),('sza-lr2','sza-lr2'),('sha-vpnpe1','sha-vpnpe1'),('sha-flr1','sha-flr1'),('hkh-flr1','hkh-flr1'),('hkh-flr2','hkh-flr2'),('hkh-vpnpe1','hkh-vpnpe1'),('hkh-acvpnpe1','hkh-acvpnpe1'),('hkh-us1','hkh-us1'),('usa-xen1','usa-xen1'),('usa-fnet1','usa-fnet1'),('hki-dyx1','hki-dyx1'),('twb-vpnpe1','twb-vpnpe1'),('szb-fastip1','szb-fastip1'),('szb-acvpnpe1','szb-acvpnpe1'),('szb-vpnpe1','szb-vpnpe1'),('szb-flr1','szb-flr1'),('szb-flr2','szb-flr2'),('szb-sfastip1','szb-sfastip1'),('szb-xen1','szb-xen1'),('szb-bk1','szb-bk1'),('szb-ipsec1','szb-ipsec1'),('none','none'),('dgb-fastip1','dgb-fastip1'),('dgb-sfastip1','dgb-sfastip1'),('dgb-flr1','dgb-flr1'),('dgb-flr2','dgb-flr2'),('dgb-bk1','dgb-bk1'),('dgb-coresw1','dgb-coresw1'),('dgb-coresw2','dgb-coresw2'),('dgb-acsw1','dgb-acsw1'),('dgb-vpnpe1','dgb-vpnpe1'),('dgb-acvpnpe1','dgb-acvpnpe1'),('dgb-xen1','dgb-xen1'),('dgb-bpflr1','dgb-bpflr1'),('dgb-fastip2','dgb-fastip2'),('dgb-ipsec1','dgb-ipsec1'),('其他运营商','其他运营商'),('鹏博士POP','鹏博士POP'),('DYX POP','DYX POP'),('客户路由器','客户路由器'),('aua-xen1','aua-xen1'),('uka-xen1','uka-xen1'),('dea-xen1','dea-xen1')]

LINETYPE=[('OPENVPN-Tunnel','OPENVPN-Tunnel'),('NHRP-Tunnel','NHRP-Tunnel'),('GRE-Tunnel','GRE-Tunnel'),('L2TP-Tunnel','L2TP-Tunnel'),('IPLC','IPLC'),('IEPL','IEPL'),('DPLC','DPLC'),('MSTP','MSTP'),('SDH','SDH'),('PPTP','PPTP'),('SSL','SSL'),('IPSEC','IPSEC')]

LINETYPE=[('OPENVPN-Tunnel','OPENVPN-Tunnel'),('NHRP-Tunnel','NHRP-Tunnel'),('GRE-Tunnel','GRE-Tunnel'),('L2TP-Tunnel','L2TP-Tunnel'),('IPLC','IPLC'),('IEPL','IEPL'),('DPLC','DPLC'),('MSTP','MSTP'),('SDH','SDH'),('PPTP','PPTP'),('SSL','SSL'),('IPSEC','IPSEC')]

pengpop=[('none','none'),('沈阳','沈阳'),('长春','长春'),('大连','大连'),('洽尔滨','洽尔滨'),('北京','北京'),('武汉','武汉'),('长沙','长沙'),('郑州','郑州'),('洛阳','洛阳'),('上海','上海'),('南京','南京'),('福州','福州'),('厦门','厦门'),('宁波','宁波'),('温州','温州'),('杭州','杭州'),('合肥','合肥'),('无锡','无锡'),('青岛','青岛'),('济南','济南'),('南宁','南宁'),('成都','成都'),('广州','广州'),('深圳','深圳'),('西安','西安'),('昆明','昆明'),('贵阳','贵阳'),('惠州','惠州'),('东莞','东莞'),('海口','海口'),('重庆','重庆'),('蘇州','蘇州'),('甘肃兰州','甘肃兰州'),('河北廊坊','河北廊坊'),('唐>山','唐山'),('香港','香港')]

linelocalinfo=[('',''),('CUSTOMER-CROSS-CONNECT','CUSTOMER-CROSS-CONNECT'),('CUSTOMER-Bare Fiber','CUSTOMER-Bare Fiber'),('CUSTOMER-SDH','CUSTOMER-SDH'),('CUSTOMER-MSTP','CUSTOMER-MSTP'),('CUSTOMER-ADSL','CUSTOMER-ADSL'),('CUSTOMER-PON','CUSTOMER-PON'),('CUSTOMER-MAN','CUSTOMER-MAN'),('CUSTOMER-4G','CUSTOMER-4G'),('CUSTOMER-Share Fiber','CUSTOMER-Share Fiber'),('FNETLINK-CROSS-CONNECT','FNETLINK-CROSS-CONNECT'),('FNETLINK-Bare Fiber','FNETLINK-Bare Fiber'),('FNETLINK-SDH','FNETLINK-SDH'),('FNETLINK-MSTP','FNETLINK-MSTP'),('FNETLINK-ADSL','FNETLINK-ADSL'),('FNETLINK-PON','FNETLINK-PON'),('FNETLINK-MAN','FNETLINK-MAN'),('FNETLINK-4G','FNETLINK-4G'),('FNETLINK-Share Fiber','FNETLINK-Share Fiber')]

LINEJIFATYPE=[('MAIN','MAIN'),('BACKUP','BACKUP')]
MRTGSERVER=[('mrtg.twowin.com.cn:10080','MRTG1'),('202.173.255.28:10080/cacti/','MRTG2'),('mrtg.fnetlink.com.hk:10080','MRTG3')]

newlinetype=[('OPENVPN-Tunnel','OPENVPN-Tunnel'),('NHRP-Tunnel','NHRP-Tunnel'),('GRE-Tunnel','GRE-Tunnel'),('L2TP-Tunnel','L2TP-Tunnel'),('IPLC','IPLC'),('IEPL','IEPL'),('DPLC','DPLC'),('MSTP','MSTP'),('SDH','SDH'),('PPTP','PPTP'),('SSL','SSL'),('IPSEC','IPSEC'),('FastIP-Tunnel','FastIP-Tunnel'),('FastIP-Circuit','FastIP-Circuit'),('組網-Tunnel-MPLSVPN-FNet','組網-Tunnel-MPLSVPN-FNet'),('組網-Circuit-MPLSVPN-FNet','組網-Circuit-MPLSVPN-FNet'),('組網-Tunnel-NNI-FNet-DrPeng','組網-Tunnel-NNI-FNet-DrPeng'),('組網-Circuit-NNI-FNet-DrPeng','組網-Circuit-NNI-FNet-DrPeng'),('組網-Circuit-NNI-DrPeng-FNet','組網-Circuit-NNI-DrPeng-FNet'),('組網-Circuit-P2P-Clien','組網-Circuit-P2P-Clien'),('組網-Tunnel-P2P-Client','組網-Tunnel-P2P-Client'),('組網-Tunnel-P2MP-Client','組網-Tunnel-P2MP-Client'),('Monitor-Tunnel','Monitor-Tunnel'),('FastIP-FirstTunnel','FastIP-FirstTunnel'),('FastIP-SecondaryTunnel','FastIP-SecondaryTunnel'),('組網-FirstTunnel-MPLSVPN-FNet','組網-FirstTunnel-MPLSVPN-FNet'),('組網-SecondaryTunnel-MPLSVPN-FNet','組網-SecondaryTunnel-MPLSVPN-FNet'),('组网-Circuit-MPLSL2VPN','组网-Circuit-MPLSL2VPN'),('線路-MSTP','線路-MSTP'),('線路-SDH','線路-SDH'),('線路-IPLC','線路-IPLC'),('線路-IEPL','線路-IEPL'),('線路-DPLC ','線路-DPLC '),('線路-Internet','線路-Internet  '),('線路-HKMetro ','線路-HKMetro'),('線路-IPTransit','線路-IPTransit'),('FastNet','FastNet')]

class FromJituanID(forms.ModelForm):

        class Meta:
                model = JituanID
                widgets = {
                    'jtcreate_date': TextInput(attrs={'class':'vDateField'}),
                }

class FromCid(forms.ModelForm):
      
        class Meta:
                model = Cid
                widgets = {
                    'cidcreate_date': TextInput(attrs={'class':'vDateField'}),
                }

class FromSite(forms.ModelForm):
        class Meta:
                model = Site 
		exclude = ['oldcid']
                widgets = {
                    'sitecreate_date': TextInput(attrs={'class':'vDateField'}),
                    'siteid': Select(choices=SITEOPT),
                    'siteaddr': Textarea(),
                }
class FromLine(forms.ModelForm):
        class Meta:
                model = Line
                widgets = {
                    'linecreate_date': TextInput(attrs={'class':'vDateField'}),
                    'lineid': Select(choices=LINEOPT),
                    'lineserver': Select(choices=PE),
		    'pengpop': Select(choices=pengpop),
                    'linelocalinfo': Select(choices=linelocalinfo),
                    'lineaccesstype' : Select(choices=newlinetype),
                    'linejifangtype': Select(choices=LINEJIFATYPE),
                    'lineother' : Textarea(),
                    'linebaozhanginfo' : Textarea(),
                    'linemrtgserver' : Select(choices=MRTGSERVER),
                }

class FromService(forms.ModelForm):

        class Meta:
                model = Service
                widgets = {
                    'serviceid': Select(choices=SERVICEOPT),
                    'servicecreate_date': TextInput(attrs={'class':'vDateField'}),
                    'serviceother' : Textarea(),
                    'serviceshebei' : Textarea(),
                }

