# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:56:06 2018

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as pyplot
from sklearn import linear_model
from sklearn.metrics import r2_score
import pickle

minnumber = 250
maxnumber = 440

in1 = open("runconditions2.pkl", 'rb')
runconditions = pickle.load(in1)

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

results = session.query(Result).filter(Result.runid >= minnumber).filter(Result.runid <= maxnumber)

x = []
xdata = []
y = []

for runnumber in range(minnumber,maxnumber+1):
    runresults = results.filter(Result.runid == runnumber).order_by(Result.time)
    if runresults.count() != 0:
        y.append(runresults.count())
        x.append(runconditions[runnumber])
        xdata.append([x[-1]])

pyplot.scatter(xdata,y)

model = linear_model.LinearRegression()
model.fit(xdata,y)
ypred = model.predict(xdata)
print("Coefficient: ", model.coef_)
print("Intercept: ", model.intercept_)
print("R^2: ", r2_score(y, ypred))

pyplot.plot(x,ypred,'r')