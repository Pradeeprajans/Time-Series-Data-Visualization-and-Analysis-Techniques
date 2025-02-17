#!/usr/bin/env python
# coding: utf-8

# # WELCOME TO THE NOTEBOOK
# ---
# In this Notebook we are going to learn about different data visualization techniques for time series analysis. we will also discuss the different tasks we can consider for a better understanding, exploration and anlysis, while working with time series datasets.
# 
# the dataset: Average daily temprature of different cities around globe from 1995 to 2020 
# 
# 
# #### Agenda:
#     Task1: Importing our dataset 
#     Task2: Data Preprocessing
#     Task3: Analysing global temperature from 1995 to 2019
#     Task4: Comparing yearly average temperature of different regions over time
#     Task5: Monthly average temperature in Canada
# 
# ----

# Importing modules

# In[1]:


import pandas as pd 

import numpy as np 

import plotly.express as px 
import plotly.graph_objects as go
import matplotlib.pyplot as plt 

print("modules are imported!")


# In[ ]:





# Let's load our dataset

# In[2]:


data = pd.read_csv('dataset.csv')
data.head()


# The Dataset That we are going to work with is a ***Geo-Spatial Time-Series Dataset***
# 
# #### What is our dataset representing? 
# **Geo-Spatial**: Data represents that **Something** has happend **somewhere**! <br>
# **Time-Series**: Data represents that **Something** has happend **at a specific time**! <br>
# <br>
# **Geo-Spatial Time-Series Dataset**: Data represents that **Something** has happend **somewhere** **at a specific time**!
# 
# 
# ### Time Series tasks:
#     1- Overall Trend analysis
#     2- Key Moments
#     3- Outliers

# ## Task 2: Preprocessing

# #### Let's get only our needed columns

# In[7]:


needed_columns = ["Region","Country","City","Month","Day","Year","AvgTemperature"]
data = data[needed_columns]
data


# Let's convert fahrenheit to celsius

# In[12]:


data["AvgTemperature"]=round((data["AvgTemperature"] -32) * 5/9 , 1)
data.head()


# Let's find the outliers

# In[13]:


data["AvgTemperature"].hist()


# Removing the outliers 

# In[15]:


data = data[data.AvgTemperature > -40] 
data["AvgTemperature"].hist()


# sorting values by Year, Month and Day Column to see the time range of our data

# In[17]:


data.sort_values(['Year','Month','Day'])


# we don't have 2020 data completely, so let's just remove them from our dataset 

# In[18]:


data =data[data.Year < 2020]
data.sort_values(['Year','Month','Day'])


# ## Task 3: Global temperature from 1995 to 2019 
#     - Aggregating our data based on the year 
#     - plot our data in a line chart 

# In[23]:


data_agg=data[['Year',"AvgTemperature"]].groupby("Year").mean().reset_index()
data_agg.head()


# Let's draw a line chart for this data

# In[26]:


fig = px.line(data_agg,x="Year", y="AvgTemperature",title="Global Avg Temp 1995-2019")
fig.update_xaxes(dtick = "year")
fig.show()


# ### Time Series tasks:
#     1- Overall Trend analysis
#     2- Key Moments
#     3- Outliers

# ### Overall Trend Analysis
# Let's fit a linear line to our plot using numpy and Linear Regression 

# In[31]:


coef = np.polyfit(x = data_agg.Year, y= data_agg.AvgTemperature, deg = 1)
# y = mx + C
m = coef[0]
C = coef[1]

line = m * data_agg.Year +C
fig.add_trace(go.Scatter(x = data_agg.Year,y=line, name= 'Trend Line' ))
fig.show()


# 
# ### Bar chart vs Line chart
# Let's compare Bar chart and Line chart in terms of the tasks we can solve using each of them

# Time Series tasks:
# 
#     1- Overall trend analysis
#     2- Key Moments
#     3- Outliers

# Let's plot a bar chart for the same data

# In[34]:


px.bar(data_agg,x = "Year", y ="AvgTemperature",color ='AvgTemperature')


# ### Task 4: Let's compare yearly average temperature of different regions over time 

# In[39]:


data_regions=data[["Region",'Year',"AvgTemperature"]].groupby(["Region",'Year']).mean().reset_index()
data_regions


# In[43]:


fig1 = px.line(data_regions,x="Year",y="AvgTemperature",color="Region")
fig1.update_xaxes(dtick="Year")
fig1.show()


# ### Task 5: Monthly average temperature in Canada

# In[52]:


data_canada = data[data.Country == "Canada"][['Month',"Year","AvgTemperature"]]
data_canada = data_canada.groupby(['Month',"Year"]).mean().reset_index()

data_canada


# Creating a date column with this format ***MONTH/YEAR***

# In[55]:


data_canada.Month = data_canada.Month.astype(str)
data_canada.Year = data_canada.Year.astype(str)

data_canada["Date"]=data_canada.Month + '/' + data_canada.Year
data_canada.head()


# Let's plot a bar chart to analyse this data

# In[57]:


fig = px.bar(data_canada, x ="Date", y = "AvgTemperature",color = 'Month')
fig.show()


# ### Let's use a Box Plot for analyzing the same data

# In[59]:


px.box(data_canada, x ='Month', y="AvgTemperature", color= "Month")


# In[ ]:




