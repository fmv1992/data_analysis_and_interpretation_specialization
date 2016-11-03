# pylama:skip=1

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import sklearn.metrics

import zipfile
with zipfile.ZipFile('../data_set/tree_addhealth.zip', 'r') as zipfileobj:
    with zipfileobj.open('tree_addhealth.csv', 'r') as csvfile:
        db = pd.read_csv(csvfile)

"""
Data Engineering and Analysis
"""
#Load the dataset

AH_data = db.copy()

data_clean = AH_data.dropna()

data_clean.dtypes
data_clean.describe()


"""
Modeling and Prediction
"""
#Split into training and testing sets

predictors = data_clean[['BIO_SEX','HISPANIC','WHITE','BLACK','NAMERICAN','ASIAN',
'age','ALCEVR1','ALCPROBS1','marever1','cocever1','inhever1','cigavail','DEP1',
'ESTEEM1','VIOL1','PASSIST','DEVIANT1','SCHCONN1','GPA1','EXPEL1','FAMCONCT','PARACTV',
'PARPRES']]

targets = data_clean.TREG1

pred_train, pred_test, tar_train, tar_test  =   train_test_split(predictors, targets, test_size=.4)

print('shape', pred_train.shape)
print('shape', pred_test.shape)
print('shape', tar_train.shape)
print('shape', tar_test.shape)

#Build model on training data
classifier=DecisionTreeClassifier()
classifier=classifier.fit(pred_train,tar_train)

predictions=classifier.predict(pred_test)

print('conf matrix', sklearn.metrics.confusion_matrix(tar_test,predictions))
print('acc score', sklearn.metrics.accuracy_score(tar_test, predictions))

#Displaying the decision tree
from sklearn import tree
#from StringIO import StringIO
from io import StringIO
#from StringIO import StringIO
from IPython.display import Image
out = StringIO()
tree.export_graphviz(classifier, out_file=out)
import pydotplus
graph=pydotplus.graph_from_dot_data(out.getvalue())
with open('graph.png', 'wb') as f:
   f.write(graph.create_png())