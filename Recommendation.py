from CustomNeuralNetwork import FFNN
from Preprocess import PreProcessData
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from Selenium import Selenium
from QureyParser import QueryParser
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
class Recommender:
    NeuralNets = FFNN()
    QP = QueryParser()
    preprocess = PreProcessData()
    RESTAURANT_LIST = "./Restaurant_Reviews/Restaurant_List.csv"
    RESTAURANT_REPOSITORY = "./Restaurant_Reviews/"
    def EatAt(self):
        

        data = pd.read_csv("imdb_master.csv", encoding = 'latin1')

        # Shuffle the datasets and split into two different lists data_review, data_label

        data_review,data_label,num_inputs = self.preprocess.shuffle_dataset(data)

        print("data_label : ",data_label)

        # One hot encode reviews and labels
        data_label = self.preprocess.one_hot_encode(data_label)
        data_review = self.preprocess.one_hot_encode(data_review)
        neuralnetwork = FFNN()
        # (self,n_inputs = None, dropout = 0.5, num_classes = 2,input_activation_function = 'relu' ,output_activation_function = 'softmax')
        model = neuralnetwork.init_network(n_inputs = num_inputs)

        x_train = data_review[:10]
        x_test = data_review[10:]
        y_train = data_label[:10]
        y_test = data_label[10:]
        # train_model(self,x_train,y_train,x_test,y_test,epochs = 2,batch_size = 32)
        model.fit(x_train, y_train,
                batch_size=32,
                epochs=10,
                validation_data=(x_test, y_test), 
                verbose=2)


        print("One hot encoded labels are : ", data_label)

        print("One hot encoded reviews are : ", list(data_review[0]).count(1))
    
    def JudgeTheRestaurant(self):
        filename = self.SuggestMe()
        reviews = self.GetReviews(filename)
        veg_reviews,nonveg_reviews = self.CategorizeTheReviews(reviews)
        print("Number of Veg Reviews: {} and NonVeg Reviews: {} ".format(len(veg_reviews),len(nonveg_reviews)))
        ambience_rating = round(self.NeuralNets.AmbienceRating(veg_reviews),1)
        print("Ambience Rating is: {}".format(ambience_rating))
        service_rating = round(self.NeuralNets.ServiceRating(veg_reviews),1)
        print("Service Rating is: {}".format(service_rating))
        food_rating = round(self.NeuralNets.FoodRating(veg_reviews),1)
        print("Food Rating is: {}".format(food_rating))
        with open('./Data/Restaurant_Information.json', 'r') as fp:
            Restaurants = json.load(fp)
        
        key = self.QP.matchChoices(filename,list(Restaurants.keys()))

        Price_two = int(Restaurants[key]['price_two'])
        Know_for = Restaurants[key]['known_for']
        What_People_love_here = Restaurants[key]['what_people_love_here']

        Testing_Parametres = [Price_two/2,ambience_rating,service_rating,food_rating]
        Testing_Parametres = [Testing_Parametres]
        decision = self.LogicallyDecide(Testing_Parametres)
        if decision:
            print("I think you should go to this restaurant. ")
            print("Quick Facts: \n")
            if len(Know_for) >0:
                print("This Restaurant is known for: ",Know_for)
            if len(What_People_love_here) > 0:
                people_loves_here = ''
                if len(What_People_love_here)> 2:
                    people_loves_here = ', '.join(What_People_love_here[:-1])
                    people_loves_here += ' and {}'.format(What_People_love_here[-1])
                else:
                    people_loves_here = 'and'.join(What_People_love_here)
                print("People Loves {} here.".format(people_loves_here))
        else:
            print("Naah ! This restaurant is not for you.")




    def LogicallyDecide(self,Parameters):
        from sklearn.externals import joblib
        self.Generate_LR_Model()
        logmodel = joblib.load('./NeuralNets/LRModel.pkl')
        pred = pd.Series(logmodel.predict(Parameters))
        pred = list(pred)[0]
        if pred in 'pos':
            return True
        else:
            return False
    
    def Generate_LR_Model(self):
        
        rest_data=pd.read_csv("./Data/MyPreferences.csv")
        #rest_data.head()

        #sns.countplot(x="Overall",data=rest_data)

        #sns.countplot(x="Overall",hue="Ambience",data=rest_data)

        #sns.countplot(x="Overall",hue="Service",data=rest_data)

        #rest_data["Service"].plot.hist()

        #rest_data.info()

        X=rest_data.drop("Overall",axis=1)
        X=X.drop("Distance",axis=1)
        y=rest_data["Overall"]

        X_train = X
        y_train = y
        
        from sklearn.linear_model import LogisticRegression
        #from sklearn.pipeline import make_pipeline
        #from sklearn.preprocessing import StandardScaler
        from sklearn.externals import joblib

        logmodel=LogisticRegression()
        logmodel.fit(X_train,y_train)
        joblib.dump(logmodel, './NeuralNets/LRModel.pkl')


    def CategorizeTheReviews(self,reviews):
        Veg_Reviews,NonVeg_Reviews = self.NeuralNets.CategorizeReviews(reviews)
        return Veg_Reviews,NonVeg_Reviews
    
    def AmbienceRating(self,reviews):
        ambience = self.NeuralNets.AmbienceRating(reviews)

    def GetReviews(self,filename):
        data = open(filename,'r')
        review_string = data.read()
        reviews = re.split(r'\d\.\d<>',review_string)
        return reviews
    
    def SuggestMe(self):
        restaurant_name = input("Which Restaurant ? ")
        restaurant_url,file_name = self.SelectRestaurant(restaurant_name)
        print("The URL is : ",restaurant_url)
        print("Wait...! I am Downloading the reviews of this restaurant")
        restaurant_file = open(self.RESTAURANT_LIST,'a')
        restaurant_file.close()
        restaurant_file = open(self.RESTAURANT_LIST,'r')
        restaurant_list = []
        for line in restaurant_file:
            restaurant_list.append(line[:-1])
        review_filename = self.RESTAURANT_REPOSITORY+file_name+".txt"
        restaurant_file.close()
        #print("Restaurant List:",restaurant_list)
        if file_name in restaurant_list:
            print("File Already Exist")
            return review_filename
        #print("File not found ")
        #exit()
        Sel = Selenium()
        Sel.run(restaurant_url,file_name)
        print("Reviews are downloaded")
        restaurant_file = open(self.RESTAURANT_LIST,'a')
        restaurant_file.write(file_name+"\n")
        restaurant_file.close()
        return review_filename


    def SelectRestaurant(self,restaurant_name):
        choices = self.FindZomatoURL(restaurant_name)
        print("Which restaurant are you looking for the {} in {}".format(restaurant_name,' or '.join(list(choices.keys()))))
        choice = input("Tell me : ")
        choice = self.QP.matchChoices(choice,list(choices.keys()))
        return choices[choice]

    def FindZomatoURL(self,restaurant_name):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        response = requests.get("https://www.google.com/search?source=hp&ei=TmZpXJWwFMaFyAO3sJvYAQ&q="+restaurant_name+"restaurant bangalore site:zomato.com")

        content = response.content
        soup = BeautifulSoup(content,"html.parser")

        all_the_urls=""
        tags = soup.find_all('a')
        all_the_urls=[]
        for tag in tags:
            found = re.findall(r'/url\?q=(https://www.zomato.com/bangalore/.*-.*)/',tag.get('href'))
            if len(found):
                all_the_urls.append(found[0])
        unique_urls=list(set(all_the_urls))
        rest_urls = []
        for url in unique_urls:
            name = url.split('/')[-1]
            rest_urls.append(name)
        loc=[]
        loc_name=[]
        for url in rest_urls:
            filename=url.split('-')
            location=url.split('-')[1:]
            loc_name.append('-'.join(filename))
            l=' '.join(location)
            loc.append(l)
        restaurants=dict()
        for i in range(len(loc)):
            restaurants[loc[i]]=(all_the_urls[i],loc_name[i])
        return restaurants