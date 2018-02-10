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
# testUsers = 200

mtrx = zeros((trainUsers,131262))

with open('dataset/RatingsTrainMatrix.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		for j in range(trainUsers):
			mtrx[j][i]=float(row[j])




############ new user ###########################
user = zeros(131262)



user[88139]=5.0 #captain america the first avenger
user[102124]=5.0 #iron man 3
user[59314]=4.5 #iron man
user[86331]=4.5 #thor
user[110101]=5 #captain america winter soldier

# user[88124]=5 
# user[355]=5
# user[4637]=3
# user[63991]=3
# user[64968]=4

# user[111359]=5 #lucy
# user[70158]=5 #orphan
# user[122281]=5 #pride and prejudice
# user[111920]=5 #fault in our stars
# user[6538]=5 #pirates

# user[67254]=4 #girl with dragon tattoo
# user[919]=5 #gone with the wind
# user[1720]=3 #titanic
# user[1034]=5 #sound of music
# user[130072]=5 #cinderella

# user[4895]=1 #sroceres stone
# user[5815]=2 #chamber of secrets
# user[8367]=1 #azkaban
# user[40814]=1 #goblet of fire
# user[54000]=1 #order of phoenix

# user[317]=3 #shawshank redemption
# user[1220]=3 #godfather 2
# user[109486]=3 #interstellar
# user[79131]=4 #inception
# user[112551]=5 #whiplash


cosineDist = zeros(trainUsers)

for row in range(len(mtrx)):
	cosineDist[row] = sp.cosine(user, mtrx[row])

# print cosineDist

index = argpartition(cosineDist, 4) ### sort till kth smallest element

similarUsers = index[:4]  ###first k elements of index
# similarUsers = numpy.flipud(similarUsers) ##reverse array
# print similarUsers

recomMovieArr = [[]]

for i in range(len(similarUsers)):
	row = []
	for j in range(len(mtrx[0])):
		if user[j]==0 and mtrx[similarUsers[i]][j] > 3:
			if j not in recomMovieArr:
				# print similarUsers[i], j, mtrx[similarUsers[i]][j]
				row.append(j)
	recomMovieArr.append(row)

# n = len(recomMovieArr[0])


# print len(recomMovieArr[0])
# print len(recomMovieArr[1])
# print len(recomMovieArr[2])
# print len(recomMovieArr[3])	 

finalMovies = []

# for i in range(4):
# 	for j in range(len(recomMovieArr[i])):
# 		if recomMovieArr[i][j] not in finalMovies:
# 			finalMovies.append(recomMovieArr[i][j])

for i in range(4):
	j = i+1
	while(j<4):
		arr = reduce(numpy.intersect1d, (recomMovieArr[i], recomMovieArr[j]))
		for k in range(len(arr)):
			if arr[k] not in finalMovies:
				finalMovies.append(arr[k])
		j = j+1	

# print finalMovies

if len(finalMovies)<5:
	while len(finalMovies)<5:
		for i in range(4):
			for j in range(len(recomMovieArr[i])):
				if recomMovieArr[i][j] not in finalMovies:
					finalMovies.append(recomMovieArr[i][j])

fmratings = zeros(len(finalMovies))

for i in range(len(finalMovies)):
	for j in similarUsers:
		# print finalMovies[i], j, mtrx[j][finalMovies[i]]
		fmratings[i] = max(fmratings[i], mtrx[j][finalMovies[i]])

# print fmratings

printMovies = []
index = argpartition(fmratings, -5)
index = numpy.flipud(index)
k = 0
while k<5:
	printMovies.append(finalMovies[index[k]])
	k = k+1

# print printMovies
movies = []

with open('dataset/movies.csv') as readfile:                          
	reader = csv.reader(readfile)
	for row in reader:
		movies.append(row)



for val in printMovies:
	for i in range(len(movies)):
		if movies[i][0] == "movieId":
			continue
		if val+1 == int(movies[i][0]):
			print movies[i][1]