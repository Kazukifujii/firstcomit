import numpy as np
from pdosfilter import SameObitalPdosFilter as SOP
from readinfo import setcifdata
import matplotlib.pyplot as plt
import pandas as pd
import readinfo as ri

dir='/home/fujikazuki/gaustest'
tdir='/home/fujikazuki/comptest'

ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]
cifdata1=setcifdata(ciflist[12])
test=SOP(cifdata1.cifadress)
"""
test.gaussianfilter(sigma=0.5)
for i in test.afterdata.keys():
    test.afterdata[i].to_csv(tdir+'/test3/'+i+'.csv')
"""
readtest1=pd.read_csv(tdir+'/test3/p.csv',index_col=0)


ydata=readtest1[[str(s[1]) for s in cifdata1.specsite][1]].to_numpy()
xdata=readtest1.index.to_numpy()

p_rtest=pd.DataFrame(ri.peakrange(xdata,ydata),columns=['x','y','p_r'])
#print(p_rtest)
fig=plt.figure()
ax1=fig.add_subplot(1, 1, 1)
ax1.plot(xdata,ydata)
xmax=p_rtest['x'].to_list()
ymax=p_rtest['y'].to_list()
integral_peak=p_rtest['p_r'].to_list()

ax1.plot(xmax,ymax,'ro')
i=3
ax1.plot([xmax[i]-integral_peak[i],xmax[i]+integral_peak[i]],[2,2],'mo')
"""
for i in range(len(xmax)):
    if i%2==0:
        ax1.plot([xmax[i]-integral_peak[i],xmax[i]+integral_peak[i]],[2,2],'mo')
    else:
        ax1.plot([xmax[i]-integral_peak[i],xmax[i]+integral_peak[i]],[3,3],'mo')
"""
ax1.set_ylim([0,5])
ax1.set_xlim([-20,40])
ax1.grid()
plt.show()