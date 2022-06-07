import  makepdos as mp
import re,os,shutil
from readinfo import setcifdata
import pdosplot as pdosp

#parsing ciffiles in the direcoty
#there result direcoty
print(os.getcwd)
cifdir='/samplecif'
#cifdir='~/sampletcif'

#fs.make_pdos_in_di(cifdir)
mp.listup_cif(cifdir)
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]


#saving pdos
try:
    os.mkdir(cifdir+'/pdospng')
except:
    shutil.rmtree(cifdir+'/pdospng')
    os.mkdir(cifdir+'/pdospng')
os.chdir(cifdir+'/pdospng')
cifdatas=[setcifdata(s) for s in ciflist]

for cifdata in cifdatas:
    if cifdata.allsite!=None:
        os.mkdir(cifdata.cifnumber)
        os.chdir(cifdata.cifnumber)
        for j in range(len(cifdata.allsite)):
            figname=str(cifdata.formular)+str(cifdata.allsite[j])
            key='dos.isp1.site{0:03d}.tmp'.format(j+1)
            for i in range(1,4):
                pdosp.savepdos(cifdir+'/result'+'/'+cifdata.cifnumber,orbital=[i],fig_name=figname,key=key)
        os.chdir('..')