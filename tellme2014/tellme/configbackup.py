import urllib,urllib2,httplib,cookielib,time
from BeautifulSoup import BeautifulSoup

def get_page(opener,url,data={}):
    headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; "
                + ".NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; "
                + "InfoPath.2; .NET4.0E)"}
    postdata=urllib.urlencode(data)
    if postdata:
        request=urllib2.Request(url,postdata,headers=headers)
    else:
        request=urllib2.Request(url,headers=headers)
    f = opener.open(request)
    content = f.read()
    return content

def get_form_data(page):
    data = {}
    soup = BeautifulSoup(page)
    inputs = soup.find('form').findAll('input')
    for input in inputs:
        name = input.get('name')
        value = input.get('value')
        data[name] = value
    return data

def confadd(cid,host):
    try:
        cookiejar=cookielib.CookieJar()
        cj=urllib2.HTTPCookieProcessor(cookiejar)
        opener=urllib2.build_opener(cj)
        url_post = "http://192.168.55.250:10087/config/cgi/cid.cgi?__mode=add_cid&screen=edit_cid.html"
        auto_submit_page = get_page(opener,url_post)
        data = get_form_data(auto_submit_page)
        data['cid'] = cid
        data['host'] = host
        data['username'] = 'bothwin'
        data['password'] = 'Tfe28@w%'
        data['enable_pass'] = 'Tfe28@w%'
        data['active'] = 'on'
        data['wday'] = time.localtime().tm_wday
        data['hour'] = time.localtime().tm_hour
        data['type'] = 'FNETLINK'
        del data['cancel']
        del data['save']
        del data['en_copy']
        del data['en_check']
        headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; "
                    + ".NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; "
                    + "InfoPath.2; .NET4.0E)"}
        postdata=urllib.urlencode(data)
        postdata=postdata+'&save=%E4%BF%9D%E5%AD%98%E4%BF%AE%E6%94%B9'
        request=urllib2.Request(url_post,postdata,headers=headers)
        opener.open(request)
    except:
        return 0
