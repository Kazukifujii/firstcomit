import pdosplot 
import glob,sys,os,shutil
import functions as fs
from readinfo import setcifdata



dir='/home/fujikazuki/ciflist'
ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]

from readinfo import setcifdata
try:
    os.mkdir(dir+'/pdospng')
except:
    shutil.rmtree(dir+'/pdospng')
    os.mkdir(dir+'/pdospng')
os.chdir(dir+'/pdospng')

cifdatas=[setcifdata(s) for s in ciflist]

for cifdata in cifdatas:
    os.mkdir(cifdata.cifnumber)
    os.chdir(cifdata.cifnumber)
    print(cifdata.cifnumber)
    if cifdata.allsite!=None:
        for j in range(len(cifdata.allsite)):
            figname=cifdata.formular+str(cifdata.allsite[j])
            key='dos.isp1.site{0:03d}.tmp'.format(j+1)
            for i in range(1,4):
                pdosplot.savepdos(dir+'/result'+'/'+cifdata.cifnumber,orbital=[i],fig_name=figname,key=key)
    os.chdir('..')

sys.exit()
pdir=dir+'/pdospng'
files=os.listdir(pdir)
pdoslist=[dir+'/'+f+'.cif' for f in files if os.path.isdir(os.path.join(pdir, f))]
newciflist=[pdoslist[idx:idx + 4] for idx in range(0,len(pdoslist), 4)]


for i,cif in enumerate(newciflist):
    pdosplot.sumpdos(dir+'/pdospng',cif,orbital='d',indexnumber=i)
