#!/usr/bin/env python

import urllib2
import sys
import json
from bs4 import BeautifulSoup, NavigableString
import re
import csv
import datetime
import os
import psycopg2 as dbapi2

"""db = psycopg2.connect (database="test", user="postgres", password="postgres")
cur = db.cursor()
cur.execute("CREATE TABLE craigslist (postid varchar,city varchar,area varchar,profession varchar,title varchar,postedtime varchar,updatedtime varchar,compensation varchar,url varchar,description varchar)")
"""
duplicates = []
latestDictionary = {}

def get_latest():
    #get date 
    for i in range(14):
        day = datetime.timedelta(days=i)
        today = datetime.date.today()
        prevday = str(today-day).replace("-", "_")
        #filename = city+"/"+city+"_"+str(today).replace("-", "_")+".csv"
        filename = "data/jobs/"+city+"/"+city+"_"+prevday+".csv"
        print filename
        if os.path.exists(filename):
            print "Exists: "+filename
            lastfile = open(filename,"r")
            lastfilereader = csv.reader(lastfile)
            header = next(lastfilereader)
            for row in lastfilereader:
                print row
                latest = row[4]
                print latest, "latest"
                lastfile.close()
                return [filename,latest]
    return "long"
    #yesterday
    #open file for yesterday
    #read first entry
    #get date and save as latest


#keywords = ["!","!!", "!!!","!!!!","experienced","diverse","innovative","verbal","amazing", "creative","enthusiastic","energy","organized","independently", "detail oriented", "entry level", "team player", "fast paced", "drug test", "friendly", "flexible","passion", "passionate", "estabilished","weekends","weekend", "unique", "energetic", "technology"]
def download_craigslist(page_count = 1, limit = 5):
    data = []
    duplicateCount = 0
    uniqueCount = 0

    for i in range(page_count):
        link = 'http://'+city+'.craigslist.org/jjj/index' + str(i*100) + '.html'
        soup = BeautifulSoup(urllib2.urlopen(link).read())
        x =  soup.body.article.find("div",class_="content")
        title = []
        time = []
        art = []
        
        for tag in x.find_all('p'):
            k=0
            for ah in tag.find_all('a'):
                if k%2 ==1:
                    art.append(ah['href'])
                k+=1

        #save first=latest for each city
        
        for l in art:
            
            base = "http://"+city+".craigslist.org"
            sidesoup = BeautifulSoup(urllib2.urlopen(base+l).read())
            
            if len(sidesoup.findAll(class_="bigattr"))>0:
                compensation = str(sidesoup.findAll(class_="bigattr")[0].text.encode("utf8").split(":")[1])
            else:
                compensation = "NA"
            #description = str(sidesoup.findAll("section",id="postingbody")[0].text.encode("utf8"))
            area = str(l.split("/")[1])
            profession = str(l.split("/")[2])
            if(sidesoup.body):
                #print sidesoup.body
                if (sidesoup.body.article):
                  # print sidesoup.body.article
                    if(sidesoup.body.article.section):
                     #   print sidesoup.body.article.section
                        
                        postinginfo = str(sidesoup.find(class_="postinginfos").text.encode('utf-8',errors='ignore'))
                        """if ("post id:" in postinginfo):
                            indexofpostid=postinginfo.index("post id:")
                            postid=postinginfo[indexofpostid+9:indexofpostid+19]
                        """
                        if(sidesoup.body.article.section.section):
                            postedtime = str(sidesoup.body.article.section.section.p.time.string)
                        if "updated:" in postinginfo:
                            indexofupdated=postinginfo.index("updated:")
                            updatedtime=postinginfo[indexofupdated+9:indexofupdated+27]
                        else:
                            updatedtime=postedtime
                        if str(latest[1]) == str(updatedtime):
                            print "end of new entries"
                            return  
                        url = base+l
                        title = str(sidesoup.body.article.section.h2.text[4:-1].encode("utf8"))
                        description = str(sidesoup.findAll("section",id="postingbody")[0].text.encode('utf-8',errors='ignore')).lower().strip('\n')
                        outputArray = [area, profession, title, postedtime, updatedtime, compensation, url, description]
                        #outputArray = [postid, city, area, profession, title, postedtime, updatedtime, compensation, url, description]
                        print outputArray
                        #alreadydownloaded = downloaded.readlines()
                        #print columnsChecked
                        """delineatedOutput = []
                        totalString=""
                        for output in outputArray:
                            if "\'" in output:
                                indexofsingleq=output.index("\'")
                                output=output[:indexofsingleq]+output[indexofsingleq+1:]
                            if output!=outputArray[-1]:
                                delineatedOutput.append("\'"+str(output)+"\'"+",")
                            else:
                                delineatedOutput.append("\'"+str(output)+"\'")
                        if not (cur.execute("SELECT * FROM craigslist where postid=\'"+str(postid)+"\'")):
                            for output in delineatedOutput:
                                totalString+=output
                            print totalString
                            cur.execute("INSERT into craigslist VALUES ("+totalString+") ")
                        """
                        alreadydownloaded =[]
                        if l in alreadydownloaded:
                            duplicateCount+=1
                            print "duplicate timestamp", duplicateCount
            #                    print "duplicate", [area, profession, title, time, url]
                        else:
                            if title in titles:
                                print "dup title"
                            uniqueCount+=1
                            print "unique count", uniqueCount
                            alreadydownloaded.append(l)
                            #print outputArray
                            #print [area, profession, title, time, url]
                            spamwriter.writerow(outputArray)
                        if limit > 0 and len(data) >= limit:
                            return data
        #return data
"""
cities=['boston']
for city in cities:
    download_craigslist()
cur.execute("SELECT * from craigslist")
rows = cur.fetchall()
for i, row in enumerate(rows):
    print "Row", i, "value = ", row
"""

timestamped_filename = str(datetime.datetime.now().date()).replace("-", "_")
#print timestamped_filename
currentdate = datetime.datetime.now().date()
#print currentdate
#cities = ["newyork","boston","atlanta", "austin", "sanantonio","boulder","chicago","santafe","cincinnati","cleveland","philadelphia","saltlakecity","pittsburgh","portland","honolulu","sacramento","detroit","columbus","losangeles", "miami", "seattle", "phoenix", "houston", "dallas", "washingtondc"]

#cities = ["sanantonio","boulder","chicago","santafe","cincinnati","cleveland","philadelphia","saltlakecity","pittsburgh","portland","honolulu","sacramento","detroit","columbus","losangeles", "miami", "seattle", "phoenix", "houston", "dallas", "washingtondc"]

#cities = ["chicago","santafe","cincinnati","cleveland","philadelphia","saltlakecity","pittsburgh","portland","honolulu","sacramento","detroit",
#cities = ["columbus","losangeles", "miami", "seattle", 
#cities = ["phoenix", "houston", "dallas", "washingtondc"]

cities = ["boston"]
for city in cities:
    latest = get_latest()
    print latest

    if not os.path.exists("data/jobs/"+city):
        os.makedirs("data/jobs/"+city)
    print city

    

    titles = []
    outputfile = open("data/jobs/"+city+"/new_"+city+"_"+timestamped_filename+".csv","wb")
    spamwriter = csv.writer(outputfile)
    spamwriter.writerow(["area", "profession", "title", "postedtime", "updatedtime", "compensation", "url","description"])
    download_craigslist(1, 5)
    outputfile.close()

    if latest=="long":
        finalfile = open("data/jobs/"+city+"/"+city+"_"+timestamped_filename+".csv","wb")
        outputfile = open("data/jobs/"+city+"/new_"+city+"_"+timestamped_filename+".csv","rb")
        spamreader=csv.reader(outputfile)
        spamwriter = csv.writer(finalfile)
        for row in spamreader:
            spamwriter.writerow(row)
        outputfile.close()
        finalfile.close()

    else:
        outputfile = open("data/jobs/"+city+"/new_"+city+"_"+timestamped_filename+".csv","rb")
        finalfile = open("data/jobs/"+city+"/final_"+city+"_"+timestamped_filename+".csv","wb")
        oldfile = open(latest[0],"rb")
        spamwriter2 = csv.writer(finalfile)
        spamreader = csv.reader(outputfile)
        spamreader2 = csv.reader(oldfile)
        for row in spamreader:
            spamwriter2.writerow(row)
        for row in spamreader2:
            if row!=['area', 'profession', 'title', 'postedtime', 'updatedtime', 'compensation', 'url', 'description']:
                spamwriter2.writerow(row)
        outputfile.close()
        finalfile.close()
        oldfile.close()

        newfile = open("data/jobs/"+city+"/"+city+"_"+timestamped_filename+".csv","wb")
        finalfile = open("data/jobs/"+city+"/final_"+city+"_"+timestamped_filename+".csv","rb")
        spamreader = csv.reader(finalfile)
        spamwriter = csv.writer(newfile)
        for row in spamreader:
            spamwriter.writerow(row)
        finalfile.close()
        newfile.close()

        if (latest[0]!="data/jobs/"+city+"/"+city+"_"+timestamped_filename+".csv"):
            os.remove(latest[0])
        os.remove("data/jobs/"+city+"/final_"+city+"_"+timestamped_filename+".csv")
    os.remove("data/jobs/"+city+"/new_"+city+"_"+timestamped_filename+".csv")
