from operator import ne
import pdosplot 
import glob,sys,os

dir='/home/fujikazuki/ciflist'
pdir=dir+'/pdospng'
files=os.listdir(pdir)
pdoslist=[dir+'/'+f+'.cif' for f in files if os.path.isdir(os.path.join(pdir, f))]
newciflist=[pdoslist[idx:idx + 4] for idx in range(0,len(pdoslist), 4)]

for i,cif in enumerate(newciflist):
    pdosplot.sumpdos(dir+'/pdospng',cif,orbital='d',indexnumber=i)
