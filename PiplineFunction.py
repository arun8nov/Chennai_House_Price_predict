import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import datetime
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import sklearn
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

class Chennai_House:

    def __init__(self):
        pass

    def Data_Clean(self, df):
        mask = df.QS_OVERALL.isna()
        df.loc[mask, 'QS_OVERALL'] = df.loc[mask, ['QS_ROOMS', 'QS_BATHROOM', 'QS_BEDROOM']].mean(axis=1)
        df.dropna(inplace=True)
        df.AREA.replace({
            'Adyar': 'Adayar',
            'Chrompt': 'Chrompet',
            'Chrmpet': 'Chrompet',
            'Chormpet': 'Chrompet',
            'Karapakam': 'Karapakkam',
            'Ana Nagar': 'Anna Nagar',
            'Velchery': 'Velachery',
            'Ann Nagar': 'Anna Nagar',
            'Adyr': 'Adayar',
            'KKNagar': 'KK Nagar',
            'TNagar': 'T Nagar'
        }, inplace=True)
        df.DATE_SALE = pd.to_datetime(df.DATE_SALE, format='%d-%m-%Y')

        df['SALE_YEAR'] = df.DATE_SALE.dt.year
        df['SALE_MONTH'] = df.DATE_SALE.dt.month
        df['SALE_MONTH_NAME'] = df.DATE_SALE.dt.month_name()
        df['SALE_DAY'] = df.DATE_SALE.dt.day
        df['SALE_DAY_OF_WEEK'] = df.DATE_SALE.dt.dayofweek
        df['SALE_DAY_NAME'] = df.DATE_SALE.dt.day_name()
        df['SALE_QUARTER'] = df.DATE_SALE.dt.quarter

        df.SALE_COND.replace({
            'Adj Land': 'AdjLand',
            'Ab Normal': 'AbNormal',
            'Partiall': 'Partial',
            'PartiaLl': 'Partial'
        }, inplace=True)

        df.PARK_FACIL.replace('Noo', 'No', inplace=True)

        df.DATE_BUILD = pd.to_datetime(df.DATE_BUILD, format='%d-%m-%Y')

        df['BUILD_YEAR'] = df.DATE_BUILD.dt.year
        df['BUILD_MONTH'] = df.DATE_BUILD.dt.month
        df['BUILD_MONTH_NAME'] = df.DATE_BUILD.dt.month_name()
        df['BUILD_DAY'] = df.DATE_BUILD.dt.day
        df['BUILD_DAY_OF_WEEK'] = df.DATE_BUILD.dt.dayofweek
        df['BUILD_DAY_NAME'] = df.DATE_BUILD.dt.day_name()
        df['BUILD_QUARTER'] = df.DATE_BUILD.dt.quarter

        df.BUILDTYPE.replace({
            'Other': 'Others',
            'Comercial': 'Commercial'
        }, inplace=True)

        df.UTILITY_AVAIL.replace({
            'All Pub': 'AllPub'
        }, inplace=True)

        df.STREET.replace({
            'Pavd': 'Paved',
            'NoAccess': 'No Access'
        }, inplace=True)

        df['BUILDING_AGE'] = df.SALE_YEAR - df.BUILD_YEAR

        df.reset_index(drop=True, inplace=True)
        for i in df.columns:
            if df[i].dtype == 'object':
                df[i] = df[i].str.lower()

        df.columns = [i.lower() for i in df.columns]

        return df

    # This is the single, corrected Data_Selection method
    def Data_Selection(self, df):
        df = df[['area', 'building_age', 'int_sqft', 'date_sale', 'dist_mainroad', 'n_bedroom',
                 'n_bathroom', 'n_room', 'sale_cond', 'park_facil', 'date_build',
                 'buildtype', 'utility_avail', 'street', 'mzzone', 'qs_rooms',
                 'qs_bathroom', 'qs_bedroom', 'qs_overall', 'sales_price']]

        X_cat = df.select_dtypes('object')

        X_cat_En1 = df[['n_bedroom', 'n_bathroom', 'n_room']]

        X_num = df.select_dtypes(['int32', 'int64', 'float'])
        X_num = X_num[['int_sqft', 'building_age']]


        y = df[['sales_price']]
        
        order_col = [list(df.groupby(i)['sales_price'].mean().sort_values(ascending=False).index) for i in X_cat.columns]

        return X_cat, X_cat_En1, X_num, y,order_col

    def Cat_Encoding(self, df):
        # Correctly call the Data_Selection method using 'self'
        X_cat= self.Data_Selection(df)[0]
        order_col = [list(df.groupby(i)['sales_price'].mean().sort_values(ascending=False).index) for i in X_cat.columns]
        order = OrdinalEncoder(categories=order_col, dtype='int64')
        X_cat_En = pd.DataFrame(order.fit_transform(X_cat), columns=order.get_feature_names_out())
        return X_cat_En,order_col

    def Num_Scaling(self, df):
        # Correctly call the Data_Selection method using 'self'
        X_num= self.Data_Selection(df)[2]
        Scale = StandardScaler()
        X_num_en = pd.DataFrame(Scale.fit_transform(X_num), columns=Scale.get_feature_names_out())
        for i in X_num_en.columns:
            X_num_en[i] = X_num_en[i].round(2)
        return X_num_en