#Ardalan Ahanchi
#UWB Hackathon Project

import sys
import warnings
import numpy as np
import scipy as sp
import sklearn as sk
from sklearn import preprocessing

#Saves the given matrix to the "Preprocessed.csv" file.
def save(matrix, fileName):
	fileName = fileName + ".pp"
	out = open(fileName,"w")
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if j == (len(matrix[0]) - 1):
				out.write(matrix[i][j])
				out.write("\n")
			else:
				out.write(matrix[i][j])
				out.write(",")

#Adds all the discrete values to a dictionary and assigns them numbers.
def fixDiscrete(matrix):
	#Add all the values to a dictionary and assign numeric values.
	for col in range(len(matrix[0])):
		if matrix[0][col] == "0":
			dictionary = {}
			index = 0
			for i in matrix[2:,col]:
				if i not in dictionary:
					dictionary[i] = index
					index += 1

			for j in range(2, len(matrix)):
				matrix[j][col] = dictionary[matrix[j][col]]
	return matrix

#Removes all the rows which contain the values marked with a "?"
def removeMissingRows(matrix):
	wasDeleted = False
	idx = 0;
	for i in matrix:
		for j in i:
			if j == "?":
				matrix = np.delete(matrix, idx, 0)
				wasDeleted = True
				break
		if wasDeleted :
			wasDeleted = False
		else:
			idx += 1
	return matrix

#Removes all the columns that are marked with a "2".
def removeMarkedCols(matrix):
	index = 0;
	for i in matrix[0]:
		if i == "2":
			matrix = np.delete(matrix, index, 1)
		else:
			index += 1
	return matrix

#Scales all the values in the matrix between [0,1]
def scale(matrix):
	warnings.filterwarnings("ignore")
	minMaxScaler = preprocessing.MinMaxScaler()
	return minMaxScaler.fit_transform(matrix[:][2:])

#Main function which pre-processes the data and saves it to the output file.
def main():
	#Get the passed file name as the argument. (Default = Database.csv)
	fileName = "Database.csv"
	if(len(sys.argv)) == 2:
		fileName = sys.argv[1]

	#Load the data into a two dimentional numpy array.
	matrix = np.loadtxt(open(fileName, "rb"), delimiter=",", dtype='str')

	#Remove the columns which are marked by a "2" identifier.
	#matrix = removeMarkedCols(matrix)

	#Remove the rows which contain the cells with the value of "?"
	#matrix = removeMissingRows(matrix)

	#Make the discrete data numeric for the columns marked as (0=discrete)
	#matrix = fixDiscrete(matrix)

	#Scale the values in the matrix between [0,1]
	matrix[:][2:] = scale(matrix)

	#Save the matrix to the output file.
	save(matrix[:][1:], fileName)

if __name__ == "__main__": main()
