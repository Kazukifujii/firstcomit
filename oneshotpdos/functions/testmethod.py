
from readinfo import *

def tset_pdosdata(directory):
        '''sample
        dir='~/ciflist/result/1528444'
        dict_df=set_pdosdata(dir)
        '''
        if not os.path.isdir(directory):
            print(directory+" dose no exist")
            return
        files=glob.glob(directory+'/dos.isp1.site*')
        files=[re.search(r"([^/]*?)$",s).group() for s in files]
        opdosdic={key:pd.read_csv(directory+'/'+key,header=None,index_col=0,comment='#',delim_whitespace=True) for key in files}
        r=13.605
        orbital=ORBITAL
        realpdosdic={key:pd.DataFrame(columns=orbital,index=opdosdic[files[0]].index.to_numpy()*r).fillna(0) for key in files}
        for k,key in enumerate(opdosdic):
            opdosdic[key].index=opdosdic[key].index*r
            for i,o in enumerate(orbital,1):
                anl=int(0.5*i*((i-1)*2+2))
                anf=int(0.5*(i-1)*((i-2)*2+2)+1)
                for j in range(anf,anl+1):
                    realpdosdic[key][o]+=opdosdic[key][j]/r
        return pd.concat(realpdosdic,axis=0)

def tset_sameorbital(specdata,pdosdata):
    level_1_keys=np.unique(pdosdata.index.get_level_values(0).to_numpy())
    idx=pd.IndexSlice[level_1_keys,:]
    xdata=pdosdata.xs(level_1_keys[0],level=0).index
    ykeys=[str(s[1]) for s in specdata]
    sameorbital_pdos=dict()
    for o in ORBITAL:
        empty_pdos=pd.DataFrame(index=xdata,columns=ykeys)
        for i,s in enumerate(ykeys):
            sitenumber=int(specdata[i][0])
            idx=pd.IndexSlice['dos.isp1.site{0:03d}.tmp'.format(sitenumber),:]
            empty_pdos[s][:]=pdosdata.loc[idx,o]
        sameorbital_pdos[o]=empty_pdos
    return  pd.concat(sameorbital_pdos)



dir='/home/fujikazuki/gaustest'
resultdir='/home/fujikazuki/gaustest/classtest'
ciflist=[s.replace('\n','')  for s in open(dir+'/cif_list.txt')]
cifdata=setcifdata(ciflist[0])
d1=tset_pdosdata(cifdata.resultadress)
import numpy as np
sd1=tset_sameorbital(cifdata.specsite,pdosdata=d1)
idx=pd.IndexSlice['s',:]
print(sd1)