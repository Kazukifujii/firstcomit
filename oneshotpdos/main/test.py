import functions as fn  
from readinfo import setcifdata

dir='/home/fujikazuki/ciflist_test'
ciflist=[s.replace('\n','') for s in open(dir+'/cif_list.txt').readlines()]
cifinfo=setcifdata(ciflist[0])

dict_df=fn.set_pdosdata(dir+'/result/'+cifinfo.cifnumber)
print(cifinfo.cifnumber)
print(dict_df)

