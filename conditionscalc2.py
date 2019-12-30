# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 22:53:23 2018

@author: Toby
"""

import pickle


runnumber = 456
comparison = 442
pbtime = 1017
actualtime = 1037

experience = 12 #actual value shouldn't matter

in1 = open("model2.pkl", 'rb')
model = pickle.load(in1)
in2 = open("imp_model2.pkl", 'rb')
imp_model = pickle.load(in2)
in3 = open("mse2.pkl", 'rb')
mse = pickle.load(in3)
in4 = open("runconditions2.pkl", 'rb')
runconditions = pickle.load(in4)
in5 = open("es2.pkl", 'rb')
es = pickle.load(in5)

in1.close()
in2.close()
in3.close()
in4.close()
in5.close()

print("Conditions: ", runconditions[runnumber])
print("Reference: ", runconditions[comparison])

worsta = runconditions[runnumber] + es[runnumber]
bestb = runconditions[comparison] - es[comparison]
besta = runconditions[runnumber] - es[runnumber]
worstb = runconditions[comparison] + es[comparison]

inputs = []

inputs.append([5000/pbtime, experience/10, (5000/pbtime)*(experience/10),(experience/10)**2, worsta, (5000/pbtime)*(worsta), (5000/pbtime)**2])
inputs.append([5000/pbtime, experience/10, (5000/pbtime)*(experience/10),(experience/10)**2, bestb, (5000/pbtime)*(bestb), (5000/pbtime)**2])
inputs.append([5000/pbtime, experience/10, (5000/pbtime)*(experience/10),(experience/10)**2, besta, (5000/pbtime)*besta, (5000/pbtime)**2])
inputs.append([5000/pbtime, experience/10, (5000/pbtime)*(experience/10),(experience/10)**2, worstb, (5000/pbtime)*worstb,(5000/pbtime)**2])

predictions = imp_model.predict(inputs)

maxspeedeffect = predictions[1] - predictions[0]
minspeedeffect = predictions[3] - predictions[2]

maxpred = 5000/((5000/actualtime) + maxspeedeffect)
minpred = 5000/((5000/actualtime) + minspeedeffect)

print("Max: ", maxpred)
print("Min:", minpred)