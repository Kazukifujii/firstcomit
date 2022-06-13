from importlib.util import spec_from_file_location
import pandas as pd
from pdosfilter import PdosFilter
from readinfo import setcifdata
import re,os,itertools
from constant import element_group,ORBITAL
from makepdos import listup_cif

def cif_conbination(cif_dir):
    cif_list_txt=cif_dir+'/cif_list.txt'
    if not os.path.isfile(cif_list_txt):
        listup_cif(cif_dir)
    with open(cif_list_txt,mode='r') as f:
            ciflist=[re.search(r"([^/]*?)$",s.strip()).group() for s in f.readlines()]
    return list(itertools.combinations(ciflist,2))

class ComparsionPdos():
    """
    """
    def __init__(self,cifadress_1,cifadress_2):
        self.pdos_data_1=PdosFilter(cifadress_1)
        self.pdos_data_2=PdosFilter(cifadress_2)
        if len(self.pdos_data_1.cifdata.specsite)!=len(self.pdos_data_2.cifdata.specsite):
            print('not same number of specsite')
            return
        self.weight=dict()
        self.speclenge=len(self.pdos_data_1.cifdata.specsite)
        atomlist1=[(str(i[1]),element_group[i[1][0]]) for i in self.pdos_data_1.cifdata.specsite]
        atomlist2=[(str(i[1]),element_group[i[1][0]]) for i in self.pdos_data_2.cifdata.specsite]
        atomlist1.sort(key = lambda x: x[1])
        atomlist2.sort(key = lambda x: x[1])
        self.atomlist1=[s for s,_ in atomlist1]
        self.atomlist2=[s for s,_ in atomlist2]
    
    def gaussian(self,Sigma):
        self.pdos_data_1.gaussianfilter(sigma=Sigma)
        self.pdos_data_2.gaussianfilter(sigma=Sigma)
        
    
    def difference(self):
        #sort by element group number
        if len(self.pdos_data_1.cifdata.specsite)!=len(self.pdos_data_2.cifdata.specsite):
            print('not same number of specsite')
            return
        self.pdos_data_1.make_sameorbitaldata()
        self.pdos_data_2.make_sameorbitaldata()
        self.difdict=dict()
        for orbital in ORBITAL:
            difdf=pd.DataFrame()
            for j in range(self.speclenge):
                difdf[j]=abs(self.pdos_data_1.sameorbital_pdos[orbital][self.atomlist1[j]]-self.pdos_data_2.sameorbital_pdos[orbital][self.atomlist2[j]])
            self.difdict[orbital]=difdf
    

dir='/home/fujikazuki/gaustest'
resultdir='/home/fujikazuki/gaustest/classtest'
ciflist=[s.replace('\n','')  for s in open(dir+'/cif_list.txt')]
tc=ComparsionPdos(cifadress_1=ciflist[10],cifadress_2=ciflist[2])
print(tc.pdos_data_1.cifdata.specsite)
print(tc.pdos_data_2.cifdata.specsite)
tc.gaussian(Sigma=0.5)
tc.difference()
import matplotlib.pyplot as plt
tc.difdict['p'].plot()
plt.ylim([0,5])
plt.xlim([-20,40])
plt.grid()
plt.show()
