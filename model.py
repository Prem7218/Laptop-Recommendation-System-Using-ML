import pandas as pd
import numpy as np

# File :- https://www.kaggle.com/datasets/bhavikjikadara/brand-laptops-dataset
# Downlod File From Above...
#
# <!-- Model Code -->
#
# ```

# -*- coding: utf-8 -*-
"""Laptop_Data_Model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZhbTKFRLk7CW_uL3nQQUvSSs1NI-TAtv
"""


laptops = pd.read_csv('laptops.csv')

laptops.shape

laptops.head(1)

laptops['Model'][0]

# Remove Col.
# ratings ,num_cores, num_threads, secondary_Memory_Capacity, gpu_type, gpu_brand, resolution_height, resolution_width...

# IMP Col.
# Model, price, Processor_brand, processor_type, ram_memory, ssd, touch_screen, display_size, warrenty.

laptops.info()

laptops1 = laptops[['brand','Model','Price','processor_brand','processor_tier','ram_memory','secondary_storage_capacity','is_touch_screen','display_size','year_of_warranty']]

laptops1.columns = ['Brand','Model','Price','Process_Brand','Process_Type','Ram','SSD_Size','Touch_Screen','Display_size','Warrenty']

laptops1.head(1)

laptops1.isnull().sum()

laptops1.duplicated().sum()

laptops1['Model'][0]


def transform_record(record):
    words = record.split()
    return [' '.join(words[:2])]


laptops1['Model'] = [transform_record(record) for record in laptops1['Model']]

laptops1['Model'] = laptops1['Model'].apply(lambda x:[i.replace(" ","") for i in x])

laptops1.head(1)

laptops1['Processer'] = laptops1['Process_Brand'] + laptops1['Process_Type']

laptops1.head(1)

laptops2 = laptops1[['Brand','Model','Price','Process_Brand','Ram','SSD_Size','Touch_Screen','Display_size','Warrenty']]

laptops2.info()

laptops2['Brand'] = laptops2['Brand'].apply(lambda x:x.lower())

laptops2['Process_Brand'] = laptops2['Process_Brand'].apply(lambda x:x.lower())

laptops2.head(1)

import matplotlib.pyplot as plt

plt.bar(laptops2['Brand'][:6],laptops2['Price'][:6])

final_laptops = laptops2.sort_values(by='Price', ascending=True)


def recommend(price):
    affordable_laptops = final_laptops[final_laptops['Price'] <= price]
    i = 0
    for index, row in affordable_laptops.iterrows():
      if i != 10:
        print(row,"\n\n")
        i+=1
        plt.scatter(row['Brand'],row['Price'])
      else:
        break

import pickle
pickle.dump(laptops2,open('laptops.pkl','wb'))



# ```