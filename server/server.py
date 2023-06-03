from io import StringIO
import io
import json
import sys
from flask import Flask, render_template, request
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import base64
import re
import os


from AI.digitRecogniser import Recognizer


class R:
    def __init__(self) -> None:
        self.recognizer = Recognizer()
        self.recognizer.SetModel("models\Hyi.model")
    def Recognise(self, image):
        return self.recognizer.Recognize(image)
    
r = R()
app = Flask(__name__,
            static_url_path='',
            static_folder='static')


def CheckModelNameValidity(ModelName):
    #0 - OK
    #1 - name too short
    #2 - name already taken
    if len(ModelName) < 3:
        return 1
    if os.path.exists(f"models/{ModelName}"):
        return 2
    return 0

@app.route('/')
def HomePage():
    return render_template("home.html")

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


@app.route('/recognize.html', methods=['POST'])
def get_image():
    image_b64 = request.values['imageBase64']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    decoded_bytes = base64.b64decode(image_data)
    image_data_decoded = io.BytesIO(decoded_bytes)
    image = Image.open(image_data_decoded)
    image_array = np.array(image)[:,:,3]
    image_array = np.invert(np.array([image_array]))
    image_array = image_array.reshape(28,28)
    
    digit = r.Recognise(image_array)
    
    response_data = {
        'result': 'success',
        'digit': str(digit)
    }
    return json.dumps(response_data), 200, {'ContentType': 'application/json'}

@app.route('/hello')
def hello():
    return 'Hello, World'


if __name__ == '__main__':
    
    app.run()