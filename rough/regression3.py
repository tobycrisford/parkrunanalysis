# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 20:38:08 2018

@author: Toby
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as pyplot
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pickle

maxrunnumber = 456

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

results = session.query(Result).filter(Result.pb != 0).filter(Result.runid >= 250)

x = []
xdata = []
y = []

for result in results:
    if result.pb / result.time > 0.9 and result.pb / result.time < 1.2:
        x.append(5000/result.pb)
        xdata.append([5000/result.pb, result.experience/10, (5000/result.pb)*(result.experience/10),(result.experience/10)**2])
        y.append(5000/result.time)

pyplot.figure(1)
pyplot.scatter(x, y, s = 0.01)
pyplot.xlabel('PB speed when run happened')
pyplot.ylabel('Speed')
pyplot.title("Data for runs >250 when speed is between 90% and 120% of PB")

model = linear_model.LinearRegression()

model.fit(xdata, y)
ypred = model.predict(xdata)

pyplot.plot(x, ypred, 'r')
print("Coefficient: ", model.coef_)
print("Intercept: ", model.intercept_)
print("R^2: ", r2_score(y, ypred))
mse = mean_squared_error(y, ypred)
print("MSE: ", mse)
pyplot.text(3.5, 2, "Coefficient: " + str(model.coef_) + "\nIntercept: " + str(model.intercept_) + "\nR^2: " + str(r2_score(y, ypred)) + "\nMSE: " + str(mse))



rnumbers = []
error = []
prederror = []
numberofrunners = []

for runnumber in range(200,maxrunnumber+1):

    runresults = results.filter(Result.runid == runnumber)
    
    x = []
    y = []
    
    for result in runresults:
        if result.pb / result.time > 0.9 and result.pb / result.time < 1.2:
            x.append([5000/result.pb, result.experience/10, (5000/result.pb)*(result.experience/10),(result.experience/10)**2])
            y.append(5000/result.time)
            
    if len(x) != 0:
    
        ypred = model.predict(x)
        
        yn = np.array(y)
        ypredn = np.array(ypred)
        
        error.append(np.sum(ypredn - yn)/len(y))
        prederror.append(np.sqrt(mse) / np.sqrt(len(y)))
        rnumbers.append(runnumber)
        numberofrunners.append(len(y))
        


pyplot.figure(2)
pyplot.plot(rnumbers, np.array(error)/np.array(prederror))
pyplot.xlabel('Run number')
pyplot.ylabel('Error (multiples of std dev under independence assumption)')
pyplot.title("Error in prediction of average speed \n To be used as measurement of conditions")

pyplot.figure(3)
pyplot.plot(rnumbers, np.array(error))
pyplot.xlabel('Run number')
pyplot.ylabel('Error')
pyplot.title("Error in prediction of average speed \n To be used as measurement of conditions")


pyplot.figure(4)
datatbft = error[0:111] + [(1/2)*(error[110]+error[111])] + error[111:162] + [(1/2)*(error[161]+error[162])] + error[162:]

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
  

pyplot.plot(testperiods[2:], aic[2:])
pyplot.plot([52, 52], [-200,-400],'r')
pyplot.xlabel('Period')
pyplot.ylabel('Test statistic')
pyplot.title('Periodicity of conditions measurement\nRed = 52')

runconditions = np.zeros(1000)
es = np.zeros(1000)

for i in range(0, len(rnumbers)):
    runconditions[rnumbers[i]] = error[i]
    es[rnumbers[i]] = prederror[i]
    

x = []
y = []

for result in results:
    if result.pb / result.time > 0.9 and result.pb / result.time < 1.2:
        x.append([5000/result.pb, result.experience/10, (5000/result.pb)*(result.experience/10),(result.experience/10)**2, 100 * runconditions[result.runid], (5000/result.pb)*(100 * runconditions[result.runid]), (5000/result.pb)**2])
        y.append(5000/result.time)

imp_model = linear_model.LinearRegression()

imp_model.fit(x, y)

ypred = imp_model.predict(x)
print("Coefficient: ", imp_model.coef_)
print("Intercept: ", imp_model.intercept_)
print("R^2: ", r2_score(y, ypred))
imp_mse = mean_squared_error(y, ypred)
print("MSE: ", imp_mse)




rnumbers = []
error = []
prederror = []
numberofrunners = []

for runnumber in range(200,maxrunnumber+1):

    runresults = results.filter(Result.runid == runnumber)
    
    x = []
    y = []
    
    for result in runresults:
        if result.pb / result.time > 0.9 and result.pb / result.time < 1.2:
            x.append([5000/result.pb, result.experience/10, (5000/result.pb)*(result.experience/10),(result.experience/10)**2, 100 * runconditions[result.runid], (5000/result.pb)*(100 * runconditions[result.runid]), (5000/result.pb)**2])
            y.append(5000/result.time)
            
    if len(x) != 0:
    
        ypred = imp_model.predict(x)
        
        yn = np.array(y)
        ypredn = np.array(ypred)
        
        error.append(np.sum(ypredn - yn)/len(y))
        prederror.append(np.sqrt(imp_mse) / np.sqrt(len(y)))
        rnumbers.append(runnumber)
        numberofrunners.append(len(y))
        


pyplot.figure(5)
pyplot.plot(rnumbers, np.array(error)/np.array(prederror))
pyplot.xlabel('Run number')
pyplot.ylabel('Error (multiples of std dev under independence assumption)')
pyplot.title("Error in prediction of average time")



out1 = open("model2.pkl", 'wb')
pickle.dump(model, out1)
out2 = open("imp_model2.pkl", 'wb')
pickle.dump(imp_model, out2)
out3 = open("mse2.pkl", 'wb')
pickle.dump(mse, out3)
out4 = open("runconditions2.pkl", 'wb')
rc = [100*runconditions[i] for i in range(0,len(runconditions))]
pickle.dump(rc, out4)
out5 = open("es2.pkl", 'wb')
esout = [100*es[i] for i in range(0, len(es))]
pickle.dump(esout, out5)

out1.close()
out2.close()
out3.close()
out4.close()
out5.close()

print(np.min(rc))