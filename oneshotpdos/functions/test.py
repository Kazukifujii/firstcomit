from re import L
from pdosfilter import MpPosdata as sob


dir='/home/fujikazuki/Documents/ecalj関係/mp1000'
dir2='/home/fujikazuki/Documents/ecalj関係/mp1885'

d1=sob(dir)
d1.gaussianfilter(0.5)
d1.peakdata()

d2=sob(dir2)
d2.gaussianfilter(0.5)
d2.peakdata()


import pandas as pd




dc={key:'site_%i'%i for i,key in enumerate(d1.atomlist)}
dc2={key:'site_%i'%i for i,key in enumerate(d2.atomlist)}
def rename(x,site):
    return x.rename(site,inplace=True)

dd={'d1':d1.peaks,'d2':d2.peaks}
dd=pd.concat(dd,axis=1)
idx=pd.IndexSlice['p',:]
col=pd.IndexSlice[:,[d1.atomlist[0],d2.atomlist[0]],:]
#print(dd.loc[idx,col])
#d1_cols=d1.peaks.loc[idx,:].index.to_list()


#print(dd)


from constant import ORBITAL
import math
def colclate_l(x):
    return abs(x[1]-x[4])*math.sqrt(pow(x[0]-x[3],2)+pow(x[2]-x[5],2))

l_df=pd.DataFrame()
for siten in [0,1]:
    col_d1=pd.IndexSlice[d1.atomlist[siten],:]
    col_d2=pd.IndexSlice[d2.atomlist[siten],:]
    for o in ORBITAL:
        idx=pd.IndexSlice[o,:]
        orbital_dic=dict()
        for I,i in d1.peaks.loc[idx,col_d1].iterrows():
            for J,j in d2.peaks.loc[idx,col_d2].iterrows():
                l=abs(i.droplevel(level=0)-j.droplevel(level=0))
                L=l['arg_y']*math.sqrt(l['arg_x']*2+l['peak_range']*2)
                
print(l_df)