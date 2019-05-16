
import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

import argparse

from pyhisto.histogram import Histogram as histo
#from pyhisto.tools import FindPeaks
from pyhisto.tools import GaussRealFit


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Autocalibration of an histogram')
    parser.add_argument('file', type=str,
                        nargs='?', help="histogram.1d.txt file to read")
    args = parser.parse_args()
    Ref152Eu = map(float, """121.7817
244.6974
344.2785
411.1165
443.965
778.9045
867.380
964.079
1299.142
1408.013""".split('\n'))
    if os.path.exists(args.file) and os.path.isfile(args.file):
        h = histo(fromfile=args.file)
        fwhms = []
        errs = []
        for eref in Ref152Eu:
            hzoom = h.slice(eref-8.,
                            eref+8.)
            gf = GaussRealFit(hzoom)
            err_center = eref - gf.mean
            fwhm = gf.stdev*2.35482
            fwhms.append(fwhm)
            errs.append(err_center)
            print("{0} {1.mean} {2} {3} ".format(eref,
                                                 gf,
                                                 err_center,
                                                 fwhm))
            #gf.plot()
            
