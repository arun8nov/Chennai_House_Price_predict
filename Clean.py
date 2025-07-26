import pandas as pd
df = pd.read_csv("Chennai houseing sale.csv")
mask = df.QS_OVERALL.isna()
df.loc[mask,'QS_OVERALL'] = df.loc[mask,['QS_ROOMS','QS_BATHROOM','QS_BEDROOM']].mean(axis=1)
df.dropna(inplace=True)
df.AREA.replace({
    'Adyar' : 'Adayar',
    'Chrompt' : 'Chrompet',
    'Chrmpet' : 'Chrompet',
    'Chormpet' : 'Chrompet',
    'Karapakam' : 'Karapakkam',
    'Ana Nagar' : 'Anna Nagar',
    'Velchery' : 'Velachery',
    'Ann Nagar' : 'Anna Nagar',
    'Adyr' : 'Adayar',
    'KKNagar' : 'KK Nagar',
    'TNagar' : 'T Nagar'
}, inplace = True)
df.DATE_SALE = pd.to_datetime(df.DATE_SALE,format='%d-%m-%Y')

df['SALE_YEAR'] = df.DATE_SALE.dt.year
df['SALE_MONTH'] = df.DATE_SALE.dt.month
df['SALE_MONTH_NAME'] = df.DATE_SALE.dt.month_name()
df['SALE_DAY'] = df.DATE_SALE.dt.day
df['SALE_DAY_OF_WEEK'] = df.DATE_SALE.dt.dayofweek
df['SALE_DAY_NAME'] = df.DATE_SALE.dt.day_name()
df['SALE_QUARTER'] = df.DATE_SALE.dt.quarter

df.SALE_COND.replace({
    'Adj Land' : 'AdjLand',
    'Ab Normal' : 'AbNormal',
    'Partiall' : 'Partial',
    'PartiaLl' : 'Partial'
},inplace=True)

df.PARK_FACIL.replace('Noo','No',inplace=True)

df.DATE_BUILD =pd.to_datetime(df.DATE_BUILD,format='%d-%m-%Y')

df['BUILD_YEAR'] = df.DATE_BUILD.dt.year
df['BUILD_MONTH'] = df.DATE_BUILD.dt.month
df['BUILD_MONTH_NAME'] = df.DATE_BUILD.dt.month_name()
df['BUILD_DAY'] = df.DATE_BUILD.dt.day
df['BUILD_DAY_OF_WEEK'] = df.DATE_BUILD.dt.dayofweek
df['BUILD_DAY_NAME'] = df.DATE_BUILD.dt.day_name()
df['BUILD_QUARTER'] = df.DATE_BUILD.dt.quarter

df.BUILDTYPE.replace({
    'Other': 'Others',
    'Comercial' : 'Commercial'
},inplace= True)

df.UTILITY_AVAIL.replace({
    'All Pub' : 'AllPub'

},inplace=True)

df.STREET.replace({
    'Pavd' : 'Paved',
    'NoAccess' : 'No Access'
},inplace=True)

df['BUILDING_AGE'] = df.SALE_YEAR - df.BUILD_YEAR

df.reset_index(drop=True,inplace=True)

chennai_house_df = df.copy()

print(chennai_house_df.head())

print("Chennai House data processed successfully")