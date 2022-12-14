# -*- coding: utf-8 -*-
"""stock_price_pred_06_10_2022_22_50

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PpN4dcaf2hLt6EJndqcQ74tMZkpv2kvg
"""

pip install catboost

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn.utils.fixes import sp
pd.set_option('display.max_columns', None)

data_learn = pd.read_hdf('/content/drive/MyDrive/Colab Notebooks/sample_dataset.h5', sep = ',')

data_learn.rename(columns = {'Unnamed: 198_level_1':'y'}, inplace = True)


X= data_learn[['BID0',
   'BID1',
   'BID2',
   'BID3',
   'BID4',
   'VBID0',
   'VBID1',
   'VBID2',
   'VBID3',
   'VBID4',
   'ASK0',
   'ASK1',
   'ASK2',
   'ASK3',
   'ASK4',
   'VASK0',
   'VASK1',
   'VASK2',
   'VASK3',
   'VASK4',
   'PTRADE',
   'VTRADE']].copy()
X[('index',  'num')] = X.index




y = data_learn['y'].copy()

shift_num = 10

y = ((y.shift(shift_num)).loc[y.index>shift_num - 1]).reset_index()
y.pop('index')

X = (X.loc[X.index > shift_num - 1].copy()).reset_index()
X.pop('level_0')

X['y_shift1'] = y.shift(1)
X['y_shift2'] = y.shift(2)
X['y_shift3'] = y.shift(3)
X['y_shift4'] = y.shift(4)

i = 5
while i < len(X):
  if X.loc[i,'y_shift1'][0] < 0:
    X.loc[i,'pos_ind_y_shift1'] = 0
  elif X.loc[i,'y_shift1'][0] == 0:  
    X.loc[i,'pos_ind_y_shift1'] = 1
  else: X.loc[i,'pos_ind_y_shift1'] = 2

  
  if X.loc[i,'y_shift2'][0] < 0:
    X.loc[i,'pos_ind_y_shift2'] = 0
  elif X.loc[i,'y_shift2'][0] == 0:  
    X.loc[i,'pos_ind_y_shift2'] = 1
  else: X.loc[i,'pos_ind_y_shift2'] = 2

  if X.loc[i,'y_shift3'][0] < 0:
    X.loc[i,'pos_ind_y_shift3'] = 0
  elif X.loc[i,'y_shift3'][0] == 0:  
    X.loc[i,'pos_ind_y_shift3'] = 1
  else: X.loc[i,'pos_ind_y_shift3'] = 2

  if X.loc[i,'y_shift4'][0] < 0:
    X.loc[i,'pos_ind_y_shift4'] = 0
  elif X.loc[i,'y_shift4'][0] == 0:  
    X.loc[i,'pos_ind_y_shift4'] = 1
  else: X.loc[i,'pos_ind_y_shift4'] = 2
  
  i+=1

j = 15
while j < len(X):
  X.loc[j,'avg_y_shift1_10'] = (X.loc[j-1,'y_shift1'][0]+X.loc[j-2,'y_shift1'][0]+X.loc[j-3,'y_shift1'][0]+X.loc[j-4,'y_shift1'][0]+X.loc[j-5,'y_shift1'][0]+X.loc[j-6,'y_shift1'][0]+X.loc[j-7,'y_shift1'][0]+X.loc[j-8,'y_shift1'][0]+X.loc[j-9,'y_shift1'][0]+X.loc[j-10,'y_shift1'][0])/10
  X.loc[j,'avg_y_shift1_5'] = (X.loc[j-1,'y_shift1'][0]+X.loc[j-2,'y_shift1'][0]+X.loc[j-3,'y_shift1'][0]+X.loc[j-4,'y_shift1'][0]+X.loc[j-5,'y_shift1'][0])/5
  X.loc[j,'avg_y_shift1_2'] = (X.loc[j-1,'y_shift1'][0]+X.loc[j-2,'y_shift1'][0])/2


  X.loc[j,'avg_y_shift2_10'] = (X.loc[j-1,'y_shift2'][0]+X.loc[j-2,'y_shift2'][0]+X.loc[j-3,'y_shift2'][0]+X.loc[j-4,'y_shift2'][0]+X.loc[j-5,'y_shift2'][0]+X.loc[j-6,'y_shift2'][0]+X.loc[j-7,'y_shift2'][0]+X.loc[j-8,'y_shift2'][0]+X.loc[j-9,'y_shift2'][0]+X.loc[j-10,'y_shift2'][0])/10  
  X.loc[j,'avg_y_shift2_5'] = (X.loc[j-1,'y_shift2'][0]+X.loc[j-2,'y_shift2'][0]+X.loc[j-3,'y_shift2'][0]+X.loc[j-4,'y_shift2'][0]+X.loc[j-5,'y_shift2'][0])/5
  X.loc[j,'avg_y_shift2_2'] = (X.loc[j-1,'y_shift2'][0]+X.loc[j-2,'y_shift2'][0])/2

  X.loc[j,'avg_pos_ind_y_shift1_10'] = (X.loc[j-1,'pos_ind_y_shift1'][0] + X.loc[j-2,'pos_ind_y_shift1'][0] + X.loc[j-3,'pos_ind_y_shift1'][0] + X.loc[j-4,'pos_ind_y_shift1'][0]+ X.loc[j-5,'pos_ind_y_shift1'][0]+ X.loc[j-6,'pos_ind_y_shift1'][0]+ X.loc[j-7,'pos_ind_y_shift1'][0]+ X.loc[j-8,'pos_ind_y_shift1'][0]+ X.loc[j-9,'pos_ind_y_shift1'][0]+ X.loc[j-10,'pos_ind_y_shift1'][0])/10
  X.loc[j,'avg_pos_ind_y_shift1_5'] = (X.loc[j-1,'pos_ind_y_shift1'][0] + X.loc[j-2,'pos_ind_y_shift1'][0] + X.loc[j-3,'pos_ind_y_shift1'][0] + X.loc[j-4,'pos_ind_y_shift1'][0]+ X.loc[j-5,'pos_ind_y_shift1'][0])/5
  X.loc[j,'avg_pos_ind_y_shift1_2'] = (X.loc[j-1,'pos_ind_y_shift1'][0] + X.loc[j-2,'pos_ind_y_shift1'][0])/2

  X.loc[j,'avg_pos_ind_y_shift2_10'] = (X.loc[j-1,'pos_ind_y_shift2'][0] + X.loc[j-2,'pos_ind_y_shift2'][0] + X.loc[j-3,'pos_ind_y_shift2'][0] + X.loc[j-4,'pos_ind_y_shift2'][0]+ X.loc[j-5,'pos_ind_y_shift2'][0]+ X.loc[j-6,'pos_ind_y_shift2'][0]+ X.loc[j-7,'pos_ind_y_shift2'][0]+ X.loc[j-8,'pos_ind_y_shift2'][0]+ X.loc[j-9,'pos_ind_y_shift2'][0]+ X.loc[j-10,'pos_ind_y_shift2'][0])/10
  X.loc[j,'avg_pos_ind_y_shift2_5'] = (X.loc[j-1,'pos_ind_y_shift2'][0] + X.loc[j-2,'pos_ind_y_shift2'][0] + X.loc[j-3,'pos_ind_y_shift2'][0] + X.loc[j-4,'pos_ind_y_shift2'][0]+ X.loc[j-5,'pos_ind_y_shift2'][0])/5
  X.loc[j,'avg_pos_ind_y_shift2_2'] = (X.loc[j-1,'pos_ind_y_shift2'][0] + X.loc[j-2,'pos_ind_y_shift2'][0])/2

  j +=1

X = X.loc[X.index >=15].reset_index()
X.pop('level_0')
y = y.loc[y.index >=15].reset_index()
y.pop('index')


def cross_valid_data(X,y,k):
  X_train = []
  y_train = []
  X_test = []
  y_test = []
  i = 0

  while i <k:
    X_train.append(X.loc[(X.index < len(y) - shift_num - i)])
    X_test.append(X.loc[(X.index >= len(y) - shift_num - i)*(X.index < len(y) - i)])

    y_train.append(y.loc[(y.index < len(y) - shift_num - i)])
    y_test.append(y.loc[(y.index >= len(y) - shift_num - i)*(X.index < len(y) - i)])

    i +=1
  
  return   X_train, y_train, X_test, y_test

def prediction(X,y,k,n_estimators, learning_rate):
  splitted = cross_valid_data(X,y,k)
  model = CatBoostRegressor(eval_metric = 'MAE',  n_estimators = n_estimators, learning_rate = learning_rate, random_seed = 1)

  predictions = []
  real_qty = []


  mae = []
  mape = []
  r2 = []
  spearmanr = []

  for i in range(0, k):
    model.fit(splitted[0][i], splitted[1][i])
    
    predictions.append(model.predict(splitted[2][i]))
    real_qty.append(splitted[3][i])

    mae.append(mean_absolute_error(predictions[i], splitted[3][i]))
    mape.append(mean_absolute_percentage_error(predictions[i], splitted[3][i]))
    r2.append(r2_score(predictions[i], splitted[3][i]))
    spearmanr.append(stats.spearmanr(predictions[i], splitted[3][i]))

  return predictions, real_qty, mae, mape, r2, spearmanr

aa = prediction(X,y,5,1000,0.1)

print('MAE: ', aa[2])

print('MAPE: ', aa[3])

print('R2: ', aa[3])

print('Spearmanr: ', aa[4])

