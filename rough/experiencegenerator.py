# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:56:10 2018

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

results = session.query(Result)

resultstoupdate = results.filter(Result.runid == runtoupdate)

for result in resultstoupdate:
    result.experience = -1

session.commit()

for result in resultstoupdate:
    if result.experience == -1:
        runnerresults = results.filter(Result.runnerid == result.runnerid).order_by(Result.runid)
        counter = 0
        for runnerresult in runnerresults:
            runnerresult.experience = counter
            counter = counter + 1

session.commit()