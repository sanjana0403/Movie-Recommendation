import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp
import scipy.stats as st
from scipy.spatial import distance
from sklearn.metrics import mean_squared_error
from math import sqrt

actual_user = zeros(131262)
test_user = zeros(131262)
test_movie = zeros(5)
mov_vector = zeros(1128)
mtrx = zeros((131170,1128))
metric = zeros(131170)
with open('dataset/ratings.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue
		if int(row[0])>1:
			break
		else:
			actual_user[int(row[1])-1] = float(row[2])


count = 0
for j in range(len(actual_user)):
	if(count>4):
		break
	elif(actual_user[j]!=0):
		test_user[j]=actual_user[j]
		test_movie[count]=j
		count=count+1
	else:
		continue

#for j in range(200):
#	print actual_user[j],test_user[j]

#with open('/home/garima/Desktop/Project/matrix/content.csv') as readfile:
#	reader = csv.reader(readfile)
#	for i,row in enumerate(reader):
#		for j in range(1128):
#			mtrx[i][j]=float(row[j])

with open('dataset/genome-scores.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue
		if int(row[0])>131170:
			break
		mtrx[int(row[0])-1][int(row[1])-1] = float(row[2])


#print mtrx
sums = 0
for i in range(5):
	print "movie ",i+1
	print mtrx[int(test_movie[i])]
	for j in range(1128):
		mov_vector[j]=mov_vector[j]+test_user[int(test_movie[i])]*mtrx[int(test_movie[i])][j]
	sums=sums+test_user[int(test_movie[i])]

print mov_vector
print sums
for j in range(1128):
	mov_vector[j]=mov_vector[j]/sums

print mov_vector

### calculating distance of every movie from mov_vectpr 
for i in range(131170):
	metric[i]=st.spearmanr(mov_vector,mtrx[i])[0]
	#print i, metric[i]

print "distance"
print metric

### giving ratings to these movies
for i in range(131170):
	if metric[i]<0.55:
		metric[i]=5
	elif metric[i]<0.60:s
		metric[i]=4.5
	elif metric[i]<0.65:
		metric[i]=4
	elif metric[i]<0.70:
		metric[i]=3.5
	elif metric[i]<0.75:
		metric[i]=3
	elif metric[i]<0.80:
		metric[i]=2.5
	elif metric[i]<0.85:
		metric[i]=2
	elif metric[i]<0.9:
		metric[i]=1.5
	else:
		metric[i]=1s

print "ratings"
print metric

count=0
sums=0
for i in range(131170):
	if(actual_user[i]!=0):
		print actual_user[i],metric[i]
		sums=sums+abs(actual_user[i]-metric[i])
		count=count+1

print "mae",sums/count

	