from constant import element_group

from readinfo import setcifdata
cifdir='/home/fujikazuki/gaustest'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]
cifdatas=[setcifdata(s) for s in ciflist]
