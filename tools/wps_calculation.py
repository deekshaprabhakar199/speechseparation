import pandas as pd
import numpy as np
import matplotlib

df = pd.read_csv('../eval-results/recording_characteristics.csv', sep='|')

def count_words(x):
    n=x.split()
    return len(n)

df['n_words']=df['ground_truth'].apply(count_words)
df['wpm']=df['n_words']/df['duration']*60
print(df['wpm'])
print(df['wpm'].describe())

df['speed_class']=np.where(df['wpm']>=170, 'Fast',
                                np.where(df['wpm'] >=140, 'Average', 'Slow'))

df['wpm'].hist()
matplotlib.pyplot.show()
df.to_csv('../eval-results/recording_characteristics.csv', sep='|', index=False)
