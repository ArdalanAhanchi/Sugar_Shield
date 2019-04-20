#Ardalan Ahanchi
#Machine Learning

#Filter out the warnings from the terminal output.
import warnings
warnings.filterwarnings("ignore")

import sys
import pandas as pd
import numpy as np
import flask
from flask import request, jsonify
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.decomposition import PCA

trained_model = None

#Setup flask.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

	#Run the PCA feature reduction on data.
	pca = PCA(.95)
	pca.fit(trainingX)
	trainingX = pca.transform(trainingX)
	testingX = pca.transform(testingX)

	#Train and print statistics for the SVC classifier.
	trained_model = SVC(random_state=0, decision_function_shape='ovo')

	trained_model.fit(trainingX, trainingY)
	prediction = trained_model.predict(testingX)
	print("Type is", type(testingX))
	printStats(testingY, prediction, "Support Vector Classifier")

#Called when a 404 error occures.
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"Error" : "Page Not Found."}), 404

#Called when the user requested a prediction.
@app.route('/predictdiabetes', methods=['POST'])
def predict_diabetes():
	data = request.get_json(force=True)

	predict_list = [data["Pregnancies"], data["Glucose"], data["BloodPressure"]\
					data["SkinThickness"], data["Insulin"], data["BMI"], data["Pedigree"], data["Age"]]

	prediction = trained_model.predict(np.array(predict_list))
	print(prediction)

	return jsonify({"Prediction" : "Positive"}), 200


	#return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"



if __name__ == "__main__":
	train_svg()
	app.run()
