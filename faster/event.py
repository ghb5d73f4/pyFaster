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

_the_61_unpacker = struct.Struct("<LL")
_the_62_unpacker = struct.Struct("<L")
_the_70_unpacker = struct.Struct("<LLL")



class Event(object):
    def __init__(self, header,
                 data):
        self.type_alias = header['type_alias']
        #self.type = 'unknown'
        #self.magic = header['magic']
        self.time = header['clock']
        self.label = header['label']
        self.load_size = header['load_size']
        #self.data = {}
        self.rawdata = data
        pass
    #end of __init__
        
    def __getattr__(self, attr):
        ''' Used to get Just-In-Time interpreted attributes '''
        return getattr(self, "_get_{0}".format(attr),
                        self._get_nothing)()
        
    def _get_type(self):
        self.type = faster.const.type_alias.get(self.type_alias, 
                                               'faster_event_{}'.format(self.type_alias))
        return self.type
    
    def _get_data(self):
        '''return the unpacked data, and store it in self.data'''
        getattr(self,
                "_unpack_type_{0}".format(self.type_alias),
                self._unpack_nothing)()
        return self.data

    def _get_nothing(self):
        raise AttributeError
        return None
    
    def _unpack_nothing(self):
        self.data= {}

    def _unpack_type_61(self):
        high, low = _the_61_unpacker.unpack(self.rawdata)
        measure = low & 0xFFFFFC00 >> 10 # ./
        delta_t = high >>7 #  ./
        saturated = (low & 0x40000000) >> 30 #0x00000002 >>1 
        pileup = (low & 0x80000000) >>31 #0x00000001
        self.data = {'dt':delta_t,
                     'value':measure,
                     'saturated':saturated,
                     'pileup':pileup}


    def _unpack_type_62(self):
        word = _the_62_unpacker.unpack(self.rawdata)[0]
        measure = word & 0x007FFFFF
        saturated = (word & 0x40000000) >> 30
        pileup = (word & 0x20000000) >> 29
        tdc = (word & 0x1f800000) >> 25
        sat_cpz = (word & 0x80000000) >> 31
        self.data={'value': measure,
                   'tdc': tdc,
                   'saturated': saturated,
                   'sat_cpz': sat_cpz,
                   'pileup': pileup}


    def _unpack_type_10(self):
        '''unpack Group data'''
        # A group is just some generic events...
        self.data  = {'events': [],
                      'size': 0}
        try:
            the_data = StringBuffer(self.rawdata)
            head_data = the_data.read(faster.const.header_size)
            while(head_data):
                header = faster.file_reader.File_reader.read_header(head_data)
                evt_data = faster.file_reader.File_reader.read_data(the_data, header)
                self.data['events'].append(Event(header, data=evt_data))
                head_data = the_data.read(faster.const.header_size)
                pass
            #end while
            self.data['size']=len(self.data['events'])
        except:
            self.data['error']=True
        pass        
        

    def _unpack_type_70(self):
        '''unpack ADC scaler data'''
        try: 
            calc,sent,trig = _the_70_unpacker.unpack(self.rawdata)
            self.data = {'calc':calc, 'sent':sent, 'trig':trig}
        except:
            self.data = {}

    def _repr_head(self):
        return "<{s.type}, CLOCK={s.time}, LABEL={s.label}, LOAD_SIZE={s.load_size}>".format(s=self)

    def __repr__(self):
        return "<{s.type}, CLOCK={s.time}, LABEL={s.label}, LOAD_SIZE={s.load_size}, DATA={s.data}>".format(s=self)
    pass
