import h5Keysight
import pylab

file = 'keysight1.h5'

t, r = h5Keysight.hdfReadKeysight(file)

pylab.plot(t, r)
pylab.show()

print("Test finished")