# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:27:32 2018

@author: Toby
"""

import requests
from pyquery import PyQuery as pq
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time as timer

def timereader(timetext):
    colon1 = timetext.find(":")
    colon2 = timetext[colon1+1:].find(":")
    colon2 = colon2 + colon1 + 1
    if colon2 == colon1:
        colon1 = -1
    seconds = int(timetext[colon2+1:])
    minutes = int(timetext[colon1+1:colon2])
    hours = 0
    if not colon1 == -1:
        hours = int(timetext[0:colon1])
    return 60 * 60 * hours + 60 * minutes + seconds

engine = create_engine(r"sqlite:///C:\Users\Toby\Dropbox\parkrun\cambridgedata.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'
    
    resultid = Column(Integer, primary_key=True)
    runid = Column(Integer)
    runnerid = Column(Integer)
    time = Column(Integer)
    pb = Column(Integer)
    position = Column(Integer)
    experience = Column(Integer)
    age = Column(String)
    gender = Column(String)
    
Base.metadata.create_all(engine)

example_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

session = Session()

for runnumber in range(454, 457):
    
    print(runnumber)
    
    timer.sleep(2)
    
    r = requests.get("http://www.parkrun.org.uk/cambridge/results/weeklyresults/?runSeqNumber=" + str(runnumber), headers=example_headers)
    
    d = pq(r.text)
    
    rows = d('table#results')('tr')[1:]
    
    results = []
    
    for row in rows:
        cols = d(row)('td')
        link = d(cols[1])('a')
        if link.length == 1:
            linkaddr = link.attr('href')
            runneridentry = linkaddr[linkaddr.find('=')+1:]
            
            timeentry = timereader(d(cols[2]).text())
            
            posentry = int(d(cols[0]).text())
            
            expentry = 0
            expentrystr = d(cols[9]).text()
            if not len(expentrystr) == 0:
                expentry = int(expentrystr)
            
            ageentry = d(cols[3]).text()
            
            genentry = d(cols[5]).text()
            
            results.append(Result(runid = runnumber, runnerid = int(runneridentry), time = timeentry, pb = 0, position = posentry, experience = expentry, age = ageentry, gender = genentry))
    
    
    for result in results:
        session.add(result)
    session.commit()
    
    
    
    
