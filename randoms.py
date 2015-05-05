from random import *
from cPickle import *
arrs = []
for x in range(50000):
    arrs.append(random())

dump( arrs, open( "save.p", "wb" ) )