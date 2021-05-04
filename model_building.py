# -*- coding: utf-8 -*-
"""
Created on Mon May  3 13:24:16 2021

@author: Nikhil DragNeel
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
df = pd.read_csv('eda_data.csv')

#A) choose relevant columns

df.columns

# df_custom_Model = df[['choose the columns you want']] <--- in this case it is already been done
df_model = df

#B) get dummy data
df_dum = pd.get_dummies(df_model)

#C) train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('avg_salary', axis = 1)
y = df_dum.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=12)

#D) multiple linear regression
# import statsmodel

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso

from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 5))

#from sklearn.metrics import SCORERS
# SCORERS.keys()
# sorted(sklearn.metrics,SCORERS.keys())
#cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error')
#cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 3)
#np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 3))

#E) lasso regression

lm_l = Lasso(alpha=5.98)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 5))

alpha = []
error = []

for i in range (1000):
    alpha.append(i/100)
    lml = Lasso(alpha = (i /100))
    # error.append(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 3))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error',cv = 5)))
plt.plot(alpha,error)

err= tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

#F) random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 5))

#G) tune models GridsearchCSV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,100,10),'criterion':('mse','mae'),'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error', cv = 5)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

#H) test ensembles
tpread_lm = lm.predict(X_test )
tpread_lml = lm_l.predict(X_test)
tpread_rf = gs.best_estimator_.predict(X_test)


from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, tpread_lm)
mean_absolute_error(y_test, tpread_lml)
mean_absolute_error(y_test, tpread_rf)

mean_absolute_error(y_test,(tpread_lm+tpread_rf)/2)

mean_absolute_error(y_test,(tpread_lml+tpread_rf)/2)









