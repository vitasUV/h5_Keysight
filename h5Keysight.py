import sys
import h5py
import numpy as np
from collections import namedtuple

def hdfReadKeysight(h5file):
    ''' read h5file and return data as numpy array
    Oscilloscope Infinium S-series
    :h5file: path to bin file
    '''
    memory1atrr = namedtuple("memory1atrr",
                                "waveformType Start nPoints NumSegments\
                                count xDispRange xDispOrigin xInc xOrg \
                                xUnits yDispRange yDispOrigin YInc YOrg \
                                yReference yUnits minBandwidth maxBandwidth \
                                SavedIntFct DispIntFct IntSetting WavAttr FFT_RBW")

    m1dataAttr = namedtuple("m1dataAttr",
                                "LfdSeed StartIndex DataType DecMode \
                                PktSize RawNumPst ReductionAllowed \
                                MemConIntlvMode InfoValid SegmentedTimeTag \
                                SegmentedXOrg")
    try:
        f = h5py.File(h5file, 'r')
        if f["/FileType/KeysightH5FileType"].value != b'Keysight Waveform':
            return None, None
        mem = f["/Waveforms/Memory 1"]
        dataset = f["/Waveforms/Memory 1/Memory 1Data"]
        attr1 = memory1atrr._make(list(mem.attrs.values()))
        d1attr = m1dataAttr._make(list(dataset.attrs.values()))
        stop = attr1.xOrg + attr1.nPoints * attr1.xInc
        time = np.linspace(attr1.xOrg, stop, attr1.nPoints)
        data = dataset.value
        return time, data
    except:
        sys.stderr.write("%s open error\n" & (h5file))
        return None, None
    finally:
        f.close()