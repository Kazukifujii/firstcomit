from re import L
from pdosfilter import MpPosdata as sob
import pandas as pd
from constant import ORBITAL
import math


dir='/home/fujikazuki/Documents/ecalj関係/mp1000'
dir2='/home/fujikazuki/Documents/ecalj関係/mp1885'

d1=sob(dir)
d1.gaussianfilter(0.5)
d1.peakdata()
d2=sob(dir2)
d2.gaussianfilter(0.5)
d2.peakdata()
siten_dic=dict()
for siten in [0,1]:
    col_d1=pd.IndexSlice[d1.atomlist[siten],:]
    col_d2=pd.IndexSlice[d2.atomlist[siten],:]
    orbital_dic=dict()
    for o in ORBITAL:
        idx=pd.IndexSlice[o,:]
        orbital_df=pd.DataFrame()
        for I,i in d1.peaks.loc[idx,col_d1].iterrows():
            for J,j in d2.peaks.loc[idx,col_d2].iterrows():
                l=abs(i.droplevel(level=0)-j.droplevel(level=0))
                L=l['arg_y']*math.sqrt(l['arg_x']*2+l['peak_range']*2)
                orbital_df.loc[I[1],J[1]]=L
        orbital_dic[o]=orbital_df
    siten_dic['site_%i'%siten]=pd.concat(orbital_dic)
L_df=pd.concat(siten_dic,axis=1)

print(L_df)
