from pdosfilter import MpPosdata as mpd
dir='/home/fujikazuki/Documents/mp2534'

t=mpd(dir)
t.gaussianfilter(sigma=0.5)
t.peakdata_histogram()
t.peaks_h