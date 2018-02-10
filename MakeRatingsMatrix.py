import sys
import csv
import numpy
from numpy import *
import scipy.spatial.distance as sp


mtrx = zeros((131262, 800)) #userXmovies
testmtrx = zeros((131262, 200))

with open('dataset/ratings.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue
		if int(row[0])==1001:
			break
		if int(row[0])>800:
			testmtrx[int(row[1])-1][int(row[0])-801] = float(row[2])
		else:			
			mtrx[int(row[1])-1][int(row[0])-1] = float(row[2])


numpy.savetxt("RatingsTrainMatrix.csv", mtrx, delimiter=",")
numpy.savetxt("RatingsTestMatrix.csv", testmtrx, delimiter=",")


