########################
### DATA PREPARE
#########################

import pandas as pd
import numpy as np

### Read in county info and drought data, select snapshot of date 2016-06-28
county = pd.read_csv('./county_info_2016.csv', encoding = "ISO-8859-1")
county.columns = ['USPS','GEOID','ANSICODE','NAME','ALAND','AWATER','ALAND_SQMI','AWATER_SQMI','INTPTLAT','INTPTLONG' ]
county = county[['GEOID','ALAND_SQMI','AWATER_SQMI']]

dr = pd.read_csv('./us-droughts.csv')
data = dr[dr.releaseDate == '2016-06-28']

### Data cleansing
data = data.drop(data[['validStart', 'validEnd', 'domStatisticFormatID']], axis=1)

### Calculate drought level (when NONE is 100% => 0, if D4 is 100% => 5, and linearly between 0 and 5)
data['LEVEL'] = (data.D4*5 + (data.D3-data.D4)*4 + (data.D2-data.D3)*3 + (data.D1-data.D2)*2 + (data.D0-data.D1))/100

### Merge drought data and county info by FIPS/GEOID
data_final = pd.merge(data, county, left_on='FIPS', right_on='GEOID', how='inner', sort='False')
### Prepend column FIPS to 5-digits 
data_final['FIPS'] = data_final['FIPS'].astype(str)
data_final['FIPS'] = data_final['FIPS'].apply(lambda x: x.zfill(5))
data_final = data_final[['state', 'county', 'FIPS', 'LEVEL', 'ALAND_SQMI', 'AWATER_SQMI']]

### output data
data_final.to_csv('drought_combined.csv', index = False)

