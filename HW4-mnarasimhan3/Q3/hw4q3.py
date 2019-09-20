## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.30, random_state =100, shuffle = True)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
reg = LinearRegression()
reg.fit(x_train, y_train)

reg_y_pred = reg.predict(x_test)

reg_y_train = reg.predict(x_train)
reg_train_accuracy = accuracy_score(y_train, reg_y_train.round())
reg_test_accuracy = accuracy_score(y_test, reg_y_pred.round())
print('Regression train accuracy', reg_train_accuracy)
print('Regression test accuracy', reg_test_accuracy)

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX


# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX

rf = RandomForestClassifier()
rf.fit(x_train, y_train)
# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
rf_y_pred = rf.predict(x_test)
rf_y_train = rf.predict(x_train)

rf_train_accuracy = accuracy_score(y_train, rf_y_train.round())
rf_test_accuracy = accuracy_score(y_test, rf_y_pred.round())
print('Random Forest train accuracy', rf_train_accuracy)
print('Random Forest test accuracy', rf_test_accuracy)

# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
importance = rf.feature_importances_

args = np.argsort(-importance)
print(importance)
print('Feature numbers', x_train.columns[args])
print('Best feature', x_train.columns[args[0]])
print('Least feature', x_train.columns[args[-1]])

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX

param_grid = {'n_estimators': [25,50,75,100,125],
              'max_depth': [9,11,13,15,17]}

grid_search = GridSearchCV(rf, param_grid=param_grid, cv=10)
grid_search.fit(x_train, y_train)
print('RF Grid search best parameters', grid_search.best_params_)
print('RF Grid search best score', grid_search.best_score_)
print('RF Grid search results', grid_search.cv_results_)
print(' ')
'''
rf_best = RandomForestClassifier(n_estimators = 125, max_depth = 17)
rf_best.fit(x_train, y_train)
rf_best_y_pred = rf_best.predict(x_test)
rf_best_test_accuracy = accuracy_score(y_test, rf_best_y_pred.round())
print('Random Forest - best - test accuracy', rf_best_test_accuracy)
'''
# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
sc = StandardScaler()
x_train_scaled = sc.fit_transform(x_train)
x_test_scaled = sc.transform(x_test)

svc_base = SVC(gamma='auto')
svc_base.fit(x_train_scaled,y_train)
svc_y_pred = svc_base.predict(x_test_scaled)
svc_y_train = svc_base.predict(x_train_scaled)

svc_train_accuracy = accuracy_score(y_train, svc_y_train.round())
svc_test_accuracy = accuracy_score(y_test, svc_y_pred.round())
print('SVC train accuracy', svc_train_accuracy)
print('SVC test accuracy', svc_test_accuracy)
# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
svc_param_grid = [{'kernel':['linear'], 'C':[0.001, 0.01, 0.1,1,10,100]},{'kernel':['rbf'], 'C':[0.001,0.01,0.1,1,10,100]}]
svc_grid_search = GridSearchCV(svc_base, param_grid=svc_param_grid, cv=10)
svc_grid_search.fit(x_train_scaled, y_train)
print('SVC Grid search best parameters', svc_grid_search.best_params_)
print('SVC Grid search best score', svc_grid_search.best_score_)
print('SVC Grid search results', svc_grid_search.cv_results_)
print('  ')

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX


# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX
pca = PCA(n_components = 10, svd_solver = 'full')
pca.fit(x_train)
print('Explained variance', pca.explained_variance_ratio_)
print('Singular values', pca.singular_values_)

