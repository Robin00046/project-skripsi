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
dataset.head(30)
#mengganti null
dataset['sta_bangunan']=dataset['sta_bangunan'].replace(0,np.nan)
dataset['sta_lahan']=dataset['sta_lahan'].replace(0,np.nan)
dataset['lantai']=dataset['lantai'].replace(0,np.nan)
dataset['dinding']=dataset['dinding'].replace(0,np.nan)
dataset['kondisi_dinding']=dataset['kondisi_dinding'].replace(0,np.nan)
dataset['atap']=dataset['atap'].replace(0,np.nan)
dataset['kondisi_atap']=dataset['kondisi_atap'].replace(0,np.nan)
dataset.head(20)
#imputassi missing value
fill=dataset["kondisi_dinding"].mean()
dataset["kondisi_dinding"]=dataset["kondisi_dinding"].fillna(fill)
fill=dataset["kondisi_atap"].mean()
dataset["kondisi_atap"]=dataset["kondisi_atap"].fillna(fill)
#outlier
q1=dataset['lantai'].quantile(0.25)
q3=dataset['lantai'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['sta_bangunan'].quantile(0.25)
q3=dataset['sta_bangunan'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['sta_lahan'].quantile(0.25)
q3=dataset['sta_lahan'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['dinding'].quantile(0.25)
q3=dataset['dinding'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['kondisi_dinding'].quantile(0.25)
q3=dataset['kondisi_dinding'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['atap'].quantile(0.25)
q3=dataset['atap'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['kondisi_atap'].quantile(0.25)
q3=dataset['kondisi_atap'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['sumber_airminum'].quantile(0.25)
q3=dataset['sumber_airminum'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['cara_peroleh_airminum'].quantile(0.25)
q3=dataset['cara_peroleh_airminum'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['ibu_hamil'].quantile(0.25)
q3=dataset['ibu_hamil'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['anak_sekolah'].quantile(0.25)
q3=dataset['anak_sekolah'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['lansia'].quantile(0.25)
q3=dataset['lansia'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
q1=dataset['balita'].quantile(0.25)
q3=dataset['balita'].quantile(0.75)
iqr=q3-q1
lower_bound=q1-1.5*iqr
upper_bound=q3+1.5*iqr
#pemilian atribut
x= dataset.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
y= dataset['penerima_pkh']
#Scaling
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
data_scaled_minmax = data_scaler_minmax.fit_transform(x)
data_scaled_minmax
#smote
from imblearn.combine import SMOTETomek
from collections import Counter
os=SMOTETomek(1)
X_train_ns,y_train_ns=os.fit_resample(x,y)
print("The number of classes before fit {}".format(Counter(y)))
print("The number of classes after fit {}".format(Counter(y_train_ns)))
#memecah training set dan test set
from sklearn.model_selection import KFold
kf = KFold(n_splits=10)
for train_index, test_index in kf.split(x):
  print("TRAIN:", train_index, "TEST:", test_index)
  x_train, x_test = x.iloc[train_index], x.iloc[test_index]
  y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#membuat model random forest clasification
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=5, criterion='entropy', random_state=0)
classifier.fit(x_train, y_train)
#memprediksi
y_pred = classifier.predict(x_test)
y_pred
#ambil
pickle.dump(classifier, open('model1.pkl', 'wb'))
# Loading model to compare the results
model = pickle.load(open('model1.pkl','rb'))