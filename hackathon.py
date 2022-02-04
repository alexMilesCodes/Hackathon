import pandas as pd
from alive_progress import alive_it


data = pd.read_csv('HIP-Data.csv')
data['Year'] = [int(data['Date'][i][6:]) for i in range(len(data['Date']))]

print('data recieved, rows: ' + str(len(data['Date'])))

data = data.loc[data['SalesVolume'].notna()]

data2 = pd.DataFrame({'Date': data['Date'].unique()})
data2['Year'] = [int(data2['Date'][i][6:]) for i in range(len(data2['Date']))]
data2['Month'] = [int(data2['Date'][i][3:5]) for i in range(len(data2['Date']))]
cols = data.columns.tolist()
cols.remove('Date')
cols.remove('AreaCode')
cols.remove('RegionName')
cols.remove('SalesVolume')

print('New rows: ' + str(len(data['Date'])))

count = 0
for col in alive_it(cols):
    col_ = []
    full = True
    for date in data2['Date']:
        sub = data.loc[data['Date'] == date][['SalesVolume', col]]
        if sub[col].any():
            col_.append(sum([int(sub[col][i])*int(sub['SalesVolume'][i]) for i in sub.loc[sub[col].notna()].index])/
                        sum(sub[col].notna().astype('int')*sub['SalesVolume']))
        else:
            col_.append('')
            full = False
    if full:
        data2[col] = col_
    count += 1
    print(str(count) + '/' + str(len(cols)))

data3 = data.groupby('Date')['SalesVolume'].mean()
data2 = data2.join(data3, 'Date', 'inner')
print(data2.head())
data2.to_csv('data2.csv')
