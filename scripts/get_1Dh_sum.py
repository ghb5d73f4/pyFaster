#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Mar 13 14:09:01 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: add1D -*-
# -*- purpose: -*-
 
'''
Module docstring
'''

import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

from filter_Mclass import Vfilter

from pyhisto.bin import Bin
from pyhisto.histogram import Histogram as histo


class make_time_calib(Vfilter):
    """Return the maximum bin"""
    
    _default_fields = {
        'min':None, 'max':None,        
        }

    def banzai(self, *w, **kw):
        h = histo(fromstring=self.input).slice(self.min, self.max)
        sum_ = sum(h)
        print("histogram = \"{0}\"".format(h._repr_()))
        print("integral = {0}".format(sum_))
        pass
    #end banzai
            
if __name__ == '__main__':
    make_time_calib()
