from pdosfilter import MpPosdata as mpd
resultdir='/home/fujikazuki/Documents/mp2534'

t=mpd(mpadress=resultdir)
t.gaussianfilter(sigma=0.5)


import matplotlib.pyplot as plt

import pandas as pd
idx=pd.IndexSlice['s',:]
col=pd.IndexSlice[t.atomlist[0]]

t.afterdata.plot()
plt.show()