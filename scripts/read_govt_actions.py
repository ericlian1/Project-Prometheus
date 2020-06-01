import numpy as np
import os, glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('jhu_covid19.csv',parse_dates=['dt'])
tests = pd.read_csv('testing per state.csv')
# mob = pd.read_csv('Global_Mobility_Report.csv',parse_dates=['date'])
# d = pd.read_csv('states_abbr.csv')
# d = dict(zip(d[' NAME'].str.lstrip(" ").str.replace("\"",""),d['ABBREVIATION']))


# mob.rename(columns={'date':'dt','sub_region_1':'state_n','sub_region_2':'county'},inplace=True)
# mob = mob[mob.country_region_code=='US'].dropna(subset=['state_n'])
# mob['county'] = mob.county.str.rstrip(" County")
# mob['state'] = mob['state_n'].map(d)

# mob_state = mob[mob.county.isnull()]
# mob_state.drop(columns=['country_region','country_region_code','state_n'],inplace=True)

# dc = mob[mob.state_n=='District of Columbia']
# dc['county'] = dc['state_n'].values

# mob = pd.concat([dc,mob.dropna(subset=['county'])])
# # mob.drop(columns=['country_region','country_region_code','state_n'],inplace=True)

# mob_state.set_index(['state','dt'],inplace=True)
# mob.set_index(['state','dt'],inplace=True)
# mob.update(mob_state,overwrite=False)
# print(mob)

# c = [i for i in mob_state.columns.tolist() if i not in ['state','county','dt']]
# # for i in c:
# #     df[i] = ""

# df2 = pd.merge(df.drop(columns=c),mob_state,on=['state','dt'])
# df2 = df2.groupby(['state','dt']).mean()
# #df2.set_index(['state','dt'],inplace=True)
# df.set_index(['state','dt'],inplace=True)
# df.update(df2,overwrite=False)
# df.to_csv('jhu_covid19_m2.csv')
# print(df.columns)
# govt = pd.read_csv('govt_actions.csv',parse_dates=['Effective Date','Expiration Date'])
# govt.rename(columns={'State':'state'},inplace=True)
# govt.drop(columns=['Source','Notes','State (Full Name)'],inplace=True)

# policy = govt.groupby('Policy')

# for name,group in policy:
#     print(name)
#     if "Status" in name:
#         d = dict(zip(group.state,group.Status))
#         df[name] = df.state.map(d)
#     else:
#         print('start')
#         df = pd.merge(df,group[['state','Effective Date','Expiration Date']],on='state')
#         df[name] = (df['dt'] > df['Effective Date']) & ((df['dt'] < df['Expiration Date']) | df['Expiration Date'].isnull())
#         df.drop(columns=['Effective Date','Expiration Date'],inplace=True)
#         print('end')
# print(df)
df.to_csv('jhu_covid19_g.csv',index=None)