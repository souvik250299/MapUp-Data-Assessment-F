#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# # Question 1: Distance Matrix Calculation
# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[29]:


df=pd.read_csv('dataset-3-mapup.csv')
df.head()


# In[30]:


df.info()


# In[31]:


df.describe()


# In[32]:


# Creating a DataFrame with unique toll locations
unique_locations = sorted(set(df['id_start']).union(set(df['id_end'])))

# Creating an empty matrix with rows and columns labeled with unique toll locations
calculate_distance_matrix = pd.DataFrame(index=unique_locations, columns=unique_locations)
calculate_distance_matrix = calculate_distance_matrix.fillna(0)  # Initialize all values to 0


# In[33]:


for index, row in df.iterrows():
    calculate_distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
    calculate_distance_matrix.at[row['id_end'], row['id_start']] = row['distance']  # Ensure symmetry


# In[34]:


# Calculating cumulative distances for indirect routes
for via in unique_locations:
    for start in unique_locations:
        for end in unique_locations:
            if start != end and calculate_distance_matrix.at[start, via] != 0 and calculate_distance_matrix.at[via, end] != 0:
                if calculate_distance_matrix.at[start, end] == 0 or calculate_distance_matrix.at[start, end] > calculate_distance_matrix.at[start, via] + calculate_distance_matrix.at[via, end]:
                    calculate_distance_matrix.at[start, end] = calculate_distance_matrix.at[start, via] + calculate_distance_matrix.at[via, end]


# In[35]:


for loc in unique_locations:
    calculate_distance_matrix.at[loc, loc] = 0


# In[36]:


calculate_distance_matrix


# # Question 2: Unroll Distance Matrix
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[37]:


import itertools

# Initialize an empty list to store the unrolled data
unrolled_data = []


# In[38]:


# Iterating through the distance matrix
for idstart, row in calculate_distance_matrix.iterrows():
    for idend, distance in row.iteritems():
        # Skip cases where idstart and idend are the same or distance is 0
        if idstart != idend and distance != 0:
            unrolled_data.append({'id_start': idstart, 'id_end': idend, 'distance': distance})


# In[39]:


# Creating a DataFrame from the unrolled data
unroll_distance_matrix = pd.DataFrame(unrolled_data)

unroll_distance_matrix


# # Question 3: Finding IDs within Percentage Threshold
# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[58]:


def find_ids_within_ten_percentage_threshold(unroll_distance_matrix, reference_value):
    # Filter DataFrame rows with the given reference value as id_start
    reference_data = unroll_distance_matrix[unrolled_df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    average_distance = reference_data['distance'].mean()

    # Calculate the threshold values (10% above and below the average distance)
    threshold_upper = average_distance + (0.1 * average_distance)
    threshold_lower = average_distance - (0.1 * average_distance)

    # Filter id_start values within the threshold range
    ids_within_threshold = unrolled_df[(unroll_distance_matrix['distance'] >= threshold_lower) & (unroll_distance_matrix['distance'] <= threshold_upper)]
    unique_ids_within_threshold = sorted(ids_within_threshold['id_start'].unique())

    return unique_ids_within_threshold


# # Question 4: Calculate Toll Rate
# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for moto
# 1.2 for car
# 1.5 for rv
# 2.2 for bus
# 3.6 for truck
# 

# In[56]:


def calculate_toll_rate(unroll_distance_matrix):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type without showing the distance column
    for vehicle_type, rate in rate_coefficients.items():
        unroll_distance_matrix[vehicle_type] = unroll_distance_matrix['distance'] * rate

    # Droping the 'distance' column (since the resulting dataframe given doesn't have the distance column)
    unroll_distance_matrix = unroll_distance_matrix.drop(columns=['distance'])

    return unroll_distance_matrix


# In[57]:


result_df = calculate_toll_rate(unroll_distance_matrix)
result_df


# # Question 5: Calculate Time-Based Toll Rates
# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[ ]:


import pandas as pd
import datetime

# Function to calculate toll rates based on time intervals
def calculate_toll_rates(row):
    # Weekdays (Monday - Friday)
    if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        if datetime.time(0, 0, 0) <= row['start_time'] < datetime.time(10, 0, 0):
            return row['vehicle'] * 0.8
        elif datetime.time(10, 0, 0) <= row['start_time'] < datetime.time(18, 0, 0):
            return row['vehicle'] * 1.2
        else:
            return row['vehicle'] * 0.8
    # Weekends (Saturday and Sunday)
    else:
        return row['vehicle'] * 0.7

# Creating a time range for a full 24-hour period
time_range = pd.date_range('2023-01-01', periods=24, freq='H').time

# Generating rows for each unique (id_start, id_end) pair and time intervals
full_data = []
for _, row in result_df.iterrows():
    for day in range(7):
        for i in range(len(time_range) - 1):
            full_data.append({
                'id_start': row['id_start'],
                'id_end': row['id_end'],
                'distance': row['distance'],
                'vehicle': calculate_toll_rates(row),
                'start_day': datetime.date(2023, 1, 1 + day).strftime('%A'),
                'start_time': time_range[i],
                'end_day': datetime.date(2023, 1, 1 + day).strftime('%A'),
                'end_time': time_range[i + 1]
            })

# Creating a new DataFrame with the expanded dataset
expanded_result_df = pd.DataFrame(full_data)

print(expanded_result_df)

