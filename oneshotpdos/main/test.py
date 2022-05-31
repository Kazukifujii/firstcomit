from email import header
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from requests import head
from scipy import integrate
minrange,maxrange,step=0,40,0.01
S=0.1

indexl=[i for i in np.arange(minrange,maxrange,step)]

testdata=pd.DataFrame(index=indexl,columns=[1,2])

for i in testdata.index.tolist():
    if i==indexl[2000]:  
        testdata[1][i]=1
    else:
        testdata[1][i]=0
for i in testdata.index.tolist():
    if i==indexl[2000]:  
        testdata[2][i]=1
    else:
        testdata[2][i]=0
testdata.to_csv('/home/fujikazuki/ciflist/testdata/testdata.csv')
df={'test1':pd.read_csv('/home/fujikazuki/ciflist/testdata/testdata.csv',index_col=0)}



import os,shutil
#parsing ciffiles in the direcoty
#there result direcoty
cifdir='/home/fujikazuki/ciflist'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]

pngdir=cifdir+'/testgasu2'
try:
    os.mkdir(pngdir)
except:
    shutil.rmtree(pngdir)
    os.mkdir(pngdir)
os.chdir(pngdir)


from readinfo import setcifdata
from main.pdosfilter import pdosfilter
cifdatas=[setcifdata(s) for s in ciflist]
for cifdata in cifdatas:
    if cifdata.allsite!=None:
        os.mkdir('gausu'+cifdata.cifnumber)
        os.chdir('gausu'+cifdata.cifnumber)
        pdosdata2=pdosfilter(cifdata.resultadress)
        pdosdata2.afterpdosdata=df
        key=list(pdosdata2.afterpdosdata.keys())
        pdosdata2.gaussianfilter(sigma=S)
        pdosdata2.afterpdosdata[key[0]].plot()
        plt.show()
        os.chdir('..')
    break



import sys

sys.exit()
#gaussian filter

def g(x,sigma):
    return pow(2*math.pi*sigma**2,-0.5)*math.exp(-(x**2)/(2*sigma**2))



def gaussianfilter(x,y,sigma,e):
    concolution=[y[i]*g(e-x[i],sigma) for i,a in enumerate(x)]
    result=integrate.simps(np.array(concolution),np.array(x))
    return result
x=testdata.index.to_list()
y=testdata[1][:].to_list()
sigma=40
for i in x:
    testdata[1][i]=gaussianfilter(x,y,sigma,i)
testdata.plot()
plt.show()