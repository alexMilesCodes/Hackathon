import pandas as pd


data = pd.read_csv('HIP-Data.csv')
data['Year'] = [int(data['Date'][i][6:]) for i in range(len(data['Date']))]
data = data.loc[data['Year'] > 1994]

dada = pd.DataFrame({'Date': data['Date'].unique()})
temp = []
for date in data['Date'].unique():
    print(str(date) + ' ---> ' + str(list(data['Date']).count(date)))
    temp.append(str(list(data['Date']).count(date)))

dada['Num'] = temp

dada.to_csv('dada.csv')
