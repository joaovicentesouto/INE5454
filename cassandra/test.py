import pandas as pd
import numpy as np 

data = pd.read_csv("mnt/test.csv")

# print(data.head())

data.loc[data.index.max()+1] = ['abb', np.nan, 'add', 44]

print(data.head())
