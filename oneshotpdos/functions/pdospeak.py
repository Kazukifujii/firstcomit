from pdosfilter import MpPosdata as sob


dir='/home/fujikazuki/Documents/ecalj関係/mp1000'
dir2='/home/fujikazuki/Documents/ecalj関係/mp1885'

d1=sob(dir)
d1.gaussianfilter(0.5)
d1.peakdata()
d2=sob(dir2)
d2.gaussianfilter(0.5)
d2.peakdata()