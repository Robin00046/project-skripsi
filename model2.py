#library yang diperlukan
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle
import scipy as sp
from sklearn import preprocessing
#import dataset
dataset=pd.read_csv('data_set.csv')
#mengganti 0 menjadi null
dataset['sta_bangunan']=dataset['sta_bangunan'].replace(0,np.nan)
dataset['sta_lahan']=dataset['sta_lahan'].replace(0,np.nan)
dataset['lantai']=dataset['lantai'].replace(0,np.nan)
dataset['dinding']=dataset['dinding'].replace(0,np.nan)
dataset['kondisi_dinding']=dataset['kondisi_dinding'].replace(0,np.nan)
dataset['atap']=dataset['atap'].replace(0,np.nan)
dataset['kondisi_atap']=dataset['kondisi_atap'].replace(0,np.nan)
dataset.head(20)
#prosesss imputasi
fill=dataset["kondisi_dinding"].mean()
dataset["kondisi_dinding"]=dataset["kondisi_dinding"].fillna(fill)
fill=dataset["kondisi_atap"].mean()
dataset["kondisi_atap"]=dataset["kondisi_atap"].fillna(fill)
#outlierss
q1=dataset['lantai'].quantile(0.25)
q3=dataset['lantai'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
#pemilihan atribut dan classs
x= dataset.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
y= dataset['penerima_pkh']
#Scaling
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
data_scaled_minmax = data_scaler_minmax.fit_transform(x)
data_scaled_minmax
#smote
from collections import Counter
from imblearn.over_sampling import SMOTE
smt = SMOTE(1)
X_train_SMOTE, y_train_SMOTE = smt.fit_resample(x, y)
print("The number of classes before fit {}".format(Counter(y)))
print("The number of classes after fit {}".format(Counter(y_train_SMOTE)))
#memecah training set dan test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X_train_SMOTE, y_train_SMOTE, test_size= 0.30, random_state=0)
#membuat model random forest clasification
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=5, criterion='entropy', random_state=0)
classifier.fit(x_train, y_train)
#memprediksi
y_pred = classifier.predict(x_test)
y_pred
#ambil
pickle.dump(classifier, open('model2.pkl', 'wb'))
# Loading model to compare the results
model = pickle.load(open('model2.pkl','rb'))