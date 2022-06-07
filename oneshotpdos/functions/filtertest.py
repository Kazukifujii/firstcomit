import pdosfilter as pf
import functions as fn
from readinfo import setcifdata
import pandas as pd
import matplotlib.pyplot as plt

cifdir='/home/fujikazuki/gaustest'
resultdir=cifdir+'/orbital_p_gausianfilter'

ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]
cifdatas=[setcifdata(s) for s in ciflist]

orbital=[2]
piccifdata=cifdatas[2]
pdosdata=pf.pdosfilter(piccifdata.resultadress)
"""
pkeys=list(pdosdata.rawpdosdata.keys())
xval=pdosdata.rawpdosdata[pkeys[0]].index.to_list()
ykeys=[str(s[1]) for i,s in enumerate(piccifdata.specsite)]
all_p_pdos=pd.DataFrame(index=xval,columns=ykeys)
orbital=2
pdosdata.gaussianfilter(sigma=0.09)
for i,s in enumerate(ykeys):
    sitenumber=int(piccifdata.specsite[i][0])
    all_p_pdos[s][:]=pdosdata.afterpdosdata['dos.isp1.site{0:03d}.tmp'.format(sitenumber)].loc[:,orbital]
all_p_pdos.plot()
"""
import os,shutil
try:
    os.mkdir(cifdir+'/testsameorbital')
except:
    shutil.rmtree(cifdir+'/testsameorbital')
    os.mkdir(cifdir+'/testsameorbital')
os.chdir(cifdir+'/testsameorbital')
pdosdata.gaussianfilter(sigma=1.0)
title=piccifdata.formular
pdosdata.savepdos_sameorbital(piccifdata.specsite,fig_name=title,orbital=[2])
