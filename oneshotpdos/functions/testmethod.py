from readinfo import *


class setcifdata():
    #only set cif file name 
    #ciffile='~/1000017.cif'
    """
    cifdir='/home/fujikazuki/ciflist_test'
    with open(cifdir+'/cif_list.txt',mode='r') as f:
        ciflist=[s.replace('\n','') for s in f]
    cifdata=[setcifdata(s) for s in ciflist]
    for i in range(len(cifdata)):
        print(cifdata[i].allsite)
    """
    def __init__(self,ciffile):
        self.cifadress=ciffile
        self.cifnumber=re.search(r"([^/]*?)$",ciffile.strip()).group().replace('.cif','')
        self.resultadress=ciffile.replace(self.cifnumber+'.cif','')+'result/'+self.cifnumber
        atomsitefile=self.resultadress+'/SiteInfo.lmchk'
        if os.path.isfile(atomsitefile):
            self.allsite=siteinfo(atomsitefile)
            self.specsite=specinfo(atomsitefile)
        else:
            print('No such file is'+atomsitefile)
            self.allsite=None
        if os.path.isfile(ciffile):
            self.formular=formularinfo(ciffile)
        else:
            print('No such file is '+ciffile)
            self.formular=None