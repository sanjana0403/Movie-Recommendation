import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp
import scipy.stats as st
import sklearn.metrics as skm

###############################################################
# thresholdArr contains minimum threshold to be set
# coverageArr
# mae contains mae between the test user and the expected user(from training set) which we are getting in the result
# avgErrors contain net mae for all the expected users for a given test user
# netAvgErrors contains mean of all the values in avgErrors ie net error for a given threshold value

# thresholdmtrx contain the threshold value and the corresponding mae

# user is the test user and contains ratings for 5 first ratings taken by our actual test user

# pearson contains pearson correlation between the test user and the each user from the training set
# similarpear contains all those users from training set whose pearson values comes out to be more than given threshold

# notnull contains count of all those threshold values for which some result is coming (to calculate coverage)
# coverageArr contains coverage for all the threshold values

##############################################################

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

thresholdArr = [0.1, 0.2, 0.3, 0.4, 0.5]
coverageArr = []
for threshold in thresholdArr:
	notNull = 0
	# if threshold == 0.2:
	# 	break
	# error = zeros((200, 10))
	avgErrors = []
	for j in range(len(testmtrx)):
		mae = []
		print "j", j
		# if j==1:
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

		similarpear = []
		count = 0
		for row in range(len(pearson)):
			# if count==10:
			# 	break
			if abs(pearson[row])>threshold:
				similarpear.append(row)
				count += 1

		print 'similarpear', similarpear
		if len(similarpear)>0:
			notNull += 1

		for k in range(len(similarpear)):
			mae.append(skm.mean_absolute_error(testmtrx[j],mtrx[similarpear[k]]))
		print 'mae', mae
		if len(mae)==0:
			meanval = 0
		else:
			meanval = numpy.mean(mae)
		avgErrors.append(meanval)	
	coverage = notNull*100/testUsers
	coverageArr.append(coverage)
	netAvgErrors.append(numpy.mean(avgErrors))

thresholdmtrx = zeros((5,2))
for i in range(len(netAvgErrors)):
	thresholdmtrx[i][0] = thresholdArr[i]
	thresholdmtrx[i][1] = netAvgErrors[i]

print thresholdmtrx
print coverageArr

numpy.savetxt("/MovieRecommendation/CollaborativeAnalysis/Results/neighbourhood_threshold.csv", thresholdmtrx, delimiter=",")