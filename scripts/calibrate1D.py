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

from pyhisto.histogram import Histogram as histo


class calibrate1D(Vfilter):
    """Filter class to calibrate a 1D hisotgrams"""
    
    _default_fields = {
        'offset':0.0,
        'slope':1.0,
        'use_function':False,
        'calib_function': lambda x:x,
        }

    def banzai(self, *w, **kw):
        # first, create the basic histo from the first one
        if not self.use_function:
            print("#calibrating with offset={0}, slope={1}".format(self.offset, self.slope))
        hout = histo(fromstring=self.input)
        for b in hout:
            if not self.use_function:
                b.lowedge = b.lowedge*self.slope + self.offset
                b.upedge = b.upedge*self.slope + self.offset
            elif self.use_function:
                b.lowedge = self.calib_function(b.lowedge)
                b.upedge = self.calib_function(b.upedge)
            b.upedge, b.lowedge = max(b.upedge, b.lowedge), min(b.upedge, b.lowedge)
        #end for
        hout._frombins(hout.bins)
        print(hout)
        pass
    #end banzai
            
if __name__ == '__main__':
    calibrate1D()
