# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import datetime
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
from Clean import chennai_house_df
import sklearn

df = chennai_house_df.copy()

# Select required columns

df = df[['AREA','BUILDING_AGE', 'INT_SQFT', 'DATE_SALE', 'DIST_MAINROAD', 'N_BEDROOM',
       'N_BATHROOM', 'N_ROOM', 'SALE_COND', 'PARK_FACIL', 'DATE_BUILD',
       'BUILDTYPE', 'UTILITY_AVAIL', 'STREET', 'MZZONE', 'QS_ROOMS',
       'QS_BATHROOM', 'QS_BEDROOM', 'QS_OVERALL', 'SALES_PRICE']]

X_cat = df.select_dtypes('object')
order_col = [list(df.groupby(i)['SALES_PRICE'].mean().sort_values(ascending=False).index) for i in X_cat.columns ]

# encode the columns
from sklearn.preprocessing import OrdinalEncoder
order = OrdinalEncoder(categories=order_col,dtype='int64')
X_cat_En = pd.DataFrame(order.fit_transform(X_cat),columns=order.get_feature_names_out())

X_cat_En1 = df[['N_BEDROOM','N_BATHROOM','N_ROOM']]

y = df['SALES_PRICE']

X_num = df.select_dtypes(['int32','int64','float'])
X_num.drop(columns=['N_BEDROOM','N_BATHROOM','N_ROOM'],inplace=True)

X_num = X_num[['INT_SQFT','BUILDING_AGE']]

from sklearn.preprocessing import StandardScaler
Scale = StandardScaler()
X_num_en = pd.DataFrame(Scale.fit_transform(X_num),columns=Scale.get_feature_names_out())

ml_df = pd.concat([X_cat_En,X_cat_En1,X_num_en],axis=1)

print(ml_df)
print('Data proceed for machine learning')

