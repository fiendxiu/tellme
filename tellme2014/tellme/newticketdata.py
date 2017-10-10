import MySQLdb
import datetime
import HTMLParser

def newtickets(siteid):
    try:
        conn=MySQLdb.connect(host='192.168.55.117',user='root',passwd='both-win',db='ticket',charset='utf8',port=3306,connect_timeout=10)
        cur=conn.cursor()
        result=cur.execute("select ticket_id,title,body,created from ost_ticket_thread where title like '%%%s%%' order by created desc limit 5"% siteid)
        index=0
        rows=cur.fetchall()
        if not rows:
            return
        for row in rows:
            index+=1
        newticket_id=[0]*index
        newticket   =[([0]*6) for i in range(index)]
        index=0
        for row in rows:
            startpoint = row[1].find('[')
            endpoint = len(row[1])
            newticket_id[index]  =row[0]
            newticket[index][1]  =row[1][startpoint:endpoint]
            h = HTMLParser.HTMLParser()
            body = h.unescape(row[2])
            substr = body.split('<br />')
            newticket[index][2] = substr[4]
            newticket[index][3] = datetime.datetime.strftime(row[3],'%b-%d-%Y')
            try:
                newticket[index][4] = substr[7]
            except:
                newticket[index][4] = "Nothing"
            index+=1

        i=0
        while i < index:
            result2 = cur.execute("SELECT number FROM ost_ticket where ticket_id = '%s'",newticket_id[i])
            row2=cur.fetchone()
            newticket[i][0]  =row2[0]
            i+=1

        cur.close()
        conn.close()
        
        return(newticket)
    except:
        return(newticket)
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
