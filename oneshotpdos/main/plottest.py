
import re
import os,shutil
from readinfo import setcifdata
from main.pdosfilter import pdosfilter
#parsing ciffiles in the direcoty
#there result direcoty
cifdir='/home/fujikazuki/ciflist'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]

try:
    os.mkdir(cifdir+'/testpdospng')
except:
    shutil.rmtree(cifdir+'/testpdospng')
    os.mkdir(cifdir+'/testpdospng')
os.chdir(cifdir+'/testpdospng')

cifdatas=[setcifdata(s) for s in ciflist]
for cifdata in cifdatas:
    if cifdata.allsite!=None:
        os.mkdir(cifdata.cifnumber)
        os.chdir(cifdata.cifnumber)
        pdosdata=pdosfilter(cifdata.resultadress)
        for j in range(len(cifdata.allsite)):
            figname=cifdata.formular+str(cifdata.allsite[j])
            key='dos.isp1.site{0:03d}.tmp'.format(j+1)
            for i in range(1,4):
                pdosdata.savepdos(orbital=[i],fig_name=figname,key=key)
        os.chdir('..')