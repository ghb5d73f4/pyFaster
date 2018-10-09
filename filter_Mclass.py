#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Feb 20 10:58:08 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: filter_Mclass.py -*-
# -*- purpose: -*-
 
'''
Provides a meta class for filter class.

To use it, just derive the class, define the `_default_fields`,
   overload the `banzai` function 
   and create an instance of the inheriting class
   This will load the input, parse the args and run `banzai`
'''

import sys 

from parse_args import parse_args

class Vfilter(object):
    
    _default_fields = {}

    def __init__(self, *w, **kw):
        if not sys.stdin.isatty():
            self.input = sys.stdin.read()
        else:
            self.input = ''
        self.__dict__.update(self._default_fields)
        self.__dict__.update(parse_args())
        self.banzai(*w, **kw)
        pass

    def banzai(self, *w, **kw):
        pass
