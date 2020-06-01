import os, glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('jhu_covid19.csv',parse_dates=['dt'])
df.set_index(['state','county'],inplace=True)
d = pd.read_csv('states_abbr.csv')
d = dict(zip(d[' NAME'].str.lstrip(" ").str.replace("\"",""),d['ABBREVIATION']))

# # socioeconomic data
socioeconomic_file = "2020 County Health Rankings Data - v1.xlsx"
socioeconomic_df1 = pd.read_excel(io=socioeconomic_file,sheet_name="Additional Measure Data", header=1,
               usecols="B, C, D, CG, EJ, FB, IL,IQ, IS, IV, IW, IY, JA, JC, JJ")
socioeconomic_df2 = pd.read_excel(io=socioeconomic_file,sheet_name="Ranked Measure Data", header=1,
    usecols="B,C,GV, X, DG, EE, EQ, BD, BH, BL, GY")

socioeconomic_df1.rename(columns = {'State':'state_name', 'County':'county'}, inplace=True)
socioeconomic_df2.rename(columns = {'State':'state_name', 'County':'county'}, inplace=True)

socioeconomic_df1['state'] = socioeconomic_df1['state_name'].map(d)
socioeconomic_df2['state'] = socioeconomic_df2['state_name'].map(d)

s1state = socioeconomic_df1[socioeconomic_df1['county'].isnull()].set_index('state')
s2state = socioeconomic_df2[socioeconomic_df2['county'].isnull()].set_index('state')

print(s2state)
socioeconomic_df1 = socioeconomic_df1.dropna(subset=['county'])
socioeconomic_df2 = socioeconomic_df2.dropna(subset=['county'])

socioeconomic_df1.set_index(['state','county'],inplace=True)
socioeconomic_df2.set_index(['state','county'],inplace=True)

# #    print('\n socioeconomic_df.head()')
# #    print(socioeconomic_df.head())
# #old_df = df.copy().reset_index()
df = pd.merge(df, socioeconomic_df1.drop(columns=['state_name']), on=['state', 'county'])
# print(df.index)
# statemerged = pd.merge(old_df,s1state,on=['state'])
# statemerged.set_index('state',inplace=True)
# df.reset_index(level='county',inplace=True)

# df.set_index('county',append=True,inplace=True)

df = pd.merge(df, socioeconomic_df2.drop(columns=['state_name']), on=['state', 'county'])

df = df.reset_index()
df = df.set_index('state')
df.update(s1state.drop(columns=['state_name','county']),overwrite=False)
df.update(s2state.drop(columns=['state_name','county']),overwrite=False)
print(df)
n = 'Primary Care Physicians Ratio'
df[n] = df[n].replace({'':np.nan})
print(df[n])
df[n] = pd.to_numeric(df[n].str.rstrip(':1'),errors='coerce')

# df = df.reset_index()
# df.to_csv('jhu_covid19_socio.csv',index=['state','county'])
# statemerged.set_index('state',inplace=True)
# df.reset_index(level='county',inplace=True)
# df.update(statemerged,overwrite=False)
# df.set_index('county',append=True,inplace=True)
#    print('\n merged df.head():')
#    print(df.head())

df.to_csv('jhu_covid19_socio.csv')