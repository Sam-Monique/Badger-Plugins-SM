import numpy as np

x = np.array([1,2,3]).reshape(-1,1)


a = [1,1]
b = [2,2]

for i, j in zip(a,b):
    print(i,j)