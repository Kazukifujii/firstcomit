dir='/home/fujikazuki/gaustest'

ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]
from xml.dom.expatbuilder import theDOMImplementation
from pdosfilter import PdosFilter

tpdos=PdosFilter(ciflist[0])

print(tpdos.cifdata.cifnumber)
print(tpdos.afterpdosdata['dos.isp1.site001.tmp'].columns.to_list)
print(tpdos.afterpdosdata['dos.isp1.site001.tmp'])


