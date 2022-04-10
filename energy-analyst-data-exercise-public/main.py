import numpy as np
import pandas as pd

# Task 1
data1 = pd.read_csv('./historicalPriceData/ERCOT_DA_Prices_2016.csv')
data2 = pd.read_csv('./historicalPriceData/ERCOT_DA_Prices_2017.csv')
data3 = pd.read_csv('./historicalPriceData/ERCOT_DA_Prices_2018.csv')
data4 = pd.read_csv('./historicalPriceData/ERCOT_DA_Prices_2019.csv')

data = pd.concat([data1, data2, data3, data4])

# Task 2
data['Date'] = pd.to_datetime(data['Date'])

data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

means = data.groupby(
    ['SettlementPoint', 'Year', 'Month'])['Price'].mean()

means = means.to_frame()
means = means.rename(columns={'Price': 'AveragePrice'})

# Task 3
means.to_csv('AveragePriceByMonth.csv')

# Task 4
vol = {'SettlementPoint': [],
       'Year': [],
       'HourlyVolatility': []}

hubs = data[data.SettlementPoint.str.startswith(
    'HB_') & data.Price > 0].groupby(['SettlementPoint', 'Year'])


for sp, group in hubs:
    # gives warning due to first index, need to fix indexing so it skips
    group['LogReturn'] = np.log(group['Price']/group['Price'].shift())
    stdev = group['LogReturn'].std()
    vol['SettlementPoint'].append(sp[0])
    vol['Year'].append(sp[1])
    vol['HourlyVolatility'].append(stdev)

vol1 = pd.DataFrame(vol)
vol1.to_csv('HourlyVolatilityByYear.csv', index=False)

# Task 6
max = vol1.loc[vol1.groupby('Year')['HourlyVolatility'].idxmax()]
max.to_csv('MaxVolatilityByYear.csv', index=False)

# Task 7
data = pd.concat([data1, data2, data3, data4])
data['Date'] = pd.to_datetime(data['Date'])


sp = data.groupby('SettlementPoint')

# Iterate over SP groups using for loop:
# create new dataframes with same columns as supplementalMaterials files, group by date,
# transpose price data, append to dataframe
#
# Write to csv
