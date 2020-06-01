#import necessary modules
from pyhdf.SD import SD, SDC
import h5py
import numpy as np
import os, glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

def parse_data(df,extension,data_dir,data_names,counties,coordinates):
    '''
    df - the main dataframe (jhu covid data)
    extension - file extension of your space data, e.g. h5, hdf, he5
    data_dir - the path to the data directory
    data_names - the names of the data you are extracting
    counties - the dataframe containing coordinates for each county
    coordinates - indices for the data matrix if your data doesn't come with coordinates
    '''

    # b = datetime(2019, 12, 31)
    # x = b + timedelta(days=1)
    #dmisses = []

    #loops through all files listed in the text file
    for FILE_NAME in glob.glob(data_dir+'*'+extension):

        # **********************************************************
        # Do what you need to do to get your data into a numpy array
        # **********************************************************
        
        #--------------------------------------
        # For h5/he5 files
        #--------------------------------------
        file = h5py.File(FILE_NAME, 'r')   # 'r' means that hdf5 file is open in read-only mode
        data = file['HDFEOS']['GRIDS']['OMI UVB Product']['Data Fields']['UVindex'][:]
        data = np.where(data>=0,data,np.nan)
        date = datetime.strptime(FILE_NAME.split('_')[2],'%Ym%m%d')
        print(date)

        #data = file['Geophysical Data'][:]
        # x, y = data.shape[:-1]
        # data = np.where((data>=0)&(data<=327.6),data,np.nan).reshape(x,y)
        # date = datetime.strptime(FILE_NAME.split('_')[1],'%Y%m%d')
        
        # print(date)
        # print(np.count_nonzero(~np.isnan(data))/(1800*3600))

        # doy = int(FILE_NAME.split('.')[1][5:])
        # print(doy)
        # date = b + timedelta(days=doy)

        #--------------------------------------
        # For h4 files
        #-------------------------------------
        # hdf=SD(FILE_NAME)
        # data=hdf.datasets()
        # daytemp = hdf.select('LST_Day_CMG')[:,:]*0.02
        # daytemp[daytemp==0] = np.nan
        # nighttemp = hdf.select('LST_Night_CMG')[:,:]*0.02
        # nighttemp[nighttemp==0] = np.nan        
        # counties['LST_Day'] = daytemp[lat,lon]
        # counties['LST_Night'] = nighttemp[lat,lon]

        # Reads in data for each county and get the mean
        lat, lon = coordinates
        counties[data_names] = data[lat,lon]
        temp = counties.groupby(['state','county']).mean()
        temp['dt'] = date
        temp.set_index('dt',append=True,inplace=True)

        # Merge with the main dataframe
        df_date = df.drop(columns=data_names).loc(axis=0)[:,:,date]
        merged = pd.merge(df_date,temp[data_names],on=['state','county','dt'])
        df.update(merged)


    print('\nAll valid files given have been processed')

def main():
    # Specify your variables as per the parse_data function

    _df = pd.read_csv('jhu_covid19_backup.csv',parse_dates=['dt'])
    _df.set_index(['state','county'],inplace=True)

    counties = pd.read_csv('states_geo.csv')
    counties = counties.round(2)[['latitude','longitude','state','county']]
    
    light = pd.read_csv('combined_coords_state.csv')
    #light.rename(columns={'value':'Night Light'})
    light = light.round(2)

    def lat_get_county(df):
        lon = df['longitude'].mean()
        lat = df['latitude'].mean()
        s1 = light.iloc[(light['latitude']-lat).abs().argsort().values[0]]['latitude']
        close = light[light.latitude == s1]

        if len(close) == 0 or abs(s1 - lat) > 0.1:
            df['Night Light'] = np.nan
            return df

        c1 = close.iloc[(close['longitude']-lon).abs().argsort().values[0]]
        if len(c1) == 0 or abs(c1['longitude'] - lon) > 0.1:
            df['Night Light'] = np.nan
            return df
        df['Night Light'] = c1['value']
        print(df[['state','county']])
        return df

    # counties = counties.groupby(['state','county']).apply(lat_get_county)
    # # light = light.groupby(['state','county']).mean()
    # counties.to_csv('combined_coords_state.csv')

    # d = dict(zip(counties['latitude'].astype(str)+counties['longitude'].astype(str),counties['county']+counties.blank+counties['state']))
    # light['county-state'] = (light['latitude'].astype(str)+counties['longitude'].astype(str)).map(d)
    # print(light[~light['county-state'].isnull()])

    # print(len(light)-len(light.dropna(subset=['county-state'])))
    

    # lat = ((90-counties['latitude'])/res).astype('int').values
    # lon = ((counties['longitude']+180)/res).astype('int').values

    # parse_data(df=df,extension=extension,data_dir=data_dir,data_names=data_names,
    #     counties=counties,coordinates=(lat,lon))

    # df = df.groupby(df.index).bfill().ffill()
    light = light.groupby(['state','county']).mean()
    print(light.index)
    _df = pd.merge(_df,light['Night Light'],on=['state','county'],how='left')
    _df.to_csv('jhu_covid19_light.csv')

if __name__ == "__main__":
    main()