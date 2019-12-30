# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 23:16:46 2018

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as pyplot

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

session = Session()

results = session.query(Result.pb, Result.time).filter(Result.pb != 0)

x = []
y = []

for a, b in results:
    x.append(5000/a)
    y.append(a/b)

pyplot.scatter(x, y, s=0.01)
pyplot.plot([1,6],[1.2,1.2],'r')
pyplot.plot([1,6],[0.85,0.85],'r')
pyplot.xlabel('PB speed when run happened')
pyplot.ylabel('Speed as a fraction of PB')


#results = session.query(Result.runid, Result.time)

#x = []
#y = []

#for i in range(200,405):
 #   runresults = results.filter(Result.runid == i)
  #  totaltime = 0
  #  counter = 0
  #  for a, b in runresults:
  #      totaltime = totaltime + b
  #      counter = counter + 1
  #  if counter != 0:
  #      x.append(i)
  #      y.append(totaltime/counter)

#pyplot.plot(x, y)
#pyplot.plot([252,252],[1550,1750],'r')
#pyplot.plot([304,304],[1550,1750],'r')
#pyplot.plot([356,356],[1550,1750],'r')
#pyplot.xlabel('Run number')
#pyplot.ylabel('Average time')