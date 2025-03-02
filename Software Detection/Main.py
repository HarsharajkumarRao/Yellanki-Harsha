#============================= IMPORT LIBRARIES =============================

import pandas as pd
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")

#============================= DATA SELECTION ==============================

dataframe=pd.read_csv("Data.csv")

print("----------------------------------------------------")
print("Input Data          ")
print("----------------------------------------------------")
print()
print(dataframe.head(20))

#============================= PREPROCESSING ==============================

#==== checking missing values ====

print("----------------------------------------------------")
print("Checking Missing Values          ")
print("----------------------------------------------------")
print()
print(dataframe.isnull().sum())

#==== label encoding ====

print("----------------------------------------------------")
print("Before Label Encoding          ")
print("----------------------------------------------------")
print()
print(dataframe['defects'].head(15))
print()
label_encoder=preprocessing.LabelEncoder()

print("----------------------------------------------------")
print("After Label Encoding          ")
print("----------------------------------------------------")
print()
dataframe['defects']=label_encoder.fit_transform(dataframe['defects'])

# dataframe=dataframe.

dataframe=dataframe.apply(preprocessing.LabelEncoder().fit_transform)
print(dataframe['defects'].head(15))
print()

#============================= FEATURE SELECTION ============================


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


x=dataframe.drop('defects',axis=1)
y=dataframe['defects']

chi2_features = SelectKBest(chi2,k=10)


x_kbest= chi2_features.fit_transform(x, y)

print("---------------------------------------------------")
print("Feature Selection --- > Chi Square")
print("---------------------------------------------------")
print()
print(" The original features is :", x.shape[1])
print()
print(" The reduced feature is   :",x_kbest.shape[1] )
print()

#============================ DATA SPLITTING ============================


from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)

print("---------------------------------------------------")
print("Data Splitting")
print("---------------------------------------------------")
print()
print("Total No.of dataset =", x.shape[0])
print()
print("Total No.of train data =", x_train.shape[0])
print()
print("Total No.of test data =", x_test.shape[0])
print()


#============================ CLASSIFICATION ============================

# === ANN ===

print("---------------------------------------------------")
print("Deep Learning (ANN)")
print("---------------------------------------------------")
print()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Dense
classifier = Sequential() 
classifier.add(Dense(activation = "relu", input_dim = 21, units = 8, kernel_initializer = "uniform")) 
classifier.add(Dense(activation = "relu", units = 14,kernel_initializer = "uniform")) 
classifier.add(Dense(activation = "sigmoid", units = 1,kernel_initializer = "uniform")) 
classifier.compile(optimizer = 'adam' , loss = 'mae', metrics = ['mae','accuracy'] ) 
history=classifier.fit(x_train,y_train, batch_size = 1000 ,epochs = 10 )

acc_ann=history.history['accuracy']

acc_ann=max(acc_ann)*100

pred_ann=classifier.predict(x_test)

y_pred1 = pred_ann.reshape(-1)
y_pred1[y_pred1<0.5] = 0
y_pred1[y_pred1>=0.5] = 1
y_pred1 = y_pred1.astype('int')

from sklearn.metrics import confusion_matrix

cm1 = confusion_matrix(y_test,pred_ann)

from sklearn import metrics

acc_ann=metrics.accuracy_score(y_test,pred_ann)*100

print("---------------------------------------------------")
print("Performance Analysis ---> ANN ")
print("---------------------------------------------------")

print()
print("1. Accuracy :",acc_ann )
print()
print("2.Classification report")
print()
print(metrics.classification_report(y_test,pred_ann))
print()
import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(cm1, annot=True)
plt.title("Artificial Neural Network")
plt.show()





# ==== SVM ====

from sklearn.svm import SVC

svc_model = SVC(C= .1, kernel='linear', gamma= 1)
svc_model.fit(x_train[0:200], y_train[0:200])

y_pred_svm=svc_model.predict(x_train[0:200])

from sklearn import metrics
acc_svm=metrics.accuracy_score(y_pred_svm,y_train[0:200])*100

print("---------------------------------------------------")
print("Performance Analysis ---> SVM ")
print("---------------------------------------------------")
print()

print("1.Accuracy",acc_svm)
print()
print("2.Classification report")
print()
print(metrics.classification_report(y_train[0:200],y_pred_svm))
print()
cm1 = confusion_matrix(y_train[0:200],y_pred_svm)

sns.heatmap(cm1, annot=True)
plt.title("Support Vector Machine")
plt.show()

#======================== PREDICTION =============================

print("---------------------------------------------------")
print("Prediction")
print("---------------------------------------------------")
print()

for i in range(10,20):
    if y_pred_svm[i]==0:
        print("----------------------")
        print()
        print([i],"No Software Defects")
    elif y_pred_svm[i]==1:
        print("----------------------")
        print()
        print([i],"Software Defects")

print()
print("-----------------------------------------------------------------------")
print()


import matplotlib.pyplot as plt
vals=[acc_ann,acc_svm]
inds=range(len(vals))
labels=["ANN ","SVM"]
fig,ax = plt.subplots()
rects = ax.bar(inds, vals)
ax.set_xticks([ind for ind in inds])
ax.set_xticklabels(labels)
plt.title('Comparison graph')
plt.show() 
























