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
import math


# Max size of file is 2GB, events are at least 12 bytes long
max_number_of_events_in_file = 180000000

# Max amplitude in ADC data
adc_coding_size = 22
max_adc_amplitude = int(math.pow(2, adc_coding_size-1))

tick_seconds = 2.0e-9
tick_ns = 2.0

header_byte_size = 12 
clock_byte_size = 6
header_fmt = "< B B "+str(clock_byte_size)+"B H H"
header_size = struct.calcsize(header_fmt)
clock_fmt = "<"+str(clock_byte_size)+"B"
clock_multipliers = [1, 256, 65536, 16777216, 4294967296, 1099511627776]


type_alias = {
    70: 'adc_scaler',
    10: 'group',
    61: 'adc_event',
    62: 'trapez_event',
}

