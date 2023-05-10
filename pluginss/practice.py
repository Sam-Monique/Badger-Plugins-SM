import pandas as pd

df = pd.read_csv('pracitce.csv')

total  = 0
for i in range(df.shape[0]):
    for keys in df.keys():
        total += abs(df.iloc[i][keys] - 1)
print(total)