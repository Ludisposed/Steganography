import random
import numpy as np

d = [ [ [1, 2, 3],    [4, 5, 6],    [7 ,8 ,9] ], 
      [ [10, 11, 12], [13, 14, 15], [16 ,17 ,18] ],
      [ [19, 20, 21], [22, 23, 24], [25 ,26 ,27] ] ]
d = np.asarray(d)
r = random.sample(range(1, d.size), 3)

print(r)
d_lin = d.view()  # construct a view
d_lin.shape = -1  # turn the view into a 1d array

for i in r:
    print d_lin[i-1]
