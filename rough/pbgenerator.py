# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 20:41:17 2018

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

runtoupdate = 456

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

results = session.query(Result).order_by(Result.runid)

resultstoupdate = results.filter(Result.runid == runtoupdate)

for result in resultstoupdate:
    if result.pb == 0:
        runnerresults = results.filter(Result.runnerid == result.runnerid).order_by(Result.runid)
        runnerpb = runnerresults[0].time
        for runnerresult in runnerresults[1:]:
            runnerresult.pb = runnerpb
            if runnerresult.time < runnerpb:
                runnerpb = runnerresult.time

session.commit()        

