from matplotlib import pyplot as plt
import tensorflow as tf
import cv2
import numpy as np
import os
class Recognizer:
    def __init__(self):
        pass
    def SetModel(self, modelName):
        self.model = tf.keras.models.load_model(modelName)
    
    def Recognize(self, img):
        img = np.invert(np.array([img]))
        prediction = self.model.predict(img, verbose = 0)
        return np.argmax(prediction)

# if __name__ == "__main__":
#     mnist = tf.keras.datasets.mnist
#     (x_train, y_train),(x_test, y_test) = mnist.load_data()

#     x_train = tf.keras.utils.normalize(x_train, axis= 1)
#     x_test = tf.keras.utils.normalize(x_test, axis= 1)
#     model = tf.keras.models.load_model("handwriten.model")

#     print(model.evaluate(x_test, y_test))
#     i = 0
#     with open("digits/ans.txt", "r") as f:
#         ans = f.read()



#     while os.path.isfile(f"digits/{i}.png"):
#         img = cv2.imread(f"digits/{i}.png")[:,:,0]
        

#         img = np.invert(np.array([img]))
#         #img = tf.keras.utils.normalize(img, axis=1)
#         prediction = model.predict(img)
#         print(ans[i], " ==> ",np.argmax(prediction))
#         i+=1
