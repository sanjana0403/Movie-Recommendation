import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp
import scipy.stats as st
from scipy.spatial import distance
from sklearn.metrics import mean_squared_error
from math import sqrt

actual_user = zeros((1000,131262)) ##### all test data matrix
test_user = zeros(131262) ##### 1D array storing 5 values of actual_user in iteration
test_movie = zeros(5) ##### Index or Id of 5 movies in test user
mov_vector = zeros(1128) ##### An array that has relevance tag of user ,combination of 5 movies
mtrx = zeros((131170,1128)) ##### movie matrix , movie X relevance
metric = zeros(131170) ##### array storing distance of mov_vector with all other movies then finally storing ratings
rating = zeros(131170) ####### ratings predicted 

mae = 0

with open('dataset/ratings.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue
		if int(row[0])>1000:
			break
		else:
			actual_user[int(row[0])-1][int(row[1])-1] = float(row[2])
print "users"
print actual_user
### matrix of movies

with open('dataset/genome-scores.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue
		if int(row[0])>131170:
			break
		mtrx[int(row[0])-1][int(row[1])-1] = float(row[2])
print "matrix"
print mtrx


for k in range(1000):
	print "user",k
	count = 0
	for j in range(131262):
		if(count>4):
			break
		elif(actual_user[k][j]!=0):
			test_user[j]=actual_user[k][j]
			test_movie[count]=j
			count=count+1
		else:
			continue


	sums = 0
	for i in range(5):
		#print "movie ",i+1
		#print mtrx[int(test_movie[i])]
		for j in range(1128):
			### adding (multiplication of rating and tag relevance)
			mov_vector[j]=mov_vector[j]+test_user[int(test_movie[i])]*mtrx[int(test_movie[i])][j]
		sums=sums+test_user[int(test_movie[i])]

	#print "mov_vector",mov_vector
	#print "sums",sums
	
	# normalising to get from 0 to 1
	for j in range(1128):
		mov_vector[j]=mov_vector[j]/sums

	#print "mov_vector",mov_vector

	### calculating distance of every movie from mov_vector 
	for i in range(131170):
		metric[i]=distance.cosine(mov_vector,mtrx[i])
		#print i, metric[i]

	#print "distance",metric

	### giving ratings to these movies
	for i in range(131170):
		if metric[i]<0.2:
			metric[i]=5
		elif metric[i]<0.25:
			metric[i]=4.5
		elif metric[i]<0.3:
			metric[i]=4
		elif metric[i]<0.35:
			metric[i]=3.5
		elif metric[i]<0.4:
			metric[i]=3
		elif metric[i]<0.45:
			metric[i]=2.5
		elif metric[i]<0.5:
			metric[i]=2
		elif metric[i]<0.6:
			metric[i]=1.5
		else:
			metric[i]=1
	#print "ratings",metric

	count=0
	sums=0
	for i in range(131170):
		if(actual_user[k][i]!=0):
			#print actual_user[k][i],metric[i]
			sums=sums+abs(actual_user[k][i]-metric[i])
			count=count+1

	print "mae for ",k," ",sums/count
	mae = mae + sums/count

print "Final MAE for cosine ",mae/1000
		