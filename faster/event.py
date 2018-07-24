#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:08:42 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: event.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''
import struct

from cStringIO import StringIO as StringBuffer

import file_reader
import const

class Event(object):
    def __init__(self, header,
                 data):
        self.type_alias=header['type_alias']
        self.magic=header['magic']
        self.time = header['clock'].encode("hex")
        self.label=header['label']
        self.load_size=header['load_size']
        self.data=data
        if self.type_alias==70:
            self._unpack_type_70()
        elif self.type_alias==10:
            self._unpack_type_10()
        elif self.type_alias==61:
            self._unpack_type_61()
        pass

    def _unpack_type_61(self):
        the_data = self.data
        high, low = struct.unpack("!LL", the_data)
        delta_t = high & 0x003FFFC0  >>6
        measure = low & 0xFFFFFC00 >> 10
        rnge= low & 0x00000380 >> 7
        saturated=low & 0x00000002 >> 1
        pileup= low & 0x00000001 >> 7
        self.data = {'dt':delta_t,
                     'value':measure,
                     'range':rnge,
                     'saturated':int(saturated),
                     'pileup':int(pileup)}

    def _unpack_type_10(self):
        '''unpack Group data'''
        # A group is just some generic events...
        the_data=StringBuffer(self.data)
        group_evt = []
        head_data =the_data.read(const.header_size)
        while(head_data):
            header = file_reader.File_reader.read_header(head_data)
            evt_data = file_reader.File_reader.read_data(the_data, header)
            group_evt.append(Event(header, data=evt_data))
            head_data =the_data.read(const.header_size)
            pass
        self.data = group_evt
        
        

    def _unpack_type_70(self):
        '''unpack ADC scaler data'''
        the_data=self.data
        if not len(the_data)==struct.calcsize('!LLL'):
            return 0
        calc,sent,trig = struct.unpack("!LLL", the_data)
        self.data = {'calc':calc, 'sent':sent, 'trig':trig}

    def _repr_head(self):
        return "<FasterData TYPE={s.type_alias}, CLOCK={s.time}, LABEL={s.label}, MAGIC={s.magic}, LOAD_SIZE={s.load_size}>".format(s=self)

    def __repr__(self):
        return "<FasterData TYPE={s.type_alias}, CLOCK={s.time}, LABEL={s.label}, MAGIC={s.magic}, LOAD_SIZE={s.load_size}, DATA='{s.data}'>".format(s=self)
    pass
