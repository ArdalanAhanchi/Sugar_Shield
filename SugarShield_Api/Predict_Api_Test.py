import requests
import json

PORT = 5000
URL = "http://127.0.0.1:"

try:                                                                            #Create a json file for the server.
    body = {}
    body["Pregnancies"] = str("2")
    body["Glucose"] = str("250")
    body["BloodPressure"] = str("62")
    body["SkinThickness"] = str("35")
    body["Insulin"] = str("0")
    body["BMI"] = str("33.6")
    body["Pedigree"] = str("0.127")
    body["Age"] = str("47")

except:
    print("Invalid values, please try again.")

headerJson = {'Content-type': 'application/json'}                               #Send a post request and add the character.
response = requests.post(URL + str(PORT) + "/predictdiabetes" , data=json.dumps(body), headers=headerJson)
