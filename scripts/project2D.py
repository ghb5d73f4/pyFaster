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

import sys,os

#adding scripts path
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/lib")

from filter_Mclass import Vfilter

from pyhisto.histogram2D import Histogram2D as histo2d


class project2Dh(Vfilter):
    
    _default_fields = {
        'axis':'x',
        'min':-1,
        'max':-1,
        }

    def banzai(self, *w, **kw):
        h2 = histo2d(fromstring=self.input)
        if self.axis=='x':
            print(h2.project_x(self.min, self.max))
        elif self.axis=='y':
            print(h2.project_y(self.min, self.max))
        pass
    #end banzai
            
if __name__=='__main__':
    project2Dh()
