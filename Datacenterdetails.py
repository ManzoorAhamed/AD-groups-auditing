#!/usr/bin/python

#Purpose:Python script to extract INFO from "https://twiki.corp.inmobi.com/Infrastructure/DataCenterInventory"
#Date:04-08-2013
#Author:Manzoor

#IMPORTING MODULES
import urllib2
import MySQLdb
import sys , traceback
from bs4 import BeautifulSoup
import re
from itertools import ifilterfalse

#Creating a request to "https://twiki.corp.inmobi.com/Infrastructure/DataCenterInventory"
#host = raw_input("Enter the host name : ")
response = urllib2.urlopen('https://twiki.corp.inmobi.com/Infrastructure/DataCenterInventory').read().split("</tr>")
#response = open('file2','r').read().split("</tr>")

#DECLARING NECESSARY VARIABLES
content = ""
content1 = []
arg = []

#PARSING THE HTML PAGE TO GET THE TEXT AND STORED IT IN A LIST
for i in response:
        soup = BeautifulSoup(i)
        content = (soup.get_text())
#       content = re.sub('\n+',' ',soup.get_text())
        content = re.sub('\xa0+','NO',content)
#       content = re.sub(' +',' ',content)
        content1.append(content)
#print content1
content1 = filter(lambda name: name.strip(), content1)
#print content1

#SPLITING THE DETAILS AND PRINTING IT TO TERMINAL
db = MySQLdb.connect("localhost","root","mysql","TESTDB")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS DATACENTER")

sql = """CREATE TABLE DATACENTER ( ITAG CHAR(40), MACID CHAR(40), SERVERNAME CHAR(40), RACK CHAR(20), RACKU CHAR(20), SWITCHNAME CHAR(40), SWITCHPORT CHAR(40), CONSOLESERVER CHAR(40), CONSOLEPORT CHAR(40), IPMIDRAC CHAR(40), PDUHOSTNAME1 CHAR(40), PDU1PORT CHAR(40), PDUHOSTNAME2 CHAR(40), PDU2PORT CHAR(40), PDUHOSTNAME3 CHAR(40), PDU3PORT CHAR(40), PDUHOSTNAME4 CHAR(40), PDU4PORT CHAR(40), OWNER CHAR(20), PROJECT CHAR(40), BUG CHAR(20) )"""
cursor.execute(sql)
for i in content1:
        arg = i.split("\n")
#	print arg
	arg = map(lambda a:a.strip(),arg)
#	print arg
        sql1 = """ INSERT INTO DATACENTER ( ITAG, MACID, SERVERNAME, RACK, RACKU, SWITCHNAME, SWITCHPORT, CONSOLESERVER, CONSOLEPORT, IPMIDRAC, PDUHOSTNAME1, PDU1PORT,         PDUHOSTNAME2, PDU2PORT, PDUHOSTNAME3, PDU3PORT, PDUHOSTNAME4, PDU4PORT, OWNER, PROJECT, BUG ) 
        VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" %(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7        ],arg[8],arg[9],arg[10],arg[11],arg[12],arg[13],arg[14],arg[15],arg[16],arg[17],arg[18],arg[19],arg[20],arg[21],arg[22] )
        try:
         cursor.execute(sql1)
         db.commit()
#         print "sucess"
        except:
         db.rollback()
         traceback.print_exc()
 

db.close()
