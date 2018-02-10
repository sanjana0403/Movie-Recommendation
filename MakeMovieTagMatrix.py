import sys
import csv
import numpy
from numpy import *
# import scipy.spatial.distance as sp


mtrx = zeros((131170,1128)) #userXmovies

with open('dataset/genome-scores.csv') as readfile:                          
	reader = csv.reader(readfile)
	for i, row in enumerate(reader):
		if i==0:
			continue	
		mtrx[int(row[0])-1][int(row[1])-1] = float(row[2])
		# if row[0]>500:
		# 	break

numpy.savetxt("genomeMatrix.csv", mtrx, delimiter=",")

# mtrx = numpy.loadtxt(open("genomeMatrix.csv", "rb"), delimiter=",")

