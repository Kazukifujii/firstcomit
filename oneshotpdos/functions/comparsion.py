from sympy import O, Or
import readinfo as rf
import pandas as pd
from pdosfilter import SameObitalPdosFilter as sop
import re,os,itertools
from constant import element_group,ORBITAL
from makepdos import listup_cif
import numpy as np


def cif_conbination(cif_dir):
    cif_list_txt=cif_dir+'/cif_list.txt'
    if not os.path.isfile(cif_list_txt):
        listup_cif(cif_dir)
    with open(cif_list_txt,mode='r') as f:
            ciflist=[re.search(r"([^/]*?)$",s.strip()).group() for s in f.readlines()]
    return list(itertools.combinations(ciflist,2))

class ComparsionPdos():
    """
    """
    def __init__(self,cifadress_1,cifadress_2):
        self.pdos_data_1=sop(cifadress_1)
        self.pdos_data_2=sop(cifadress_2)
        if len(self.pdos_data_1.cifdata.specsite)!=len(self.pdos_data_2.cifdata.specsite):
            print('not same number of specsite')
            return
        self.weight=dict()
        self.specrange=len(self.pdos_data_1.cifdata.specsite)
        atomlist1=[(str(i[1]),element_group[i[1][0]]) for i in self.pdos_data_1.cifdata.specsite]
        atomlist2=[(str(i[1]),element_group[i[1][0]]) for i in self.pdos_data_2.cifdata.specsite]
        atomlist1.sort(key = lambda x: x[1])
        atomlist2.sort(key = lambda x: x[1])
        self.atomlist_1=[s for s,_ in atomlist1]
        self.atomlist_2=[s for s,_ in atomlist2]
    
    def gaussian(self,Sigma):
        self.pdos_data_1.gaussianfilter(sigma=Sigma)
        self.pdos_data_2.gaussianfilter(sigma=Sigma)
        
    
    def difference(self):
        #sort by element group number
        if len(self.pdos_data_1.cifdata.specsite)!=len(self.pdos_data_2.cifdata.specsite):
            print('not same number of specsite')
            return
        self.difdict=dict()
        for orbital in ORBITAL:
            difdf=pd.DataFrame()
            for j,_ in enumerate(self.specrange):
                difdf[j]=abs(self.pdos_data_1.afterdata[orbital][self.atomlist_1[j]]-self.pdos_data_2.afterdata[orbital][self.atomlist_2[j]])
            self.difdict[orbital]=difdf
    
    def peak_range(self):
        self.peakdata_1=dict()
        for orbital in ORBITAL:
            peakd=dict()
            for i,ss in enumerate(self.atomlist_1):
                peakd[ss]=pd.DataFrame(rf.peakrange(np.array(self.pdos_data_1.xdata),self.pdos_data_1.afterdata[orbital][ss].to_numpy()),columns=['arg_x','arg_y','peak_range'])
            self.peakdata_1[orbital]=pd.concat(peakd,axis=1)
        self.peakdata_1=pd.concat(self.peakdata_1)
        
dir='/home/fujikazuki/gaustest'
resultdir='/home/fujikazuki/gaustest/classtest'
ciflist=[s.replace('\n','')  for s in open(dir+'/cif_list.txt')]
tc=ComparsionPdos(cifadress_1=ciflist[11],cifadress_2=ciflist[2])
tc.gaussian(Sigma=0.5)
tc.peak_range()
o='p'
s=1
print(tc.peakdata_1)
import matplotlib.pyplot as plt
fig=plt.figure()
ax1=fig.add_subplot(1, 1, 1)
idx=pd.IndexSlice[o,:]
col=pd.IndexSlice
xdata=tc.pdos_data_1.xdata
ydata=tc.pdos_data_1.afterdata[o][tc.atomlist_1[s]].to_list()
xmax=tc.peakdata_1.loc[idx,col[tc.atomlist_1[1],'arg_x']].to_list()
ymax=tc.peakdata_1.loc[idx,col[tc.atomlist_1[1],'arg_y']].to_list()
integral_peak=tc.peakdata_1.loc[idx,col[tc.atomlist_1[1],'peak_range']].to_numpy()/2
ax1.plot(xdata,ydata)
ax1.plot(xmax,ymax,'ro')
for i in range(len(xmax)):
    if i%2==0:
        ax1.plot([xmax[i]-integral_peak[i],xmax[i]+integral_peak[i]],[2,2],'mo')
    else:
        ax1.plot([xmax[i]-integral_peak[i],xmax[i]+integral_peak[i]],[3,3],'mo')

ax1.set_ylim([0,5])
ax1.set_xlim([-20,40])
ax1.grid()
plt.show()