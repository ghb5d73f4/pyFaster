#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:37:21 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: const.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''

import struct


tick_seconds = 2.0e-9
tick_ns = 2.0

header_byte_size = 12 # from doc
clock_byte_size = 6
#header_fmt = "! B B "+str(clock_byte_size)+"s H H"
header_fmt = "< B "+str(clock_byte_size)+"s B H H" # from my own research
header_size = struct.calcsize(header_fmt)



type_alias = {
}

