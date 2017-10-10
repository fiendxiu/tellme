import MySQLdb
import datetime

def tickets(siteid):
    try:
        conn=MySQLdb.connect(host='192.168.55.173',user='tellme',passwd='both-win',db='ticket',charset='utf8',port=3306,connect_timeout=3)
        cur=conn.cursor()
        result=cur.execute("select * from ost_ticket where subject like '%%%s%%' order by created desc limit 5"% siteid)
        index=0
        rows=cur.fetchall()
        if not rows:
            return
        for row in rows:
            index+=1
        ticket_id=[0]*index
        ticket   =[([0]*6) for i in range(index)]
        index=0
        for row in rows:
            startpoint = row[8].find('[')
            endpoint = len(row[8])
            ticket_id[index]  =row[0]
            ticket[index][0]  =row[1]
            ticket[index][1]  =row[8][startpoint:endpoint]
            ticket[index][2]  =row[7]
            ticket[index][3]  =row[10]
            ticket[index][4]  =datetime.datetime.strftime(row[22],'%b-%d-%Y')
            index+=1

        i=0
        while i < index:
            result2 = cur.execute("SELECT * FROM ost_ticket_message where ticket_id = '%s'",ticket_id[i])
            row2=cur.fetchone()
            if not row2:
                return
            startpoint = row2[3].rfind('-*-')+3
            endpoint = len(row2[3])
            ticket[i][5]  =row2[3][startpoint:endpoint]
            i+=1

        cur.close()
        conn.close()
        
        return(ticket)
    except MySQLdb.Error,e:
        return
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
