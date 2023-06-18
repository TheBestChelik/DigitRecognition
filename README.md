# Table of Contents
- [Table of Contents](#table-of-contents)
- [DigitRecognition](#digitrecognition)
  - [Digit Recognition mode](#digit-recognition-mode)
  - [Train mode](#train-mode)
  - [Update model mode](#update-model-mode)
  - [Requirements](#requirements)
  - [Run the application](#run-the-application)
    - [Instalation](#instalation)
    - [Run](#run)
# DigitRecognition
This project showcases the core concept of utilizing AI for recognizing handwritten digits. It includes a pre-existing MNIST model, consisting of a dataset with 60,000 images. The project also offers the option to train a custom model using TensorFlow, allowing users to enhance the AI's recognition capabilities

## Digit Recognition mode
![](https://github.com/TheBestChelik/DigitRecognition/blob/master/screens/Recognize.png?raw=true)

In this mode, you can select a specific model from a dropdown list and draw a digit on the canvas. The canvas size is 560x560 pixels, and the drawn image is automatically converted to a 28x28 pixel image. This image is then sent to the server, where TensorFlow utilizes the chosen model to recognize the digit. The result of the recognition process is displayed in a designated field. To clear the canvas, simply press the right mouse button.

## Train mode
![](https://github.com/TheBestChelik/DigitRecognition/blob/master/screens/Train.png?raw=true)

In this mode, you have the opportunity to train your own model. Follow these steps:

1. Enter the desired name for your future model in the designated field.
2. Use the "Draw Digit" field to draw the digit you want to train the model on.
3. Click the "Save" button.
4. Repeat steps 2 and 3 until you reach 100% progress.
5. Finally, press the "Train" button and enjoy your newly trained model.

To ensure accuracy, the program will prompt you to draw 10 copies of each digit, resulting in a total of 100 images. While this might not be sufficient, you can enhance the model's accuracy further by utilizing the "Update Model" mode.

Similar to the Recognize mode, the canvas size is 560x560 pixels, and the drawn image is converted to a 28x28 pixel format before being sent to the server. These images are then saved in a database using SQLite. When the Train button is pressed, all the images in the database are utilized for model training using TensorFlow.

As a convenient feature, you can clear the canvas at any time by pressing the right mouse button. 
## Update model mode
![](https://github.com/TheBestChelik/DigitRecognition/blob/master/screens/Update.png?raw=true)

In this mode, you can update your existing models. Please note that only editable models, which are stored in the database, can be updated. The MNIST model, for example, cannot be updated since it is not present in the database file.

Follow these steps to update your model:

1. Select the model you would like to update from the available options.
2. Use the canvas to draw a digit. The selected model will attempt to recognize the digit, and the result will be displayed in a designated field.
3. If the number was correctly guessed by the model, simply press the "Save" button. If it was not guessed correctly, enter the correct digit in the field and then press "Save".
4. When you believe you have corrected an adequate number of digits, press the "Retrain" button.

During the update process, all the images you drew will be saved in the database for the chosen model. Once you press the "Retrain" button, the training process will commence, utilizing all the images from the database.

## Requirements
- Python 3.6+
- NumPy
- TensorFlow
- sqlite
- flask

## Run the application
### Instalation   
   Clone repository
   ```bat 
   gh repo clone TheBestChelik/DigitRecognition
   ```
   Install requirements
   ```bat
   pip install -r requirements.txt 
   ```
### Run
   ```shell
   cd digitRecognition
   python main.py
   ```