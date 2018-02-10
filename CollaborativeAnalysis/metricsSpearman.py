import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp
import scipy.stats as st
import scipy.sparse as ss
from scipy.spatial import distance
import sklearn.metrics as metrics

trainUsers = 800
testUsers = 200
mtrx = zeros((trainUsers,131262))

with open('dataset/RatingsTrainMatrix.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		for j in range(trainUsers):
			mtrx[j][i]=float(row[j])

testmtrx = zeros((testUsers, 131262)) #userXmovies

with open('dataset/RatingsTestMatrix.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		for j in range(testUsers):
			testmtrx[j][i]=float(row[j])


############ new user ###########################
totsum = 0
totcount = 0
for j in range(len(testmtrx)):
	user = zeros(131262)
	count = 0
	for i in range(len(user)):
		if(testmtrx[j][i]!=0):
			if count==5:
				break
			count +=1
			user[i] = testmtrx[j][i]

	spearmanSim = zeros(trainUsers)

	for row in range(len(mtrx)):
		spearmanSim[row] = st.spearmanr(user, mtrx[row])[0]

	indexSpearman = argpartition(spearmanSim,1) 
	similarSpearman = indexSpearman[:1]

	count = 0
	sums = 0
	for i in range(len(testmtrx[j])):
		if (testmtrx[j][i]!=0) and (mtrx[similarSpearman[0]][i]!=0):
			#print "in if"
			count = count+1
			sums = sums+abs(testmtrx[j][i]-mtrx[similarSpearman[0]][i])
			# print sums	
	
	if count!=0:
		totsum = totsum+(sums/count)
		# print sums/count
		totcount = totcount+1

		# print totsum, totcount
	
ans = totsum/testUsers
print "Average ",ans
