# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 23:14:16 2019

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np
import matplotlib.pyplot as pyplot

minrunnumber = 250
maxrunnumber = 450

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

results = session.query(Result).filter(Result.pb != 0)

pbpercentages = []
runnumbers = [i for i in range(minrunnumber, maxrunnumber + 1)]

for runnumber in runnumbers:
    
    runresults = results.filter(Result.runid == runnumber)
    
    counter = 0
    pbcounter = 0
    for result in runresults:
        if result.time < result.pb:
            pbcounter = pbcounter + 1
        counter = counter + 1

    if counter != 0:
        pbpercentages.append(pbcounter / counter)
    else:
        pbpercentages.append(pbpercentages[-1])

pyplot.figure(1)
pyplot.plot(runnumbers, pbpercentages)

datatbft = pbpercentages
aic = np.zeros(int(len(datatbft)/2)+1)
testperiods = [i for i in range(0,len(aic))]
yearfit = []
for testperiod in testperiods[2:]:
    count = int(len(datatbft)/testperiod)
    fit = np.zeros(testperiod)
    for i in range(0,testperiod):
        for j in range(0,count):
            fit[i] = fit[i] + datatbft[i + j * testperiod]
        fit[i] = fit[i]/(count)
    if testperiod == 52: yearfit = fit
    fullfit = np.array([fit[i % testperiod] for i in range(0,len(datatbft))])
    rss = np.sum((datatbft - fullfit)**2)
    aic[testperiod] = 2*testperiod + len(datatbft) * np.log(rss)
    aic[testperiod] = aic[testperiod] + (2*(testperiod**2) + 2*testperiod) / (len(datatbft) - testperiod - 1)
  

pyplot.figure(2)
pyplot.plot(testperiods[2:], aic[2:])
pyplot.plot([52, 52], [-200,-400],'r')
pyplot.xlabel('Period')
pyplot.ylabel('Test statistic')
pyplot.title('Periodicity of conditions measurement\nRed = 52')