import pandas as pd

df = pd.read_csv('cctv.csv')
df.drop(['cameraLocation',  'cameraNumber', 'cameraProject'], axis=1, inplace=True)
df.dropna(inplace=True)

df['lat'] = df['Location 1'].map( lambda x: float(x[1:-1].split(', ')[0]) )
df['long'] = df['Location 1'].map( lambda x: float(x[1:-1].split(', ')[1]) )
df.drop(['Location 1'], axis=1, inplace=True)

df.to_csv('clean_cctv.csv')
