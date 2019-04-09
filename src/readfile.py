#!env python
import codecs

with codecs.open('../data/sample_hdf5.abc', "r", "UTF-8", "ignore") as f:
    for i in range(20):
        st = f.readline()
        print (st)
