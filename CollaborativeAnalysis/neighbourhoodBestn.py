import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp
import scipy.stats as st
import sklearn.metrics as skm

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



countcos = 0
counteuc = 0
netAvgErrors = []
############ new user ###########################
neighbourSize = 1
while neighbourSize <= 50:
	# print 'neighbour', neighbourSize
	error = zeros((testUsers, neighbourSize))
	avgErrors = []
	totsum = 0
	totcount = 0
	for j in range(len(testmtrx)):
		print neighbourSize, j
		# if j==10:
		# 	break
		user = zeros(131262)
		count = 0
		for i in range(len(user)):
			if(testmtrx[j][i]!=0):
				if count==5:
					break
				count +=1
				user[i] = testmtrx[j][i]

		################################################################################################

		############ NEIGHBOURHOOD SELECTION ##########################################################

		pearson = zeros(trainUsers)

		for row in range(len(mtrx)):
			pearson[row] = st.pearsonr(user, mtrx[row])[0]
			# pearson[row][1] = st.pearsonr(user, mtrx[row])[1]

		# 2. BEST N CORRELATES ################

		indexpearson = argpartition(pearson,-neighbourSize) 

		similarpear = indexpearson[-neighbourSize:]

		print similarpear

		# for k in range(len(similarpear)):
		# 	error[j][k]=skm.mean_absolute_error(testmtrx[j],mtrx[similarpear[k]])

		count = 0
		sums = 0
		for i in range(len(testmtrx[j])):
			if (testmtrx[j][i]!=0) and (mtrx[similarpear[0]][i]!=0):
				#print "in if"
				count = count+1
				sums = sums+abs(testmtrx[j][i]-mtrx[similarpear[0]][i])
				# print sums	
		
		if count!=0:
			totsum = totsum+(sums/count)
			totcount = totcount+1
		
	avgErrors.append(float(totsum/testUsers))	
	neighbourSize += 1

graphmtrx = zeros((50,2))
for i in range(len(avgErrors)):
	graphmtrx[i][0] = i+1
	graphmtrx[i][1] = avgErrors[i]

print graphmtrx

numpy.savetxt("home/sanjana/Documents/movieRecomm/MovieRecommendation/neighbour_best_n.csv", graphmtrx, delimiter=",")