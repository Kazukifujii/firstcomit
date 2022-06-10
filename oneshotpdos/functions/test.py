dir='/home/fujikazuki/gaustest'

ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]
from readinfo import setcifdata
td=setcifdata(ciflist[0])
from pdosfilter import pdosfilter

tpdos=pdosfilter(td.resultadress)
import os
os.chdir(dir)

tpdos.make_sameorbitaldata(td.specsite)
tpdos.savepdos_sameorbital(td.specsite)