import os,sys,subprocess,logging,glob
import shutil
import itertools
import re
import pandas as pd
import matplotlib.pyplot as plt

def pdos_ecalj(cif_name):
    #to make pdos from cif using 'ecalj'
    try:
        cif2cell_c='cif2cell '+cif_name+' -p vasp --vasp-cartesian --vasp-format=5'
        subprocess.run(cif2cell_c,shell=True)
        subprocess.run('vasp2ctrl POSCAR',shell=True)
        subprocess.run('cp ctrls.POSCAR.vasp2ctrl ctrls.tmp',shell=True)
        subprocess.run('ctrlgenPDOStest.py tmp',shell=True)
        subprocess.run('cp ctrlgenPDOStest.ctrl.tmp ctrl.tmp',shell=True)
        subprocess.run('lmfa tmp',shell=True)
        subprocess.run('job_pdos tmp -np 4 NoGnuplot',shell=True)
        #subprocess.run('cif2cell '+cif_name+' >>ciftext.txt',shell=True)
    except:
        print('error in pdos_ecalj')

def listup_cif(directory):
    """
    with open(cifdir+'/cif_list.txt',mode='r') as f:
        ciflist=[re.search(r"([^/]*?)$",s.strip()).group() for s in f.readlines()]
    ciflist[i].replace('.cif',"")
    """
    if not os.path.isdir(directory):
        print('No such directory')
        sys.exit()
    files=glob.glob(directory+"/*.cif")
    for i,file in enumerate(files):
        files[i]=file.replace("./"+directory+"/",'')
    
    with open(directory+'/cif_list.txt',mode='w') as f:
        f.write('\n'.join(files))
    return

def cif_conbination(cif_dir):
    cif_list_txt=cif_dir+'/cif_list.txt'
    if not os.path.isfile(cif_list_txt):
        listup_cif(cif_dir)
    with open(cif_list_txt,mode='r') as f:
            ciflist=[re.search(r"([^/]*?)$",s.strip()).group() for s in f.readlines()]
    return list(itertools.combinations(ciflist,2))

def make_pdos_in_di(cif_directory):
    '''sample program
    make_pdos_in_di('~/cif_list')
    '''
    get_now_directory=os.getcwd()
    listup_cif(cif_directory)
    with open(cif_directory+'/cif_list.txt',mode='r') as f:
        cif_list=[s.strip() for s in f.readlines()]
    result_di=cif_directory+'/result'
    try:
        os.mkdir(result_di)
    except:
        shutil.rmtree(result_di)
        os.mkdir(result_di)

    for cif_file in cif_list:
        try:
            directory_name=cif_file.replace('.cif','')
            directory_name=result_di+'/'+re.search(r"([^/]*?)$",directory_name).group()
            #subprocess.run('cp '+cif_file+' '+directory_name+'/'+cif_number+'.cif',shell=True)
            os.mkdir(directory_name)
            os.chdir(directory_name)
            pdos_ecalj(cif_file)
            os.chdir('..')
        except:
            print('error in for cif')
    os.chdir(get_now_directory)

def set_pdosdata(directory):
        '''sample
        dir='~/ciflist/result/1528444'
        dict_df=set_pdosdata(dir)
        '''
        if not os.path.isdir(directory):
            print(directory+" dose no exist")
        files=glob.glob(directory+'/dos.isp1.site*')
        result=list()
        for i in files:
                result.append(re.search(r"([^/]*?)$",i).group())
        #df=pd.read_csv(directory+'/'+result[0],header=None,index_col=0,comment='#',delim_whitespace=True)
        dict_df=dict()
        for s in result:
            dict_df[s]=pd.read_csv(directory+'/'+s,header=None,index_col=0,comment='#',delim_whitespace=True)
        return dict_df

def savepdos(cifdir,orbital=list(range(1,6)),fig_name=str(),key='dos.isp1.site001.tmp'):
    """sample
import  functions as fs
from comparsion import comparsion_pdos_in_directory
import re
import os,shutil

from readinfo import setcifdata
#parsing ciffiles in the direcoty
#there result direcoty
cifdir='/home/fujikazuki/ciflist_test'
ciflist=[s.replace('\n','') for s in open(cifdir+'/cif_list.txt').readlines()]

try:
    os.mkdir(cifdir+'/pdospng')
except:
    shutil.rmtree(cifdir+'/pdospng')
    os.mkdir(cifdir+'/pdospng')
os.chdir(cifdir+s')

cifdatas=[setcifdata(s) for s in ciflist]

for cifdata in cifdatas:
    os.mkdir(cifdata.cifnumber)
    os.chdir(cifdata.cifnumber)
    for j in range(len(cifdata.allsite)):
        figname=cifdata.formular+str(cifdata.allsite[j])
        key='dos.isp1.site{0:03d}.tmp'.format(j+1)
        for i in range(1,4):
            fs.savepdos(cifdir+'/result'+'/'+cifdata.cifnumber,orbital=[i],fig_name=figname,key=key)
    os.chdir('..')
    """
    plt.clf()
    if not fig_name:
        fig_name=re.search(r"([^/]*?)$",cifdir).group()
    try:
        pdosdic=set_pdosdata(cifdir)
        print(key)
        pdosdf=pdosdic[key]
    except:
        print('No data '+fig_name)
        return
    r=13.605
    pdosdf.index=pdosdf.index*r
    realpdosdf=pd.DataFrame(columns=orbital,index=pdosdf.index).fillna(0)
    ls=list()
    for i in orbital:
        anl=int(0.5*i*((i-1)*2+2))
        anf=int(0.5*(i-1)*((i-2)*2+2)+1)
        for j in range(anf,anl+1):
            realpdosdf[i]=pdosdf[j]/r+realpdosdf[i]
            ls.append(j)
        realpdosdf[i].plot()
    for i in range(len(orbital)):
        I=orbital[i]
        if I==1:
            orbital[i]='s'
        elif I==2:
            orbital[i]='p'
        elif I==3:
            orbital[i]='d'
        elif I==4:
            orbital[i]='f'
    plt.ylim([0,5])
    plt.xlim([-20,20])
    plt.grid()
    plt.legend(orbital)
    titile=fig_name+'_'+re.sub("\[|\]|'|","",str(orbital))
    plt.title(titile)
    plt.savefig(titile+'.png')
