from CustomNeuralNetwork import FFNN
from Preprocess import PreProcessData
import pandas as pd

preprocess = PreProcessData()

data = pd.read_csv("imdb_master.csv", encoding = 'latin1')

# Shuffle the datasets and split into two different lists data_review, data_label

data_review,data_label,num_inputs = preprocess.shuffle_dataset(data)

print("data_label : ",data_label)

# One hot encode reviews and labels
data_label = preprocess.one_hot_encode(data_label)
data_review = preprocess.one_hot_encode(data_review)
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