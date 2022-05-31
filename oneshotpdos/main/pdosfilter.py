from functions import set_pdosdata
from readinfo import setcifdata
import matplotlib.pyplot as plt
import re
import math
import pandas as pd
from scipy import integrate
import numpy as np

def gausfunc(x,sigma):
            return pow(2*math.pi*sigma**2,-0.5)*math.exp(-(x**2)/(2*sigma**2))


class pdosfilter:
    """sample
    ciffile='~/ciflist/result/9008862
    cpdos=pdosfilter(ciffile)
    """
    def __init__(self,resultdir):
        self.rawpdosdata=set_pdosdata(resultdir)
        self.afterpdosdata=self.rawpdosdata
        
    def savepdos(self,orbital=list(range(1,6)),fig_name=str(),key='dos.isp1.site001.tmp'):
        plt.clf()
        pdosdic=self.afterpdosdata
        pdosdf=pdosdic[key]
        for i in orbital:
            pdosdf[i].plot()
        for i in range(len(orbital)):
            I=orbital[i]
            if I==1:
                orbital[i]='s'
            elif I==2:
                orbital[i]='p'
            elif I==3:
                orbital[i]='d'
            elif I==4:
                orbital[i]='f'
        plt.ylim([0,5])
        plt.xlim([-20,40])
        plt.grid()
        plt.legend(orbital)
        titile=fig_name+'_'+re.sub("\[|\]|'|","",str(orbital))
        plt.title(titile)
        plt.savefig(titile+'.png')

    def gaussianfilter(self,sigma):
        """
        import os,shutil
from main.pdosfilter import pdosfilter
from readinfo import setcifdata
import numpy as np
#parsing ciffiles in the direcoty
#there result direcoty
cifdir='/home/fujikazuki/gaustest'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]
for sigma in np.arange(0.01,10,0.01):
    pngdir=cifdir+'/gausupdos_'+str(sigma)
    try:
        os.mkdir(pngdir)
    except:
        shutil.rmtree(pngdir)
        os.mkdir(pngdir)
    os.chdir(pngdir)

    cifdatas=[setcifdata(s) for s in ciflist]
    for cifdata in cifdatas:
        if cifdata.allsite!=None:
            print('start '+cifdata.cifnumber+' '+str(sigma))
            os.mkdir(cifdata.cifnumber)
            os.chdir(cifdata.cifnumber)
            pdosdata=pdosfilter(cifdata.resultadress)
            key=list(pdosdata.afterpdosdata.keys())
            pdosdata.gaussianfilter(sigma=sigma)
            for j in range(len(cifdata.allsite)):
                figname=cifdata.formular+str(cifdata.allsite[j])
                key='dos.isp1.site{0:03d}.tmp'.format(j+1)
                for i in range(1,4):
                    pdosdata.savepdos(orbital=[i],fig_name=figname,key=key)
            print('end \n')
            os.chdir('..')
        """
        for i,key in enumerate(self.afterpdosdata):
            for j in self.afterpdosdata[key].columns.to_list():
                x=self.afterpdosdata[key][j].index.to_list()
                y=self.afterpdosdata[key][j][:].to_list()
                for k in x:
                    concolution=[y[l]*gausfunc(k-a,sigma) for l,a in enumerate(x)]
                    self.afterpdosdata[key][j][k]=integrate.simps(np.array(concolution),np.array(x))