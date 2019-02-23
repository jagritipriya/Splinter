import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
import pandas as pd
np.random.seed(42)

class FFNN:
    def init_network(self,n_inputs = None, dropout = 0.5, num_classes = 2,input_activation_function = 'relu' ,output_activation_function = 'softmax'):
        # Create a keras sequential model
        model = Sequential()
        # Add first layer that has 512 nodes and accepts the input of dimension number_of_input_nodes
        # activation function used is 'relu'
        model.add(Dense(512, activation= input_activation_function, input_dim=n_inputs))
        # Drop in the learning rate
        model.add(Dropout(0.5))
        # In second layer the activation function is 'softmax' 
        model.add(Dense(num_classes, activation='softmax'))
        # print the model information
        print(model.summary())  
        model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
        return model
    
    def train_model(self,x_train,y_train,x_test,y_test,epochs = 2,batch_size = 32):
        hist = self.fit(x_train, y_train,
          batch_size=32,
          epochs=10,
          validation_data=(x_test, y_test), 
          verbose=2)