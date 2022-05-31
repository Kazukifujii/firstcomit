import os,shutil
from gaussisanfilter import pdosfilter
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