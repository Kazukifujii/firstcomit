from pdosfilter import MpPosdata as mpd

dir='/home/fujikazuki/Documents/ecalj関係/mp1000'

d1=mpd(dir)
d1.gaussianfilter(0.5)
d1.peakdata()

import featuretools as ft

es=ft.EntitySet(id='example')

es=es.entity_from_dataframe(entity_id='locations',
                              dataframe=d1.peaks,
                              index='name')
print(es)
