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
cursor.execute("SELECT MIN(time) FROM results WHERE age LIKE '%W%' GROUP BY runnerid;")
output = cursor.fetchall()
wresults = 5000 / np.array([output[i][0] for i in range(0,len(output))])
wresults = np.reshape(wresults, [1,len(wresults)])
cursor.execute("SELECT MIN(time) FROM results WHERE age LIKE '%M%' GROUP BY runnerid;")
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
est_fraction = (1/2) * (1 + tf.erf((c - mu)/(np.sqrt(2)*sigma)))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

percentile = 5
gender = mresults
gender = gender #fast or slow

#Isolate a tail based on percentile
cut = np.percentile(gender, percentile)
print("This percentile corresponds to", cut)
cut_values = gender[gender < cut]
cut_values = np.reshape(cut_values, [1,len(cut_values)])

#Fit normal distribution to the tail
for i in range(0,10000):
    sess.run([optimizer,cost], feed_dict = {X: cut_values, c: np.reshape(cut,[1,1])})
estimated_n = len(cut_values[0,])/sess.run(est_fraction, feed_dict = {c: np.reshape(cut,[1,1])})
final_cost = sess.run(cost, feed_dict = {X: cut_values, c: np.reshape(cut,[1,1])})
print("The best fit mu is", sess.run(mu)[0,0], "while mean of original is", np.mean(gender))
print("The best fit sigma is", sess.run(sigma)[0,0], "while stdev of original is", np.std(gender))
print("The estimated number in sample is", estimated_n, "while actual is", len(gender[0,]))
print("The final value of the cost function is", final_cost)

def generate_random(m, s, c):
    r = np.random.normal(m,s)
    while r > c:
        r = np.random.normal(m,s)
    return r

#goodness of fit
count = 0
m = sess.run(mu)[0,0]
s = sess.run(sigma)[0,0]
n = 1000
for i in range(0,n):
    r = np.reshape([generate_random(m,s,cut) for i in range(0,len(cut_values[0,]))], [1,len(cut_values[0,])])
    if sess.run(cost, feed_dict = {X: r, c: np.reshape(cut,[1,1])}) > final_cost:
        count = count + 1
print("The chance of cost this low occuring from genuine normally distributed sample is", count/n)


sess.close()

#Plot
pyplot.hist(gender[0,], density=True)
x = np.linspace(min(gender[0,]),max(gender[0,]))
y = (estimated_n / len(gender[0,])) * (1/(np.sqrt(2*np.pi)*s)) * np.exp(-0.5*((x - m)**2) / s**2)
y = np.reshape(y, [len(x)])
pyplot.plot(x,y)

pyplot.show()


#def goodness_of_fit_improved(cut, optimum, l, n, sess):
#    count = 0
#    m = sess.run(mu)[0,0]
#    s = sess.run(sigma)[0,0]
#    for i in range(0,n):
#        r = np.reshape([generate_random(m,s,cut) for i in range(0,l)], [1,l])
#        for i in range(0,100):
#            sess.run([optimizer,cost], feed_dict = {X: r, c: np.reshape(cut,[1,1])})

#        if sess.run(cost, feed_dict = {X: r, c: np.reshape(cut,[1,1])}) > optimum:
#            count = count + 1
#    sess.close()
#    return count / n






#sess.close()