
from scipy.signal import argrelmax,argrelmin
from scipy import integrate
import numpy as np
import math


def peakrange(xdata,ydata):
    argmax=argrelmax(ydata)
    argmin=argrelmin(ydata)
    integral_peak=list()
    vii=0
    for i,v in enumerate(argmin[0]):
        integral_peak.append(integrate.simps(ydata[vii:v],xdata[vii:v]))
        vii=v
        if v==argmin[0][-1]:
            integral_peak.append(integrate.simps(ydata[v:-1],xdata[v:-1]))
    return [(math.pi*pow(ydata[argmax[0][i]]/v,2)) for i,v in enumerate(integral_peak)]


dir='/home/fujikazuki/gaustest'

tdir='/home/fujikazuki/comptest'

ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]
import math
from pdosfilter import SameObitalPdosFilter as SOP
from readinfo import setcifdata
cifdata1=setcifdata(ciflist[10])
test=SOP(cifdata1.cifadress)
"""
test.gaussianfilter(sigma=0.5)

for i in test.afterdata_sameorbital.keys():
    test.afterdata_sameorbital[i].to_csv(tdir+'/test3/'+i+'.csv')
"""
import matplotlib.pyplot as plt
import pandas as pd
readtest1=pd.read_csv(tdir+'/test3/p.csv',index_col=0)

from scipy.signal import argrelmax,argrelmin
import numpy as np
#np.set_printoptions(suppress=True)
print(cifdata1.specsite[1])
ydata=readtest1[[str(s[1]) for s in cifdata1.specsite][1]].to_numpy()
xdata=readtest1.index.to_numpy()
print(cifdata1.specsite)
argmax=argrelmax(ydata)
xmax=xdata[argmax[0]]
ymax=ydata[argmax[0]]
print(len(argmax[0]))
print(xmax)
print(ymax)
print('')
argmin=argrelmin(ydata)
print(len(argmin[0]))
xmin=xdata[argmin[0]]
ymin=ydata[argmin[0]]
print(xmin)
print(ymin)

import readinfo as ri
I=6
#Xmax,_,integral_peak=ri.test_peakrange(xdata,ydata)[I]
fig=plt.figure()
ax1=fig.add_subplot(1, 1, 1)
ax1.plot(xdata,ydata)
ax1.plot(xmax,ymax,'ro')
#ax1.plot([Xmax-integral_peak,Xmax+integral_peak],[1,1],'mo')

for i in range(len(argmax[0])):
    Xmax,_,integral_peak=ri.peakrange(xdata,ydata)[i]
    if i%2==0:
        ax1.plot([Xmax-integral_peak,Xmax+integral_peak],[2,2],'mo')
    else:
        ax1.plot([Xmax-integral_peak,Xmax+integral_peak],[3,3],'mo')

#ax1.plot([xmax[I]-g,xmax[I]+g],[2,2],'mo')
ax1.plot(xmin,ymin,'mo')

ax1.set_ylim([0,5])
ax1.set_xlim([-20,40])
ax1.grid()

plt.show()
