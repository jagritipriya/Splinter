import numpy as np
import json
import string
class PreProcessData:
    def remove_punctuaion(self,string_list):
        print("Removing Punctuations...")
        for i in range(len(string_list)):
            exclude = set(string.punctuation)
            string_list[i] = ''.join(ch for ch in string_list[i] if ch not in exclude)
    #    print("Exiting remove_punctuation")
        return string_list
    
    def get_unique_words(self,string_list):
       # print("Inside get_unique_words")
        unique_words = []
        for line in string_list:
            # Convert all the reviews into lower-case alphabets
            for word in line.lower().split():
                unique_words.append(word)
        unique_words = list(set(unique_words))
       # print("Exiting get_unique_words")
        return unique_words

    def create_dictionary(self,string_list):
       # print("Inside create_dictionary")
        # Creating a word-to-index dictionary 
        word2index = dict()
        # Unique_word will be a set of all the unique words present in all the reviews 
        unique_words = self.get_unique_words(string_list)

        # Size of the vocabulary 
        number_of_input_nodes = len(unique_words)
     #   print("Size of the vocab(number of the nodes in input_layer of ANN): ",number_of_input_nodes)

        # Populate the word-to-index dictionary using the unique_word list
        word2index = dict()
        for i,word in enumerate(unique_words):
            word2index[word] = i
     #   print("Exiting create_dictionary")
        return word2index

    def update_dictionary(self,old_dictionary,string_list):
        print("Inside update_dictionary")
        new_word2index = self.create_dictionary(string_list)
        old_dictionary.update(new_word2index)
        print("Exiting update_dictionary")
        return old_dictionary

    def text_to_numbers(self,string_list,word2index=None):
        #print("Inside text_to_numbers")
        # Convert all the reviews into numerical format using word-to-index dictionary
        # list 'test' and all the print statements are for validation purpose
        num_reviews =[]
        word_count = 0
        flag = 0

        string_list = self.remove_punctuaion(string_list)
        if word2index==None:
            word2index = self.create_dictionary(string_list)
        for line in string_list:
            text_rev = []
            #if flag is 0:
            #print("String is :", line)
            for word in line.lower().split():
                #if flag is 0:
                #    word_count+=1
                    #print("words are : ", word)
               # if flag is 0:
                    #print("texts are : ", word2index[word])
                if word in list(word2index.keys()):
                    text_rev.append(word2index[word])
            if flag is 0:
                #print("text review is ",text_rev)
                #print("word count is ",word_count)
                #print("length of text rev is ",len(text_rev))
                flag = 1
            num_reviews.append(text_rev)
        # num_reviews contains the reviews in numerical format
        #print("String in numerical format : ",num_reviews[0])
        #print("Exiting text_to_numbers")
        return num_reviews


    def shuffle_dataset(self,dataframe):
        #print("Inside shuffle_dataset")
        import random
        data_review = []
        data_label = []
        data_tuples = tuple()
        reviews = dataframe['review']
        labels = dataframe['label']
        data_tuple = list(zip(reviews,labels))
        #print("Zipped (review,label) tuple : \n ",data_tuple[0])
        random.shuffle(data_tuple)
        for review,label in data_tuple:
            data_review.append(review)
            data_label.append(label)
        #print("Exiting shuffle_dataset")
        return data_review,data_label

    def one_hot_encode(self,string_list,unique_word_len = None):
        print("One-Hot-Encoding the Reviews...")
        # One-Hot-Encode all the reviews
        # Kears Tokenizer doesn't work properly in this case, || Wrote our own code 
        OHE_Reviews = []
        #unique_words = self.get_unique_words(string_list)
        #print("unique_words are like : ",unique_words[:5])
        #numerical_string = self.text_to_numbers(string_list)
        numerical_string = string_list
        for line in numerical_string:
            one_hot_encoded = np.zeros(unique_word_len)
            for index in line:
                one_hot_encoded[index] = 1
            OHE_Reviews.append(one_hot_encoded)
        #print("Exiting one_hot_encode")
        return np.array(OHE_Reviews)

    def PreProcessReviews(self,reviews):
        print("Preprocessing the Reviews...")
        with open('./Data/WordToIndex.json', 'r') as fp:
            word2index = json.load(fp)
        unique_word_len = len(word2index)
        reviews = self.remove_punctuaion(reviews)
        num_reviews = self.text_to_numbers(reviews,word2index=word2index)
        One_Hot_Encoded_Reviews = self.one_hot_encode(num_reviews,unique_word_len)
        return One_Hot_Encoded_Reviews

        