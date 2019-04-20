#Ardalan Ahanchi
#Machine Learning Prediction

PORT = 5000

#Filter out the warnings from the terminal output.
import warnings
warnings.filterwarnings("ignore")

import sys
import pandas as pd
import numpy as np
import flask
from flask import request, jsonify
from flask_cors import CORS
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.decomposition import PCA

#Setup flask.
app = flask.Flask(__name__)
CORS(app)
#app.config["DEBUG"] = True
app.trained_model = None

#Prints the model statistics and extra information
def printStats(Actual, Predicted, NameToPrint):
	print(NameToPrint," *******************************", "\n")
	print("Confusion Matrix: ")
	print(confusion_matrix(Actual,Predicted), "\n")
	print("Classification Report: ")
	print(classification_report(Actual,Predicted))
	print("Accuracy: ", accuracy_score(Actual,Predicted), "\n")

#Main method which loads the data and trains the model.
def train_svg():

	#Get the passed file name as the argument. (Default = Database.csv)
	fileName = "Database.csv.pp"
	if(len(sys.argv)) == 2:
		fileName = sys.argv[1]

	print("Learning Algorithm Started.")

	#Load the data from the "Preprocessed.csv file."
	matrix = pd.read_csv(fileName, header=0, sep=",")
	allX, allY = matrix.iloc[:,:-1], matrix.iloc[:, -1]
	trainingX, testingX, trainingY, testingY = train_test_split(allX, allY, test_size=0.15, random_state=1)

	trainingY = trainingY.astype("str")
	testingY = testingY.astype("str")

	#Train and print statistics for the SVC classifier.
	app.trained_model = SVC(random_state=0, decision_function_shape='ovo')

	app.trained_model.fit(trainingX, trainingY)
	prediction = app.trained_model.predict(testingX)
	print(type(testingX))

	printStats(testingY, prediction, "Support Vector Classifier")

#Called when a 404 error occures.
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"Error" : "Page Not Found."}), 404

#Called when the user requested a prediction.
@app.route('/predictdiabetes', methods=['POST'])
def predict_diabetes():
	data = request.get_json()

	try:
		#Recieve the json object.
		predict_list = [[]]
		predict_list[0].append(data["Pregnancies"])
		predict_list[0].append(data["Glucose"])
		predict_list[0].append(data["BloodPressure"])
		predict_list[0].append(data["SkinThickness"])
		predict_list[0].append(data["Insulin"])
		predict_list[0].append(data["BMI"])
		predict_list[0].append(data["Pedigree"])
		predict_list[0].append(data["Age"])
	except:
		#If invalid object, just return a 400 bad error.
		print("Error: Invalid Json Object.")
		return jsonify({"Error" : "Invalid Json Object."}), 400

	#Compare the value against the machine learning model.
	prediction = app.trained_model.predict(predict_list)

	#Check the result and return proper json file and error code.
	if prediction[0] == '0':
		return jsonify({"Prediction" : "Positive"}), 200
	elif prediction[0] == '1':
		return jsonify({"Prediction" : "Negative"}), 200
	else:
		return jsonify({"Error" : "Unknown Error Occured."}), 400

if __name__ == "__main__":
	train_svg()
	app.run(port=PORT)
