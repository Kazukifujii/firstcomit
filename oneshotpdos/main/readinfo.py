#read and set cif's infomation from orignal cif file and SiteInfo.lmchk
#set data teyp is dict. format is {cifnumber:[formula structural,{site number:[site atom,position]]}

import re,os
def siteinfo(file):
    linens=[re.sub(' {2,}','/',s.replace('\n','')).split('/') for s in open(file).readlines()]
    
    relist=list()
    for s in linens:
        relist.append([s[3],(s[5],s[6],s[7])])
    return relist

def formularinfo(file):
    testfile=[s.replace('\n','') for s in open(file).readlines()]
    for s in testfile:
        if re.match('_chemical_formula_structural',s):
            return re.sub("_chemical_formula_structural|\n||'| ",'',s)
    for s in testfile:
        if re.match('_chemical_formula_sum',s):
            print("Instead, capture chemical sum in "+re.search(r"([^/]*?)$",file.strip()).group().replace('.cif',''))
            return re.sub("_chemical_formula_|\n||'| ",'',s)

    print('no formula data '+re.search(r"([^/]*?)$",file.strip()).group().replace('.cif',''))
    return None

    #linens=s.replace('\n','') for s in open(file).readlines()
    return


def listupAllsite(dir):
    '''sample 
    dir='/home/fujikazuki/testd'

    with open(cifdir+'/cif_list.txt',mode='r') as f:
        cifnumber=[re.search(r"([^/]*?)$",s.strip()).group().replace('.cif','') for s in f.readlines()]

    for s in cifnumber:
        print(fs.listupAllsite(cifdir+'/result'+'/'+s))
    '''
    linens=open(dir+'/ciftext.txt').readlines()
    matchlist=list()
    for i,line in enumerate(linens):
        if re.match('All sites',line):
            j=i+2#start point at Atom in All site
            break
    atomicline=list()
    while True:
        if re.match('\n',linens[j]):
            break
        atomicline.append(linens[j].replace('\n',''))
        j+=1
    return atomicline

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
        else:
            print('No such file is'+atomsitefile)
            self.allsite=None
        if os.path.isfile(ciffile):
            self.formular=formularinfo(ciffile)
        else:
            print('No such file is '+ciffile)
            self.formular=None
        
