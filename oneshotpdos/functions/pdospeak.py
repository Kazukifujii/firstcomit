from pdosfilter import MpPosdata as sob


dir='/home/fujikazuki/Documents/ecalj関係/mp1885'

d=sob(dir)
d.gaussianfilter(0.5)
d.peakdata()
d.peaks.to_csv(dir+'/pdospeaks.csv')