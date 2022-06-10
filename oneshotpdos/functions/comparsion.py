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
        
        difdict=dict()
        import matplotlib.pyplot as plt
        for orbital in ORBITAL:
            difdf=pd.DataFrame()
            for j in range(self.speclenge):
                difdf[j]=self.pdos_data_1.sameorbital_pdos[orbital][self.atomlist1[j]]-self.pdos_data_2.sameorbital_pdos[orbital][self.atomlist2[j]]
            self.ifdict[orbital]=difdf
dir='/home/fujikazuki/gaustest'
resultdir='/home/fujikazuki/gaustest/classtest'
ciflist=[s.replace('\n','')  for s in open(dir+'/cif_list.txt')]
tc=ComparsionPdos(cifadress_1=ciflist[0],cifadress_2=ciflist[1])
print(tc.pdos_data_1.cifdata.cifnumber)
print(tc.pdos_data_2.cifdata.cifnumber)
#tc.gaussian(Sigma=0.5)
tc.difference()