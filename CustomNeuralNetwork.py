import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
import pandas as pd
from keras.models import load_model
from Preprocess import PreProcessData
np.random.seed(42)

class FFNN:
    PPD = PreProcessData()
    CATEGORY_ANN = './NeuralNets/Categorize.h5'
    AMBIENCE_ANN = './NeuralNets/Ambience.h5'
    SERVICE_ANN = './NeuralNets/Service.h5'
    OVERALL_ANN = './NeuralNets/Overall.h5'
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
    
    def CategorizeReviews(self,reviews):
        Processed_Reviews = self.PPD.PreProcessReviews(reviews)
        Veg_reviews = []
        Nonveg_reviews = []
        model = load_model(self.CATEGORY_ANN)
        for review in Processed_Reviews:
            q = model.predict( np.array( [review,] )  )
            prediction = q[0][1]
            if prediction > 0.5:
                Veg_reviews.append(review)
            else:
                Nonveg_reviews.append(review)
        return Veg_reviews,Nonveg_reviews
    
    def AmbienceRating(self,reviews):
        ratings = []
        model = load_model(self.AMBIENCE_ANN)
        for review in reviews:
            q = model.predict( np.array( [review,] )  )
            prediction = round(q[0][1],2)
            ratings.append(5*prediction)
        return np.mean(ratings)
    
    def ServiceRating(self,reviews):
        service_ratings = []
        model = load_model(self.SERVICE_ANN)
        for review in reviews:
            q = model.predict( np.array( [review,] )  )
            prediction = round(q[0][1],2)
            service_ratings.append(5*prediction)
        return np.mean(service_ratings)
    
    def FoodRating(self,reviews):
        food_rating = []
        model = load_model(self.OVERALL_ANN)
        for review in reviews:
            q = model.predict( np.array( [review,] )  )
            prediction = round(q[0][1],2)
            food_rating.append(5*prediction)
        return np.mean(food_rating)



                

