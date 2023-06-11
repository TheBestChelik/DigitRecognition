from io import StringIO
import io
import json
import sqlite3
import sys
from flask import Flask, render_template, request, jsonify
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import base64
import re
import os
from AI.train import trainModel


from AI.digitRecogniser import Recognizer


def getModelNames(OnlyEditable = False):
    folders = []
    for item in os.listdir("models/"):
        item_path = os.path.join("models/", item)
        if os.path.isdir(item_path):
            folders.append(item)

    conn = sqlite3.connect('models/Database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    models = c.fetchall()
    EditableModels = []
    for model in models:
        if model[0] not in folders: 
            #deleting model from database if it is not present in list of models
            c.execute(f"DROP TABLE IF EXISTS {model[0]};")
        else:
            EditableModels.append(model[0])
    conn.close()
    if OnlyEditable:
        return EditableModels
    else:
        return folders
    

def CheckModelNameValidity(ModelName):
    #0 - OK
    #1 - name too short
    #2 - name already taken
    #3 - u cant use spaces in name
    #4 model name cant start with digit
    if " " in ModelName:
        return 3
    if ModelName and ModelName[0].isdigit():
        return 4
    if len(ModelName) < 3:
        return 1
    conn = sqlite3.connect('models/Database.db')
    cursor = conn.cursor()

    # Execute the SELECT statement to query the master table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (ModelName,))

    # Fetch the result
    result = cursor.fetchone()

    # Check if the table exists
    if result is not None:
        cursor.close()
        conn.close()
        return 2
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    return 0


def SaveImageToDatabase(tableName, digit, img):
    if img.shape!=(28,28):
        print("NOT SAVED, INCORRECT SHAPE")
        return
    conn = sqlite3.connect(f"models/Database.db")
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {tableName} (digit INTEGER, image BLOB)")
    img_bytes = img.tobytes()
    c.execute(f"INSERT INTO {tableName} (digit, image) VALUES (?, ?)", (digit, img_bytes))
    conn.commit()
    conn.close()


def GetImmagesFromDatabase(tableName):
    conn = sqlite3.connect(f"models/Database.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT digit, image FROM {tableName}")
    rows = cursor.fetchall()
    digits = []
    images = []
    for row in rows:
        digit = row[0]
        img_bytes = row[1]
        
        # Convert the byte string back to a NumPy array
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape((28, 28))


        images.append(img)
        digits.append(digit)

    conn.close()

    return images, digits

class R:
    def __init__(self) -> None:
        self.recognizer = Recognizer()
        self.currentModel = ""
        self.setModel(getModelNames()[0])

    def Recognise(self, image):
        return self.recognizer.Recognize(image)
    def setModel(self, modelName):
        if modelName!=self.currentModel:
            self.currentModel = modelName
            self.recognizer.SetModel(f"models\{modelName}")


    
r = R()
app = Flask(__name__,
            static_url_path='',
            static_folder='static')





@app.route('/')
def HomePage():
    return render_template("recognize.html")

@app.route('/home.html')
def Home():
    return render_template("home.html")

@app.route('/recognize.html')
def RecognizePage():
    return render_template("recognize.html")

@app.route('/train.html')
def TrainPage():
    return render_template("train.html")

@app.route("/train.html", methods = ["POST"])
def Training():
    data = request.get_json()
    if data['MessageType'] == "ModelName":
        result = CheckModelNameValidity(data['text'])
        response_data = {
            'result': 'success',
            'Code': result
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    if data['MessageType'] == "Image":
        image_b64 = data['imageBase64']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        decoded_bytes = base64.b64decode(image_data)
        image_data_decoded = io.BytesIO(decoded_bytes)
        image = Image.open(image_data_decoded)
        image_array = np.array(image)[:,:,3]

        SaveImageToDatabase(data["ModelName"], data["Digit"], image_array)

        response_data = {
        'result': 'success',
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    if data['MessageType'] == "StartTrain":
        img, digits = GetImmagesFromDatabase(data["ModelName"])
        x_train = np.stack(img)
        y_train = np.stack(digits)
        trainModel(x_train,y_train,f"models/{data['ModelName']}")
        ###
        response_data = {
        'result': 'success',
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}


@app.route("/recognize.html/data", methods  = ['GET'])
def GetModels():
    models = getModelNames()
    return jsonify(models)

@app.route('/recognize.html', methods=['POST'])
def Process():
    data = request.get_json()
    if data['cmd'] == "Recognise":
        image_b64 = data['imageBase64']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        decoded_bytes = base64.b64decode(image_data)
        image_data_decoded = io.BytesIO(decoded_bytes)
        image = Image.open(image_data_decoded)
        image_array = np.array(image)[:,:,3]
        image_array = np.invert(np.array([image_array]))
        image_array = image_array.reshape(28,28)
        
        
        digit = r.Recognise(image_array)
        
        response_data = {
            'digit': str(digit)
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    elif data['cmd'] == "ChangeModel":
        r.setModel(data['model'])
        response = {
        "status": "success",
        }

        return json.dumps(response)

@app.route('/update.html')
def UpdatePage():
    return render_template("update.html")


@app.route("/update.html/data", methods  = ['GET'])
def GetModelsUpdate():
    models = getModelNames(True)
    return jsonify(models)

@app.route('/update.html', methods=['POST'])
def ProcessUpdate():
    data = request.get_json()
    if data['cmd'] == "Recognise":
        r.setModel(data['model'])
        image_b64 = data['imageBase64']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        decoded_bytes = base64.b64decode(image_data)
        image_data_decoded = io.BytesIO(decoded_bytes)
        image = Image.open(image_data_decoded)
        image_array = np.array(image)[:,:,3]
        image_array = np.invert(np.array([image_array]))
        image_array = image_array.reshape(28,28)
        
        
        digit = r.Recognise(image_array)
        
        response_data = {
            'digit': str(digit)
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    elif data['cmd'] == "ChangeModel":
        r.setModel(data['model'])
        response = {
        "status": "success",
        }

        return json.dumps(response)
    elif data['cmd'] == "SaveImage":
        image_b64 = data['imageBase64']
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        decoded_bytes = base64.b64decode(image_data)
        image_data_decoded = io.BytesIO(decoded_bytes)
        image = Image.open(image_data_decoded)
        image_array = np.array(image)[:,:,3]

        SaveImageToDatabase(data["ModelName"], data["Digit"], image_array)

        response_data = {
        'result': 'success',
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    elif data['cmd'] == "Retrain":
        img, digits = GetImmagesFromDatabase(data["ModelName"])
        x_train = np.stack(img)
        y_train = np.stack(digits)
        trainModel(x_train,y_train,f"models/{data['ModelName']}")
        ###
        response_data = {
        'result': 'success',
        }
        return json.dumps(response_data), 200, {'ContentType': 'application/json'}
    else:
        print(f"Command {data['cmd']} not identified")


        



@app.route('/hello')
def hello():
    return 'Hello, World'


if __name__ == '__main__':
    
    app.run()