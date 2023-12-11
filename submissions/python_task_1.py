#!/usr/bin/env python
# coding: utf-8

# In[49]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# # Q1: Car Matrix Generation
# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# values from id_2 as columns
# values from id_1 as index
# dataframe should have values from car column
# diagonal values should be 0.

# In[50]:


df=pd.read_csv('dataset-1-mapup.csv')
df


# In[51]:


df.info()


# In[52]:


df.describe()


# In[53]:


df.isnull().sum()


# In[54]:


generate_car_matrix= df.pivot(index='id_1',columns='id_2',values='car')
generate_car_matrix


# In[55]:


generate_car_matrix.isnull().sum()


# In[56]:


generate_car_matrix.fillna(0,inplace=True)   # replacing the null values with 0

Below is the answer as required - id_1 as index, id_2 as column and dataframe having values from car column and diagonal values are 0.  
# In[57]:


generate_car_matrix


# # Question 2: Car Type Count Calculation
# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[58]:


df


# In[59]:


def categorize_cartype(x):
    if x <= 15:
        return 'low'
    elif x > 15 and x <= 25:
        return 'medium'
    else:
        return 'high'


# In[60]:


df['car_type'] = df['car'].apply(categorize_cartype)     #adding new column car_type based on values of the column car.
df


# In[61]:


get_type_count = df['car_type'].value_counts().sort_index().to_dict()

print(get_type_count)  

#count of occurrences for each car_type category in dictionary and sorting the dictionary alphabetically based on keys.


# # Question 3: Bus Count Index Retrieval
# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[62]:


df


# In[63]:


mean_bus=df['bus'].mean()        #mean value of the column 'bus'
mean_bus


# In[64]:


get_bus_indexes=df[df['bus'] > 2 * mean_bus].index.tolist()
get_bus_indexes.sort()    #returning the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.


# In[65]:


get_bus_indexes         


# # Question 4: Route Filtering
# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[97]:


df


# In[100]:


def filter_routes(df):
    # Calculate the average value of the 'truck' column
    avg_truck = df['truck'].mean()
    
    # Filter the 'route' column based on the condition
    filtered_routes = df[df['truck'] > 7]['route'].tolist()
    
    # Sort and return the unique values of the 'route' column
    return sorted(set(filtered_routes))


# In[101]:


# Call the function with the required dataset
result = filter_routes(df)
print(result)


# In[ ]:





# In[ ]:





# # Question 5: Matrix Value Modification
# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[80]:


req_dataframe=generate_car_matrix


# In[81]:


def modify_value(n):                     #writing a function to meet the conditions given in the question
    if n > 20:
        return round(n * 0.75, 1)
    else:
        return round(n * 1.25, 1)


# In[82]:


multiply_matrix = req_dataframe.applymap(modify_value)     #applying the above function created on the required dataframe to get the correct outcome


# In[83]:


multiply_matrix


# # Question 6: Time Check
# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[145]:


df2=pd.read_csv('dataset-2-mapup.csv')
df2.head()


# In[146]:


df2.info()


# In[147]:


df2.describe()


# In[148]:


day_to_int = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

df2['startDay'] = df2['startDay'].map(day_to_int)
df2['endDay'] = df2['endDay'].map(day_to_int)


# In[149]:


df2['startDay'] = pd.to_datetime(df2['startDay'], unit='D')
df2['endDay'] = pd.to_datetime(df2['endDay'], unit='D')
df2


# In[152]:


df2['startTime']=pd.to_datetime(df2['startTime'])
df2['endTime']=pd.to_datetime(df2['endTime'])
df2.info()


# In[153]:


def verify_timestamp_completeness(df2):
    # Combine date and time columns to create timestamp columns
    df2['start_timestamp'] =df2['startDay'] + '' + df2['startTime']
    df2['end_timestamp'] = df2['endDay'] + '' + df2['endTime']
    
    # Calculate the duration of each timestamp
    df2['duration'] = df2['end_timestamp'] - df2['start_timestamp']
    
    # Function to check completeness for each (id, id_2) pair
    def check_completeness(group):
        return (
            (group['duration'].min() >= pd.Timedelta(days=7)) and
            (group['start_timestamp'].dt.time.min() == pd.Timestamp('00:00:00').time()) and
            (group['end_timestamp'].dt.time.max() == pd.Timestamp('23:59:59').time())
        )
    
    # Group by 'id' and 'id_2' and check completeness
    completeness_check = df2.groupby(['id', 'id_2']).apply(check_completeness)
    
    return completeness_check


# In[ ]:




