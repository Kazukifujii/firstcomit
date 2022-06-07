from operator import index
import os,glob,re
import cv2
import numpy as np
import matplotlib.pyplot as plt
from readinfo import setcifdata,set_pdosdata
import pandas as pd

from readinfo import setcifdata
def sumpdos(dir,ciflist,orbital='s',indexnumber=None):
    """sample
    dir='/home/fujikazuki/ciflist'
    pdir=dir+'/pdospng'
    files=os.listdir(pdir)
    pdoslist=[dir+'/'+f+'.cif' for f in files if os.path.isdir(os.path.join(pdir, f))]
    newciflist=[pdoslist[idx:idx + 4] for idx in range(0,len(pdoslist), 4)]
    for i,cif in enumerate(newciflist):
    pdosplot.sumpdos(pdir,cif,orbital='s',indexnumber=i)
    """
    selectorbital=orbital
    pnglist=list()
    for i,ciffile in enumerate(ciflist):
        cifdata=setcifdata(ciffile)
        pngdir=dir+'/'+cifdata.cifnumber
        if not os.path.isdir(dir):
            print('No such npg is '+pngdir)
            continue
        files=glob.glob(pngdir+"/*.png")
        matchpng=list()
        for file in files:
            if re.compile(selectorbital+".png").search(file):
                matchpng.append(file)
        matchpng=sorted(matchpng)
        pnglist.append(matchpng)
    n_row=len(pnglist)
    n_col=0
    for i in pnglist:
        if n_col<=len(i):
            n_col=len(i)
    img = cv2.imread(pnglist[0][0]) 
    pngh,pngw,pngc=img.shape
    cv2.imwrite(dir+'/whitepng.png',np.full((pngh,pngw),255))
    whitepng=cv2.imread(dir+'/whitepng.png')
    for i in range(n_row):
        png_row=pnglist[i]
        for j in range(n_col):
            if j < len(png_row):
                if j==0:
                    pngrow=cv2.imread(png_row[j])
                    continue
                pngrow=cv2.hconcat([pngrow,cv2.imread(png_row[j])])
            else:
                pngrow=cv2.hconcat([pngrow,whitepng])
        if i==0:
            pngcol=pngrow
            continue
        pngcol= cv2.vconcat([pngcol, pngrow])
    if indexnumber==None:
        cv2.imwrite(dir+'/sumpdos_'+selectorbital+'.png',pngcol)
    else:
        cv2.imwrite(dir+'/['+str(indexnumber)+']sumpdos_'+selectorbital+'.png',pngcol)
    os.remove(dir+'/whitepng.png')

def savepdos(cifdir,orbital=list(range(1,6)),fig_name=str(),key='dos.isp1.site001.tmp'):
    """sample
import re
import os,shutil

from readinfo import setcifdata
#parsing ciffiles in the direcoty
#there result direcoty
cifdir='/home/fujikazuki/ciflist_test'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]

try:
    os.mkdir(cifdir+'/pdospng')
except:
    shutil.rmtree(cifdir+'/pdospng')
    os.mkdir(cifdir+'/pdospng')
os.chdir(cifdir+'/pdospng')

cifdatas=[setcifdata(s) for s in ciflist]

for cifdata in cifdatas:
    os.mkdir(cifdata.cifnumber)
    os.chdir(cifdata.cifnumber)
    for j in range(len(cifdata.allsite)):
        figname=cifdata.formular+str(cifdata.allsite[j])
        key='dos.isp1.site{0:03d}.tmp'.format(j+1)
        for i in range(1,4):
            fs.savepdos(cifdir+'/result'+'/'+cifdata.cifnumber,orbital=[i],fig_name=figname,key=key)
    os.chdir('..')
    """
    plt.clf()
    if not fig_name:
        fig_name=re.search(r"([^/]*?)$",cifdir).group()
    pdosdic=set_pdosdata(cifdir)
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


