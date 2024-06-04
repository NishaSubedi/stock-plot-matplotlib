import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

pd.set_option('display.max_columns', None)
df= pd.read_json('stock.json')

results_df = pd.json_normalize(df['results'])
df = df.drop(columns=['results']).join(results_df)

print(df.isnull().sum())

df['createdDateAd'] = pd.to_datetime(df['createdDateAd'])
df['createdDateBs'] = pd.to_datetime(df['createdDateBs'])

df.drop(['id', 'location', 'basicInfo', 'image', 'manufacturer', 'unit', 'countryOfOrigin'], axis=1, inplace=True)

print(df.duplicated().sum())
df.drop_duplicates(inplace=True)


plt.figure(figsize=(10, 6))
plt.bar(df['name'], df['remainingQty'], color='blue', label='Remaining Quantity')

for i, row in df.iterrows():
    
    if row['remainingQty'] <= row['stockAlertQty']:
        bar_color = 'red' 
    else:
        bar_color = 'blue'  

    plt.bar(row['name'], row['remainingQty'], color=bar_color)
    

plt.bar(df['name'], df['stockAlertQty'], color='red', label='Stock Alert')
alert_qty = df['stockAlertQty'].iloc[0] 
plt.axhline(y=alert_qty, color='black', linestyle='--')


plt.xlabel('Product Name')
plt.ylabel('Remaining Quantity')
plt.title('Remaining Quantity of Products')
plt.xticks(rotation=90)  
plt.legend()


plt.tight_layout()
plt.show()