# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 20:11:13 2019

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np
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

results = session.query(Result).filter(Result.pb != 0)#.filter(Result.age.like('VM7%'))

pbs = 0
expbs = 0
varpbs = 0

for result in results:
    p = 1/(result.experience + 1)
    expbs = expbs + p
    varpbs = varpbs + p * (1-p)
    if result.time < result.pb:
        pbs = pbs + 1

print(pbs, expbs, np.sqrt(varpbs))


runners = session.query(Result).filter(Result.pb == 0)#.filter(Result.age.like('VM7%'))

"""
streaks = []

for runner in runners:
    runnerresults = results.filter(Result.runnerid == runner.runnerid).order_by(Result.runid)
    currentstreak = 0
    longeststreak = 0
    for runnerresult in runnerresults:
        if runnerresult.time >= runnerresult.pb:
            currentstreak = currentstreak + 1
        else:
            if longeststreak < currentstreak:
                longeststreak = currentstreak
            currentstreak = 0
    if longeststreak < currentstreak:
        longeststreak = currentstreak
    streaks.append(longeststreak)
"""

normpbs = []

for runner in runners:
    runnerresults = results.filter(Result.runnerid == runner.runnerid)
    total = 0
    pbsr = 0
    expbsr = 0
    varpbsr = 0
    for runnerresult in runnerresults:
        p = 1/(runnerresult.experience + 1)
        expbsr = expbsr + p
        varpbsr = varpbsr + p * (1-p)
        total = total + 1
        if runnerresult.time < runnerresult.pb:
            pbsr = pbsr + 1
    if total >= 10:
        normpbs.append((pbsr - expbsr) / np.sqrt(varpbsr))
    
pyplot.hist(normpbs, bins=20)