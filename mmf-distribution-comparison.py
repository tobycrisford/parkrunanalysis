# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:22:28 2020

@author: Toby
"""

import sqlite3 as sql
import matplotlib.pyplot as pyplot
import numpy as np

#Load male and female PBs
connection = sql.connect("cambridgedata.db")
cursor = connection.cursor()
cursor.execute("SELECT MIN(time) FROM results WHERE age LIKE '%W%' GROUP BY runnerid;")
output = cursor.fetchall()
wresults = 5000 / np.array([output[i][0] for i in range(0,len(output))])
cursor.execute("SELECT MIN(time) FROM results WHERE age LIKE '%M%' GROUP BY runnerid;")
output = cursor.fetchall()
mresults = 5000 / np.array([output[i][0] for i in range(0,len(output))])
connection.close()

#pyplot.boxplot(mresults)
#pyplot.boxplot(wresults)
fig, ax = pyplot.subplots()
ax.boxplot([mresults,wresults])
pyplot.show()

mresults_norm = (mresults - np.mean(mresults)) / np.std(mresults)
wresults_norm = (wresults - np.mean(wresults)) / np.std(wresults)

pyplot.hist(wresults_norm, bins=30, density=True, label="W")
pyplot.hist(mresults_norm, bins=30, density=True, label="M")
pyplot.legend()
pyplot.show()


percentile = 95
cutm = np.percentile(mresults, percentile)
cutw = np.percentile(wresults, percentile)
print("This percentile corresponds to", cutm, cutw)
cut_valuesm = mresults[mresults > cutm]
cut_valuesw = wresults[wresults > cutw]
mresults_norm2 = (mresults - np.mean(cut_valuesm)) / np.std(cut_valuesm)
wresults_norm2 = (wresults - np.mean(cut_valuesw)) / np.std(cut_valuesw)

pyplot.hist(wresults_norm2, bins=30, density=True, label="W")
pyplot.hist(mresults_norm2, bins=30, density=True, label="M")
pyplot.legend()
pyplot.show()