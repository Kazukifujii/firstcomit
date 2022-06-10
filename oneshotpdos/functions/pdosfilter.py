from readinfo import set_pdosdata
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from constant import element_group,colordata
from readinfo import set_sameorbital,setcifdata

def gausfunc(x,sigma):
        return pow(2*math.pi*sigma**2,-0.5)*math.exp(-(x**2)/(2*sigma**2))


class PdosFilter:
    """sample
    ciffile='~/ciflist/9008862.cif
    cpdos=PdosFilter(ciffile)
    """
    def __init__(self,cifadress):
        self.cifdata=setcifdata(cifadress)
        if  self.cifdata.allsite!=None:
            self.rawpdosdata=set_pdosdata(self.cifdata.resultadress)
            self.afterpdosdata=set_pdosdata(self.cifdata.resultadress)
            self.pkeys=list(self.rawpdosdata.keys())
            self.xdata=self.rawpdosdata[self.pkeys[0]].index.to_list()
            self.sameorbital_pdos=set_sameorbital(specdata=self.cifdata.specsite,pdosdata=self.afterpdosdata)
    
    def savepdos(self,orbital=list(range(1,6)),fig_name=str(),key='dos.isp1.site001.tmp'):
        plt.clf()
        pdosdic=self.afterpdosdata
        pdosdf=pdosdic[key]
        for i in orbital:
            pdosdf[i].plot()
        plt.ylim([0,5])
        plt.xlim([-20,40])
        plt.grid()
        plt.legend(orbital)
        titile=fig_name+'_'+str(orbital)
        plt.title(titile)
        plt.savefig(titile+'.png')
        plt.close()
    
    def gaussianfilter(self,sigma):
        """
        import pdosfilter as pf
        from readinfo import setcifdata
        import numpy as np
        import os,shutil,time


        startime=time.perf_counter()

        cifdir='/home/fujikazuki/gaustest'
        resultdir=cifdir+'/after_p_pdos'

        try:
            os.mkdir(resultdir)
        except:
            shutil.rmtree(resultdir)
            os.mkdir(resultdir)
        os.chdir(resultdir)

        ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]
        cifdatas=[setcifdata(s) for s in ciflist]
        st=time.perf_counter()
        for sigma in np.arange(0.01,1,0.01):
            print('sigma=',sigma)
            try:
                os.mkdir("sigma="+str(sigma))
            except:
                shutil.rmtree("sigma="+str(sigma))
                os.mkdir("sigma="+str(sigma))
            os.chdir("sigma="+str(sigma))
            for cifdata in cifdatas:
                print(cifdata.cifnumber)
                if cifdata.allsite!=None:
                    try:
                        os.mkdir(cifdata.cifnumber)
                    except:
                        shutil.rmtree(cifdata.cifnumber)
                        os.mkdir(cifdata.cifnumber)
                    os.chdir(cifdata.cifnumber)
                    pdosdata=pf.pdosfilter(cifdata.resultadress)
                    pdosdata.gaussianfilter(sigma=sigma)
                    for j,info in enumerate(cifdata.allsite):
                        figname=cifdata.formular+str(info)
                        key='dos.isp1.site{0:03d}.tmp'.format(j+1)
                        for i in range(2,3):
                            pdosdata.savepdos(orbital=[i],fig_name=figname,key=key)
                    os.chdir('..')
            os.chdir('..')
        et=time.perf_counter()
        print(et-st)

        """
        for i,key in enumerate(self.afterpdosdata):
            for j in self.afterpdosdata[key].columns.to_list():
                x=self.afterpdosdata[key][j].index.to_list()
                y=self.afterpdosdata[key][j][:].to_list()
                dx=x[1]-x[0]
                minx=x[0]
                maxx=x[-1]
                c=[gausfunc(a,sigma) for a in np.arange(minx-maxx-dx,-minx+maxx+dx,dx)]
                r=np.convolve(y,c,mode='valid')
                for l,k in enumerate(x):
                   self.afterpdosdata[key][j][k]=r[l]*dx

    def savepdos_sameorbital(self,specdata,orbital=list(range(1,6)),fig_name=str(),outputcsv=False):
        """sample specdata=[site number,[site element,(position)]]
        specdata=[['2', ['Cd', ('2.387228', '0.000000', '3.374500')]], ['4', ['S', ('2.387228', '0.000000', '5.972865')]]]
        """
        atomlist=[(str(i[1]),element_group[i[1][0]]) for i in specdata]
        atomlist.sort(key = lambda x: x[1])
        colordict={key:colordata[i] for i,(key,_) in enumerate(atomlist)}
        for i,val in enumerate(orbital):
            plt.clf()
            self.sameorbital_pdos[str(val)].plot(color=colordict)
            plt.ylim([0,5])
            plt.xlim([-20,40])
            plt.grid()
            titile=fig_name+'_'+str(orbital[i])
            plt.title(titile)
            plt.savefig(titile+'.png')
            plt.close()
            if outputcsv:
                self.sameorbital_pdos[str(val)].to_csv(titile+'.csv')
        return