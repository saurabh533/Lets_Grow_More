# -*- coding: utf-8 -*-
"""Stock_Market STACKED LSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11u4qY3pVkJiB68N6SzpQFKt_e52j7m0K
"""

#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt



# In[40]:


data = pd.read_csv('/content/stock.csv')


# In[41]:


data


# In[24]:


close_data=data['Close']


# In[25]:


close_data


# In[35]:


# Convert dates to datetime objects
date_objects = pd.to_datetime(data['Date'])


# In[47]:


time = pd.DataFrame(date_objects)


# In[48]:


time


# In[57]:


# Create a line chart
plt.plot(time['Date'], data['Close'], marker='o', linestyle='-', color='r', label='Stocks')


plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('closing_price')
plt.title('Tata stock Trend Over Time')

plt.legend()

plt.tight_layout()
plt.show()


# In[58]:


import numpy as np


# In[61]:


from sklearn.preprocessing import MinMaxScaler
scalar = MinMaxScaler(feature_range=(0,1))
df1=scalar.fit_transform(np.array(close_data).reshape(-1,1))


# In[65]:


df1.shape


# In[67]:


print(df1)


# In[68]:


#Splitting data into train test split


# In[87]:


training_size = int(len(df1)*0.65)
test_size = len(df1)-training_size
train_data, test_data = df1[:training_size,:],df1[training_size:len(df1),:1]


# In[113]:


def create_dataset(dataset,time_step):
    dataX,dataY = [],[]
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step),0]
        dataX.append(a)
        dataY.append(dataset[i+time_step,0])
    return np.array(dataX),np.array(dataY)


# In[129]:


X_train,y_train=create_dataset(train_data,100)


# In[130]:


X_test,y_test=create_dataset(test_data,100)


# In[132]:


print(X_test.shape),print(y_test.shape)


# In[133]:


print(X_train.shape),print(y_train.shape)


# In[138]:


#reshape input to be [samples , time_step, features] which is required for LSTM
X_train =  X_train.reshape(X_train.shape[0],X_train.shape[1], 1)
X_test  =  X_test.reshape(X_test.shape[0],X_test.shape[1], 1)


# In[141]:


#create stacked LSTM model


# In[143]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM


# In[144]:


model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')


# In[146]:


model.summary()


# In[147]:


model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=100,batch_size=64,verbose=1)


# In[148]:




# In[ ]:

pwd

train_predict = model.predict(X_train)


# In[150]:


test_predict = model.predict(X_test)

train_predict

test_predict

len(y_train),len(train_predict)

len(y_test),len(test_predict)

#calculate RMSE values

import math

from sklearn.metrics import mean_squared_error

math.sqrt(mean_squared_error(y_train,train_predict))

math.sqrt(mean_squared_error(y_test,test_predict))

train_predict=scalar.inverse_transform(train_predict)
test_predict =scalar.inverse_transform(test_predict)

##plotting
#shift train prediction for plotting
look_back=100
trainPredictPlot = np.empty_like(df1)
trainPredictPlot[:,:] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back,:]=train_predict
#shift test predict
testPredictPlot = np.empty_like(df1)
testPredictPlot[:,:] = np.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1,:] = test_predict
#plot baseline and prediction
plt.plot(scalar.inverse_transform(df1))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

