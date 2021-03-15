# -*- coding: utf-8 -*-
from keys import ameritrade
import requests, time, re
import pandas as pd
import pickle as pkl

url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_excel('company_list.xlsx')
symbols = df['Symbol'].values.tolist() #pull symbols

start = 0  #check 500 at a time
end = 500
files = []

while start < len(symbols):
    tickers = symbols[start:end]
    

    payload = {'apikey': ameritrade, #code payload to deliver to HTML
           'symbol': tickers,
           'projection': 'fundamental'}

    results = requests.get(url,params=payload)
    data = results.json()
    f_name = time.asctime() + '.pkl'
    f_name = re.sub('[ :]', '_', f_name)
    files.append(f_name)
    with open (f_name, 'wb') as file:
        pkl.dump(data,file)  #dump to file
    
    start = end
    end += 500 # end can be out of index range
    time.sleep(1)

data = []       #data.keys() to see all

for file in files: 
    with open(file, 'rb') as f:
        info = pkl.load(f)
        tickers = list(info) # points below can be changed to preference. see data ['tickerCode']
        points = ['symbol','netProfitMarginMRQ','peRatio','pegRatio','high52']
        for ticker in tickers:
            tick = []
            for point in points:
                tick.append(info[ticker]['fundamental'][point])
            data.append(tick)
#        os.remove(file) - not working. manual delete

points = ['symbol','Margin','PE','PEG','high52']

df_results = pd.DataFrame(data,columns=points)
df_peg = df_results[(df_results['PEG'] < 1) & (df_results['PEG'] > 0) & (df_results['Margin'] > 20) & (df_results['PE'] > 10)]
#use df_peg to find shortlist

# use the statement below (can be modified) as a filter
# df_peg = df_results[(df_results['PEG'] < 1) & (df_results['PEG'] > 0) & (df_results['Margin'] > 20) & (df_results['PE'] > 10)]

def view(size):
    start = 0
    stop = size
    while stop < len(df_peg):
        print(df_peg[start:stop])
        start = stop
        stop += size
    print(df_peg[start:stop])

#commands
#df_results > all stonks
#df_peg > shortlisted stonks 
#view(size -- eg. 40)
#TODO: remake prefered data filters
# df_peg.sort_values(['PEG'])
#pd.set_option('display.max_rows',200)
#df
#
#pulling out one piece of data:
#df_symbols = df_peg['symbol'].tolist()
#new = df['Symbol'].isin(df_symbols)
# new    ------------ check for symbol in ...
# this is how the data is detached from list



