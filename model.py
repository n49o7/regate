"""
Curve-fitting our way towards a performance model.
"""


import pandas as pd
import numpy as np

with open('data/perf_speed_interpol.csv') as f:
    speed = pd.read_csv(f)

with open('data/perf_sails_interpol.csv') as f:
    sails = pd.read_csv(f).drop('Unnamed: 0',axis=1)

# sails.iloc[w-1, a]

for y in range(180):
    try:
        print(speed.iloc[0,y], sails.iloc[0,y])
    except:
        print('No perf sheet for angle', y)

n = [ [ [ speed.iloc[x-1,y], sails.iloc[x-1,y] ] for y in range(180) ] for x in range(1,40) ]
n = np.array(n)

# n[s][a][sp,s]

n[:,:,0]

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
%matplotlib tk
fig = plt.figure()
ax = plt.axes(projection='3d')
xdata = range(180)
ydata = range(39)
# zdata = np.random.random(100)
zdata = n[:,:,0]
cdata = n[:,:,1]
ax.scatter3D(xdata, ydata, zdata, 'gray')
plt.savefig('suckthis.png')

xyz=np.array(np.random.random((100,10,2)))
xyz[0]

len(xdata)
len(ydata)
zdata.shape
cdata.shape




import matplotlib
matplotlib.rcsetup.interactive_bk
# matplotlib.use('WebAgg')
# matplotlib.interactive()
# plt.ion()
# plt.plot_surface(pd.DataFrame(n).unstack().reset_index())




speed[:5]

sails[:5]
