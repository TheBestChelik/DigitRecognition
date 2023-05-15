import tensorflow as tf
import matplotlib.pyplot as plt

def trainModel(x_train, y_train, modelName):
    x_train = tf.keras.utils.normalize(x_train, axis= 1)

    print(type(y_train))
    print(x_train.shape)
    #x_test = tf.keras.utils.normalize(x_test, axis= 1)
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (28,28)))

    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))

    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss=tf.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=3, batch_size=1)

    model.save(modelName)

    return 1


if __name__ == "__main__":
    mnist = tf.keras.datasets.mnist
    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    
  

    trainModel(x_train, y_train, "Mnisk")