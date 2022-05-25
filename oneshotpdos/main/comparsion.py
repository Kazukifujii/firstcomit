import pandas as pd
import functions
import re
class comparsion_pdos_in_directory():
    """
    import functions
    import re
    directory='/home/fujikazuki/cif_pdos/main/cif_list/result/'
    cif_list=functions.cif_conbination('/home/fujikazuki/cif_pdos/main/cif_list.txt') #return tuple in list
    conp=comparsion_pdos_in_directory(*cif_list[0],directory)
    print(conp.comp_dire_1)
    for s in conp.pdos_data_1:
        print(s)
        print(conp.pdos_data_1[s].shape)
    print(conp.comp_dire_2)
    for s in conp.pdos_data_2:
        print(s)
        print(conp.pdos_data_2[s].shape)
    """
    def __init__(self,comp_dire1,comp_dire2,directory):
        self.comp_dire_1=directory+'/'+comp_dire1.replace('.cif','')
        self.comp_dire_2=directory+'/'+comp_dire2.replace('.cif','')
        self.pdos_data_1=functions.set_pdosdata(self.comp_dire_1)
        self.pdos_data_2=functions.set_pdosdata(self.comp_dire_2)
        self.weight=dict()

