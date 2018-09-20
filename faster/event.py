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

from io import BytesIO as StringBuffer

#faster modules (from within module directory)
import faster.file_reader 
import faster.const

class Event(object):
    def __init__(self, header,
                 data):
        self.type_alias=header['type_alias']
        self.type = faster.const.type_alias.get(self.type_alias, 'faster_event')
        self.magic = header['magic']
        self.time = header['clock']
        self.label = header['label']
        self.load_size = header['load_size']
        self.data = None
        self.rawdata = data
        # Dynamic calling of type unpacking:
        getattr(self,
                "_unpack_type_{0}".format(self.type_alias),
                self._unpack_nothing)()

    def _unpack_nothing(self):
         pass       

    def _unpack_type_61(self):
        high, low = struct.unpack("<LL", self.rawdata)
        measure = low & 0xFFFFFC00 >> 10 # ./
        delta_t = high >>7 #  ./
        saturated = (low & 0x40000000) >> 30 #0x00000002 >>1 
        pileup = (low & 0x80000000) >>31 #0x00000001
        self.data = {'dt':delta_t,
                     'value':measure,
                     'saturated':saturated,
                     'pileup':pileup}

    def _unpack_type_10(self):
        '''unpack Group data'''
        # A group is just some generic events...
        the_data = StringBuffer(self.rawdata)
        self.data  = []
        head_data =the_data.read(faster.const.header_size)
        while(head_data):
            header = faster.file_reader.File_reader.read_header(head_data)
            evt_data = faster.file_reader.File_reader.read_data(the_data, header)
            self.data.append(Event(header, data=evt_data))
            head_data =the_data.read(faster.const.header_size)
            pass
        #end while
        pass        
        

    def _unpack_type_70(self):
        '''unpack ADC scaler data'''
        try: 
            calc,sent,trig = struct.unpack("<LLL", self.rawdata)
            self.data = {'calc':calc, 'sent':sent, 'trig':trig}
        except:
            self.data=None

    def _repr_head(self):
        return "<{s.type}, CLOCK={s.time}, LABEL={s.label}, LOAD_SIZE={s.load_size}>".format(s=self)

    def __repr__(self):
        return "<{s.type}, CLOCK={s.time}, LABEL={s.label}, LOAD_SIZE={s.load_size}, DATA='{s.data}'>".format(s=self)
    pass
