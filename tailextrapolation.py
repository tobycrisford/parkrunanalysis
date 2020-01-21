# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 19:46:55 2020

@author: Toby
"""

#Estimates mean and variance of run-speeds based on tails

import sqlite3 as sql
import matplotlib.pyplot as pyplot
import tensorflow as tf
import numpy as np
learning_rate = 0.01

#Load male and female PBs
connection = sql.connect("cambridgedata.db")
cursor = connection.cursor()
cursor.execute("SELECT MIN(time) FROM results WHERE pb <> 0 AND age LIKE '%W%' GROUP BY runnerid;")
output = cursor.fetchall()
wresults = 5000 / np.array([output[i][0] for i in range(0,len(output))])
wresults = np.reshape(wresults, [1,len(wresults)])
cursor.execute("SELECT MIN(time) FROM results WHERE pb <> 0 AND age LIKE '%M%' GROUP BY runnerid;")
output = cursor.fetchall()
mresults = 5000 / np.array([output[i][0] for i in range(0,len(output))])
mresults = np.reshape(mresults, [1,len(mresults)])
connection.close()

#Set up cost function for MLE estimation of mean and variance
tf.reset_default_graph()
X = tf.placeholder(tf.float32, shape=[1,None])
c = tf.placeholder(tf.float32, shape=[1,None])
mu = tf.get_variable("mu", [1,1], initializer=tf.zeros_initializer())
sigma = tf.get_variable("sigma", [1,1], initializer=tf.ones_initializer())
cost = (1/2) * tf.reduce_sum(tf.square(X - mu)) * (1/tf.square(sigma)) + tf.to_float(tf.size(X)) * (tf.log(sigma) + tf.log((1 + tf.erf((c - mu) / (np.sqrt(2)*sigma)))))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

def solve(values, cutoff):
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    for i in range(0,10000):
        sess.run([optimizer,cost], feed_dict = {X: values, c: np.reshape(cutoff,[1,1])})
    r = [sess.run(mu),sess.run(sigma)]
    sess.close()
    return r

def solve_percentile(values, percentile):
    cut = np.percentile(values, percentile)
    cut_values = values[values < cut]
    cut_values = np.reshape(cut_values, [1,len(cut_values)])
    return solve(cut_values, cut)


wresults = -wresults
mresults = -mresults
#sess.close()