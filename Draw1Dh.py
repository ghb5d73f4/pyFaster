#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Wed Mar  7 09:52:30 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: draw2Dh.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''

import os
import matplotlib.pyplot as plt

from filter_Mclass import Vfilter

from pyhisto.histogram import Histogram as histo


class Draw1Dh(Vfilter):
    """Filter class to draw a 1D histogram"""
    
    _default_fields = {
        'figsize':(25, 12),
        'outext':'.png',
        'grid' : True,
        'xscale':'linear',
        'yscale':'linear',
        'min':None, 'max':None,
        }

    def banzai(self, *w, **kw):
        for f in self.free_params:
            if os.path.exists(f) and os.path.isfile(f):
                h = histo(fromstring=open(f, 'r').read())
                fig = plt.figure(figsize=self.figsize)
                plt.grid(self.grid)
                plt.xscale(self.xscale)
                plt.yscale(self.yscale)
                plt.step(*(h.slice(self.min, self.max)).xy(), where='post')
                plt.savefig(f+self.outext)
                plt.close('all')
                pass
            #end if
            pass
        #end for
        pass
    #end banzai
            
if __name__ == '__main__':
    Draw1Dh()
