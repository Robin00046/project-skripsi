#library yang diperlukan
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy as sp
import pickle
from sklearn import preprocessing

#import dataset
dataset=pd.read_csv('data_set.csv')

#pemilihan fitur
x= dataset.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
y= dataset.iloc[:, 15]

#Scaling
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
data_scaled_minmax = data_scaler_minmax.fit_transform(x)
data_scaled_minmax

#memecah training set dan test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.20, random_state=0)
x_train

#membuat model random forest clasification
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=0)
classifier.fit(x_train, y_train)

#memprediksi
y_pred = classifier.predict(x_test)
y_pred
#save to disk

pickle.dump(classifier, open('model.pkl', 'wb'))
# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))